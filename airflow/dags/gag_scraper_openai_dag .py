import requests

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook

default_args = {
    'owner': 'marcose',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


def last_scraped_episode_date(ti):
    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    conn = postgres_sql.get_conn()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT published FROM episodes_raw ORDER BY published DESC LIMIT 1
                    """)
    result = cursor.fetchone()
    last_date = str(result[0]) if result else None
    ti.xcom_push(key="last_scraped_date", value=last_date)


def scrape_feed(ti):
    import feedparser
    import pandas as pd

    feed_url = "https://geschichten-aus-der-geschichte.podigee.io/feed/mp3"
    episode_feed = feedparser.parse(feed_url)
    last_date = ti.xcom_pull(
        task_ids='get_last_scraped_episode_date', key='last_scraped_date')
    df = pd.DataFrame(episode_feed['entries'])
    df['id'] = df['title']
    df = df[['id', 'title', 'subtitle', 'summary', 'published', 'link', 'image']]
    df['published'] = pd.to_datetime(df['published'])
    df['image'] = df['image'].astype(str).str.replace('\'', '"')

    if last_date:
        df = df[df.publsihed > last_date]

    episode_list = list(df.itertuples(index=False, name=None))

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    postgres_sql.insert_rows('episodes_raw', episode_list,
                             replace=True, replace_index="id",
                             target_fields=['id', 'title', 'subtitle', 'summary', 'published', 'link', 'image'])


def create_thumbnail_link(episode_id, image_url):
    import numpy as np

    endpoint = 'http://flask:5000/get-episode-image-from-link'
    info = {
        'url': image_url,
        'episode_id': episode_id
    }

    response = requests.post(endpoint, data=info)

    if response.status_code == requests.codes.ok:
        return response.text

    return np.NaN


def clean_push_episodes():
    import numpy as np
    import re

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    df = postgres_sql.get_pandas_df("SELECT * FROM episodes_raw")

    df['id'] = df['title'].str.split(': ').str[0]
    df = df[df.id.str.startswith('GAG')]
    df['title'] = df['title'].str.split(': ').str[1]

    df['summary'] = df['summary'].str.split('//Aus unserer Werbung').str[0]
    df['summary'] = df['summary'].str.split('//AUS UNSERER WERBUNG').str[0]
    df['summary'] = df['summary'].str.split(
        'Du möchtest mehr über unsere Werbepartner erfahren?').str[0]

    df['summary'] = df['summary'].str.split('Das erwähnte Buch').str[0]
    df['summary'] = df['summary'].str.split('Literatur').str[0]
    df['summary'] = df['summary'].str.split('LITERATUR').str[0]

    df['summary'] = df['summary'].str.replace('//', ' ')
    df['summary'] = df['summary'].str.replace('\n', ' ')

    df['image'] = df['image'].map(lambda x: re.findall(
        '{"href": "(.+?)"}', x)[0] if x != 'nan' else np.NaN)

    df['thumbnail'] = df.apply(lambda x: np.NaN if x.image ==
                               np.NaN else create_thumbnail_link(x.id, x.image), axis=1)

    clean_episode_list = list(df.itertuples(index=False, name=None))
    postgres_sql.insert_rows('episodes_target', clean_episode_list,
                             replace=True, replace_index="id",
                             target_fields=list(df.columns))


def extract_and_save_entities():
    import openai
    import json

    openai.api_key = "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"

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    episode_df = postgres_sql.get_pandas_df("""
        SELECT id, summary, title, subtitle 
        FROM episodes_target 
        WHERE story_time_start IS NULL AND story_time_end IS NULL
        """)

    episode_df['text'] = episode_df['title'] + '. ' + \
        episode_df['subtitle'] + '. ' + episode_df['summary']
    episode_df = episode_df[['id', 'text']]

    system = {"role": "system",
              "content": "Du bist ein Assistent der nur JSON spricht."}

    prompt_template = """
    Der Text beinhaltet den Titel und eine Zusammenfassung einer Geschichts-Podcast Episode. Schreib mir für den Text alle enthaltenen Orte, die Zeit in der die Geschichte aus der Episode spielt und die Kategorien, in welche die Geschichte eingeordnet werden kann. Schreibe für die Orte den Namen ohne Zusatz, den Kontext, in dem Sie besprochen werden und die genauen Koordinaten als numerische Werte ohne Angabe von Maßeinheit oder Himmeldrichtung. Für die Zeit schreibe eine textliche Beschreibung, sowie das Jahr in dem die Geschichte beginnt und endet als Ganzzahl. Für die Kategorien, brauche ich einen Namen und eine kurze Beschreibung und Einordnung der Geschichte in die Kategorie. Das Wort Geschichte darf keine eigene Kategorie sein.
    Gebx^e die Antwort im Format:
    {
    "locations": [
    {
    "name":
    "context":
    "coordinates": {
    "lat":
    "long":
    }
    }
    ],
    "time": {
    "description":
    "start_year":
    "end_year":
    },
    "categories": [
    {
    "category_name":
    "description":
    }
    ]
    }
    """

    locations = {}
    topics = {}
    times = {}

    max_retries = 5

    for entry in episode_df.itertuples():

        response = None

        # Try to request and parse the response, maximum 5 times
        for i in range(max_retries):
            print(f"Requesting {entry.id}. Try Nr. {i+1}")

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", messages=[system, {"role": "user", "content": prompt_template + entry.text}])

            if response.choices[0].finish_reason != "stop":
                print(f"Model did not finish. Retrying...")
                continue

            try:
                entities = response_dict = json.loads(
                    response.choices[0].message.content)
                print(f"Got response for {entry.id}. Breaking")
                break
            except json.decoder.JSONDecodeError:
                print(f"{entry.id} Errornous JSON Format. Retrying...")
                continue

        if not response:
            print(f'No valid response after 5 retries for episode {entry.id}')
            continue

        try:
            for loc in entities['locations']:
                if loc['name'] in locations:
                    locations[loc['name']]['episodes'].append(
                        {"id": entry.id, "context": loc['context']})
                    locations[loc['name']]['coordinates'].append(
                        {'latitude': loc['coordinates']['lat'], 'longitude': loc['coordinates']['long']})
                else:
                    if loc['coordinates']:
                        locations[loc['name']] = {
                            "episodes": [{"id": entry.id, "context": loc['context']}],
                            "coordinates": [{'latitude': loc['coordinates']['lat'], 'longitude': loc['coordinates']['long']}]
                        }
                    else:
                        locations[loc['name']] = {
                            "episodes": [{"id": entry.id, "context": loc['context']}], "coordinates": []
                        }

            for topic in response_dict['categories']:
                if topic['category_name'] in topics:
                    topics[topic['category_name']].append(
                        {"id": entry.id, "context": topic['description']})
                else:
                    topics[topic['category_name']] = [
                        {"id": entry.id, "context": topic['description']}]

            times[entry.id] = response_dict['time']
        except Exception:
            print("Wrong keyed JSON Format")
            continue

    locations_list = locations.keys()
    locations_tup = [tuple([loc]) for loc in locations_list]

    postgres_sql.insert_rows('locations', locations_tup,
                             replace=True, replace_index="name",
                             target_fields=['name'])

    topics_list = topics.keys()
    topics_tup = [tuple([topic]) for topic in topics_list]

    postgres_sql.insert_rows('topics', topics_tup,
                             replace=True, replace_index="name",
                             target_fields=['name'])

    for loc, data in locations.items():
        episodes = data['episodes']
        coords = data['coordinates']

        episode_values = [tuple([loc,  ep['id'],  ep['context']])
                          for ep in episodes]
        coord_values = [tuple([loc,  coord['longitude'],  coord['latitude']])
                        for coord in coords]

        postgres_sql.insert_rows('episodes_locations', episode_values,
                                 target_fields=['location_name', 'episode_id', 'context'])
        postgres_sql.insert_rows('coordinates', coord_values,
                                 target_fields=['location_name', 'longitude', 'latitude'])

    for top, epidsodes in topics.items():
        values = [tuple([top, ep['id'], ep['context']]) for ep in epidsodes]

        postgres_sql.insert_rows('episodes_topics', values,
                                 target_fields=['topic_name', 'episode_id', 'context'])

    for episode_id, time in times.items():
        # values = tuple([episode_id, time['start_year'],
        #                 time['end_year'], time['description']])

        sql = f"UPDATE episodes_target SET story_time_start = '{time['start_year']}', story_time_end = '{time['end_year']}', story_time_description = '{time['description']}' WHERE id = '{episode_id}';"

        postgres_sql.run(sql)
        # postgres_sql.run('episodes_target', values,
        #                          replace=True, replace_index="id",
        #                          target_fields=['id', 'story_time_start',
        #                                         'story_time_end', 'story_time_description'])


def get_coordinates_for_locations():
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    locations_df = postgres_sql.get_pandas_df(
        "SELECT name FROM locations WHERE requested IS false")

    geolocator = Nominatim(user_agent="karten_aus_der_geschichte")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    locations_df['coordinates'] = locations_df['name'].apply(geocode)
    locations_df['longitude'] = locations_df['coordinates'].apply(
        lambda loc: loc.longitude if loc else None)
    locations_df['latitude'] = locations_df['coordinates'].apply(
        lambda loc: loc.latitude if loc else None)
    locations_df['requested'] = True

    target_df = locations_df[['name', 'longitude', 'latitude', 'requested']]
    location_values = list(target_df.itertuples(index=False, name=None))

    postgres_sql.insert_rows('locations', location_values,
                             replace=True, replace_index="name",
                             target_fields=list(target_df.columns))


with DAG(
    dag_id='kag_scraper_openai_dag_v1',
    start_date=datetime(2023, 3, 18),
    schedule_interval='@daily',
    catchup=False
) as dag:
    # 0. Create Tables if not exist
    create_tables = PostgresOperator(
        task_id='postgres_create',
        postgres_conn_id='postgres_be',
        sql=["""
            CREATE TABLE IF NOT EXISTS episodes_raw (
                id VARCHAR NOT NULL PRIMARY KEY,
                title VARCHAR NOT NULL,
                subtitle VARCHAR,
                summary VARCHAR NOT NULL,
                link VARCHAR NOT NULL,
                image VARCHAR,
                published DATE);
            """, """
            CREATE TABLE IF NOT EXISTS episodes_target (
                id VARCHAR NOT NULL PRIMARY KEY,
                title VARCHAR NOT NULL,
                subtitle VARCHAR,
                summary VARCHAR NOT NULL,
                link VARCHAR NOT NULL,
                image VARCHAR,
                thumbnail VARCHAR,
                published DATE,
                story_time_start VARCHAR,
                story_time_end VARCHAR,
                story_time_description VARCHAR
                );
            """, """
            CREATE TABLE IF NOT EXISTS topics (
                name VARCHAR NOT NULL PRIMARY KEY,
                valid BOOL DEFAULT true);
            """, """
            CREATE TABLE IF NOT EXISTS episodes_topics (
                id SERIAL PRIMARY KEY,
                episode_id VARCHAR REFERENCES episodes_target(id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                topic_name VARCHAR REFERENCES topics(name)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                context VARCHAR);
            """, """
            CREATE TABLE IF NOT EXISTS locations (
                name VARCHAR NOT NULL PRIMARY KEY,
                longitude VARCHAR,
                latitude VARCHAR,
                requested BOOL DEFAULT false,
                valid BOOL DEFAULT true);
            """, """
            CREATE TABLE IF NOT EXISTS coordinates (
                id SERIAL PRIMARY KEY,
                location_name VARCHAR REFERENCES locations(name)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                longitude VARCHAR,
                latitude VARCHAR,
                active BOOL DEFAULT true);
            """, """
            CREATE TABLE IF NOT EXISTS episodes_locations(
                id SERIAL PRIMARY KEY,
                episode_id VARCHAR REFERENCES episodes_target(id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                location_name VARCHAR REFERENCES locations(name)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                context VARCHAR);
            """]
    )

    # 1. Get last Episodes Publishing Date
    get_last_scraped_episode_date = PythonOperator(
        task_id='get_last_scraped_episode',
        python_callable=last_scraped_episode_date

    )

    # 2. Get all new Episodes from Feed ()
    scrape_episodes = PythonOperator(
        task_id='feed_scraper',
        python_callable=scrape_feed
    )

    # 3. Title & Summary Cleaning + Ticker
    clean_episodes = PythonOperator(
        task_id="clean_episodes",
        python_callable=clean_push_episodes
    )

    # 4. Extract, link and save locations
    extract_locations = PythonOperator(
        task_id="extract_locations",
        python_callable=extract_and_save_entities
    )

    # 5. Get coordinates for location string
    # get_coordinates = PythonOperator(
    #     task_id="get_coordinates",
    #     python_callable=get_coordinates_for_locations
    # )

    create_tables >> get_last_scraped_episode_date >> scrape_episodes >> clean_episodes >> extract_locations

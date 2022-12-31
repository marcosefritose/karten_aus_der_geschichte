from geopy.extra.rate_limiter import RateLimiter
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook



default_args = {
    'owner': 'marcose',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def last_scraped_episode_date(ti):
    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='gag')
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
        postgres_conn_id='postgres_be', schema='gag')
    postgres_sql.insert_rows('episodes_raw', episode_list,
                                replace=True, replace_index="id",
                                target_fields=['id', 'title', 'subtitle', 'summary', 'published', 'link', 'image'])

def clean_push_episodes():
    import numpy as np
    import re
    
    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='gag')
    df = postgres_sql.get_pandas_df("SELECT * FROM episodes_raw")
    
    df['id'] = df['title'].str.split(': ').str[0]
    df = df[df.id.str.contains('GAG')]
    df['title'] = df['title'].str.split(': ').str[1]
    
    df['summary'] = df['summary'].str.split('//Aus unserer Werbung').str[0]
    df['summary'] = df['summary'].str.split(
        'Du möchtest mehr über unsere Werbepartner erfahren?').str[0]
    
    df['image'] = df['image'].map(lambda x: re.findall(
        '{"href": "(.+?)"}', x)[0] if x != 'nan' else np.NaN)
    
    clean_episode_list = list(df.itertuples(index=False, name=None))
    postgres_sql.insert_rows('episodes_target', clean_episode_list,
                             replace=True, replace_index="id",
                             target_fields=list(df.columns))
    

def extract_and_link_locations():
    import spacy
    
    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='gag')
    episode_df = postgres_sql.get_pandas_df("SELECT id, summary, title, subtitle FROM episodes_target")

    episode_df['text'] = episode_df['title'] + ' ' + episode_df['subtitle'] + ' ' + episode_df['summary'] 
    episode_df = episode_df[['id', 'text']]
    
    nlp = spacy.load("de_core_news_lg")
    locations = {}

    for entry in episode_df.itertuples():
        text_doc = nlp(entry.text)
        
        for word in text_doc.ents:
            clean_string = word.text.replace('.', '').strip()
            
            if word.label_ == 'LOC' and 'http' not in clean_string:
                
                if clean_string in locations:
                    locations[clean_string].append(entry.id)
                else:
                    locations[clean_string] = [entry.id]

    locations_list = locations.keys()
    locations_tup = [tuple([loc]) for loc in locations_list]
    
    postgres_sql.insert_rows('locations', locations_tup,
                             replace=True, replace_index="name",
                             target_fields=['name'])
    
    for loc, ep_ids in locations.items():
        ep_ids = list(set(ep_ids))
        values = [tuple([loc, ep_id]) for ep_id in ep_ids]
        
        postgres_sql.insert_rows('episodes_locations', values,
                                 target_fields=['location_name', 'episode_id'])
        
def get_coordinates_for_locations():
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter
    
    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='gag')
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
    dag_id='gag_scraper_dag_v1',
    start_date=datetime(2022, 12, 29),
    schedule_interval='@daily'
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
                published DATE);
            """, """
            CREATE TABLE IF NOT EXISTS locations (
                name VARCHAR NOT NULL PRIMARY KEY,
                longitude VARCHAR,
                latitude VARCHAR,
                requested BOOL DEFAULT false,
                valid BOOL DEFAULT true);
            """, """
            CREATE TABLE IF NOT EXISTS episodes_locations(
                id SERIAL PRIMARY KEY,
                episode_id VARCHAR REFERENCES episodes_target(id) 
                    ON UPDATE CASCADE ON DELETE CASCADE,
                location_name VARCHAR REFERENCES locations(name) 
                    ON UPDATE CASCADE ON DELETE CASCADE);
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
        python_callable=extract_and_link_locations
    )
    
    # 5. Get coordinates for location string
    get_coordinates = PythonOperator(
        task_id="get_coordinates",
        python_callable=get_coordinates_for_locations
    )
    
    create_tables >> get_last_scraped_episode_date >> scrape_episodes >> clean_episodes >> extract_locations >> get_coordinates

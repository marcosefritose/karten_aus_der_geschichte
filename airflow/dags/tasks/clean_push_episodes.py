import numpy as np
import re
import requests

from airflow.hooks.postgres_hook import PostgresHook


def clean_push_episodes():
    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    df = postgres_sql.get_pandas_df("SELECT * FROM episodes_raw")

    df['key'] = df['title'].str.split(': ').str[0]

    df = df[df.key.str.contains('GAG')]
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


def create_thumbnail_link(episode_id, image_url):
    endpoint = 'http://flask:5000/get-episode-image-from-link'
    info = {
        'url': image_url,
        'episode_id': episode_id
    }

    response = requests.post(endpoint, data=info)

    if response.status_code == requests.codes.ok:
        return response.text

    return np.NaN

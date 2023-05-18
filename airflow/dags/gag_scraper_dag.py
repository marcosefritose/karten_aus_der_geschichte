import requests
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from tasks.last_scraped_episode_date import last_scraped_episode_date
from tasks.scrape_feed import scrape_feed
from tasks.clean_push_episodes import clean_push_episodes
from tasks.extract_and_link_locations import extract_and_link_locations
from tasks.get_coordinates_for_locations import get_coordinates_for_locations


default_args = {
    'owner': 'marcose',
    'retries': 5,
    'retry_delay': timedelta(minutes=5),
}


with DAG(
    dag_id='kag_scraper_dag_v1',
    start_date=datetime(2023, 5, 16),
    schedule_interval='@daily',
    catchup=False
) as dag:
    # 0. Create Tables if not exist
    create_tables = PostgresOperator(
        task_id='postgres_create',
        postgres_conn_id='postgres_be',
        sql="sql/create_db.sql"
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

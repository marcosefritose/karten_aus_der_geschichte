from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.decorators import task
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.param import Param


from tasks.last_scraped_episode_date import last_scraped_episode_date
from tasks.scrape_feed import scrape_feed
from tasks.clean_push_episodes import clean_push_episodes
from tasks.extract_and_link_locations import extract_and_link_locations
from tasks.get_coordinates_for_locations import get_coordinates_for_locations
from tasks.get_country_continent_for_locations import get_country_continent_for_locations
from tasks.gpt_extract import gpt_extract

default_args = {
    'owner': 'marcose',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='kag_scraper_dag_v2',
    start_date=datetime(2023, 5, 16),
    schedule_interval='@daily',
    catchup=False,
    default_args=default_args,
    params={
        'premium': True,
        'default_finish_status': Param('active', type='string')
    }
) as dag:
    @task.branch(task_id='branch_task')
    def branch_func(**kwargs):
        # return premium task if premium parameter exists and is True
        if kwargs['params']['premium']:
            return 'gpt_api_extract'
        else:
            return 'extract_locations'

    branching = branch_func()

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

    # 4. Extract, link and save locations using spacy
    extract_locations = PythonOperator(
        task_id="extract_locations",
        python_callable=extract_and_link_locations,
        trigger_rule=TriggerRule.NONE_FAILED
    )

    # 5. Extract locations, topics, contexts and coordinates using openAI API
    gpt_api_extract = PythonOperator(
        task_id="gpt_api_extract",
        python_callable=gpt_extract
    )

    # 6. Get coordinates for location string
    get_coordinates = PythonOperator(
        task_id="get_coordinates",
        python_callable=get_coordinates_for_locations,
        trigger_rule=TriggerRule.NONE_FAILED
    )

    # 7. Get continent and country for location string
    get_country_continent = PythonOperator(
        task_id="get_country_continent",
        python_callable=get_country_continent_for_locations,
        trigger_rule=TriggerRule.NONE_FAILED
    )

    # 8. Mark processed episodes as active
    mark_episodes_as_pending = PostgresOperator(
        task_id='mark_episodes_as_pending',
        postgres_conn_id='postgres_be',
        sql="sql/mark_episodes_as_pending.sql",
        params={
            'status': dag.params['default_finish_status']
        }
    )

    create_tables >> get_last_scraped_episode_date >> scrape_episodes >> clean_episodes >> branching

    branching >> gpt_api_extract >> extract_locations >> get_coordinates
    branching >> extract_locations >> get_coordinates

    get_coordinates >> get_country_continent >> mark_episodes_as_pending

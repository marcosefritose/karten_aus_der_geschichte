from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'marcose',
    'retries': 5,
    'retry_delay': timedelta(minutes=5)
}

def read_feed():
    import feedparser
    feed_url = "https://geschichten-aus-der-geschichte.podigee.io/feed/mp3"
    episode_feed = feedparser.parse(feed_url)
    
    print(episode_feed)

with DAG(
    dag_id='gag_scraper_dag_v1',
    start_date=datetime(2022, 12, 29),
    schedule_interval='@daily'
) as dag:
    task_1 = PythonOperator(
        task_id='feed_reader',
        python_callable=read_feed
    )
    
    task_1

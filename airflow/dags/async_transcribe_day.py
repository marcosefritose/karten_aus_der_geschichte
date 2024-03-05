import asyncio
import aiohttp
import os
import base64

import pendulum
from airflow import DAG
from airflow.decorators import task_group
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.hooks.S3_hook import S3Hook
from airflow.operators.python_operator import ShortCircuitOperator
from airflow.utils.trigger_rule import TriggerRule



from airflow.providers.http.hooks.http import HttpAsyncHook
from huggingface_hub import get_inference_endpoint
from helpers.shared import (
    start_endpoint, 
    stop_endpoint,
    cleanup_xcom_of_previous_tasks
)


DAG_ID = "transcribe_async_dag_v2"
HF_API_TOKEN = os.environ['HF_API_TOKEN']

BATCH_SIZE = 7
PARALLEL_TASKS = 2
PARALLEL_REQUESTS = 3

sem = asyncio.Semaphore(PARALLEL_REQUESTS)


def new_transcriptions() -> None:
        print("Checking new episodes to transcribe exist")
        postgres_sql = PostgresHook(
            postgres_conn_id='vercel_db', schema='verceldb')
        conn = postgres_sql.get_conn()
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT COUNT(*) FROM podcasts_episode 
                    WHERE do_transcribe = true AND transcribed = false
                        """)
        result = cursor.fetchone()
        
        if result[0] > 0:
            print(f"{result[0]} episodes to transcribe")
            return True
        else:
            print("No episodes to transcribe")
            return False
        
def read_episodes():
        postgres_sql = PostgresHook(
            postgres_conn_id='vercel_db', schema='verceldb')
        
        episode_df = postgres_sql.get_pandas_df("SELECT id, feed_id, podcast_id, audio_url FROM podcasts_episode WHERE do_transcribe = true AND transcribed = false")
        episodes_data = episode_df.to_dict(orient='records')
        
        # Split the dataframe into chunks of 5
        episode_chunks = [
            {'batch': episodes_data[x:x+BATCH_SIZE]} for x in range(0, len(episodes_data), BATCH_SIZE)]
        
        return episode_chunks
    
def upload_to_s3(episode_data) -> None:
    for episode in episode_data:
        response = episode['response']
        podcast_id = episode['podcast_id']
        episode_id = episode['episode_id']
        feed_id = episode['feed_id']
    
        print(f"Uploading to S3 {episode_id}")
        hook = S3Hook('podiverse-transcripts')
        
        hook.load_string(
            string_data=response,
            key=f'{podcast_id}/{feed_id}.json',
            bucket_name="podiverse-transcripts",
            replace=True
        )
    
        mark_transcribed(episode_id)
    
def mark_transcribed(id) -> None:
    print("Marking episodes as transcribed")
    postgres_sql = PostgresHook(
            postgres_conn_id='vercel_db', schema='verceldb')
    conn = postgres_sql.get_conn()
    cursor = conn.cursor()
    cursor.execute("""
                UPDATE podcasts_episode
                SET transcribed = true
                WHERE id = %s
                    """, [id])
    conn.commit()
    cursor.close()
    conn.close()

async def inference_call(client, url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as response:
            episode_file = await response.read()

    base64_encoded_data = base64.b64encode(episode_file)
    base64_output = base64_encoded_data.decode('utf-8')
    #data = {"inputs": "", "audio_data": base64_output, "options": {"return_timestamps": True}}
    data = {"inputs": "", "audio_data": base64_output, "options": {"return_timestamps": False}}
    print("Transcribing episode: ", url)
    response = await client.post(json=data)
    json_str = response.decode('utf-8')
    return json_str

async def transcribe_audio(client, audio_url, id, podcast_id, feed_id):
    async with sem:
        retries = 4
        for attempt in range(retries):
            try:
                response = await inference_call(client, audio_url)
                print("Transcribed episode: ", feed_id, audio_url)
                return {'podcast_id': podcast_id, 'episode_id': id, 'feed_id': feed_id, 'response': response}
            except Exception as e: # Catch any exception that occurs during inference_call
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1: # If it's not the last attempt, wait a bit before retrying
                    print(f"Retrying in {5 ** (attempt +1)} seconds")
                    await asyncio.sleep(5 ** (attempt +1)) # Exponential backoff
                else:
                    print("All retries failed.")
                    # ToDO Customize Error Message
                    raise e
        
        return {'podcast_id': podcast_id, 'episode_id': id, 'feed_id': feed_id, 'response': response}
    
    
        
def _make_api_request_for_batch(batch, **context):
    endpoint = get_inference_endpoint('whisper-large-v3', token=HF_API_TOKEN)
    client = endpoint.async_client
    
    loop = asyncio.get_event_loop()
    coroutines = []

    for episode in batch:
        audio_url = episode['audio_url']
        id = episode['id']
        podcast_id = episode['podcast_id']
        feed_id = episode['feed_id']

        coroutines.append(transcribe_audio(client, audio_url, id, podcast_id, feed_id))
    print("Starting coroutines")
    data = loop.run_until_complete(asyncio.gather(*coroutines))

    return data


with DAG(
    dag_id=DAG_ID,
    start_date=pendulum.now(),
    schedule="0 * * * *",
    description="This DAG demonstrates collecting weather data for multiple cities using dynamic task mapping over task group",
    render_template_as_native_obj=True,
    tags=["airflow2.5", "task mapping", "asyncio"],
    
):
    check_db = ShortCircuitOperator(
        task_id='check_db',
        python_callable=new_transcriptions,
        provide_context=True,
    )
    
    start_hf = PythonOperator(
        task_id="start_endpoint",
        python_callable=start_endpoint
    )
    
    read_data = PythonOperator(
        task_id="read_data",
        python_callable=read_episodes,
    )

    @task_group(group_id="http_handling")
    def my_group(episodes_data):
        make_batch_http_requests = PythonOperator(
            task_id="make_batch_http_requests",
            python_callable=_make_api_request_for_batch,
            op_kwargs=episodes_data,
            max_active_tis_per_dag=PARALLEL_TASKS,
            retries= 3,
            retry_delay=pendulum.duration(seconds=5),
        )
        
        store_to_s3 = PythonOperator(
            task_id="store_to_temp",
            python_callable=upload_to_s3,
            op_kwargs={
                "episode_data": make_batch_http_requests.output
            },
            on_success_callback=cleanup_xcom_of_previous_tasks,
        )

        make_batch_http_requests >> store_to_s3

    stop_hf = PythonOperator(
        task_id="stop_endpoint",
        python_callable=stop_endpoint,
        trigger_rule=TriggerRule.ALL_DONE
    )
    
    mapped_groups = my_group.expand(episodes_data=read_data.output)

    check_db >> [start_hf, read_data] >> mapped_groups >> stop_hf
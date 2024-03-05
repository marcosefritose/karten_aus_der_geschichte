import os
import time

from airflow.models import XCom
from airflow.utils.session import provide_session
from sqlalchemy import and_, delete

from huggingface_hub import get_inference_endpoint

HF_API_TOKEN = os.environ['HF_API_TOKEN']

def start_endpoint() -> None:
        print("Starting Hugging Face Inference Endpoint")
        endpoint = get_inference_endpoint('whisper-large-v3', token=HF_API_TOKEN)

        if endpoint.status == "paused":
            print("Resuming endpoint")
            endpoint.resume()

        if endpoint.status != "running":
            print("Waiting for the endpoint to start. Currently in status: ", endpoint.status)
            endpoint.wait()
            print("Endpoint started. Wait 20 seconds for the endpoint to be fully ready")
            time.sleep(20)
            
def stop_endpoint() -> None:
    print("Stopping Hugging Face Inference Endpoint")
    endpoint = get_inference_endpoint('whisper-large-v3', token=HF_API_TOKEN)
    endpoint.pause()
    
@provide_session
def cleanup_xcom_dag(context, session=None):
    dag_run = context["dag_run"]
    dag_id = dag_run.dag_id
    run_id = dag_run.run_id

    delete_q = delete(XCom).filter(and_(XCom.dag_id == dag_id, XCom.run_id == run_id))

    session.execute(delete_q)

def cleanup_xcom_of_previous_tasks(context):
    dag_run = context["dag_run"]
    task_instance = context["ti"]

    task = context["task"]

    task_instances = [
        dag_run.get_task_instance(tid, map_index=task_instance.map_index)
        for tid in task.upstream_task_ids
    ]

    for ti in task_instances:
        if ti is not None:
            ti.clear_xcom_data()
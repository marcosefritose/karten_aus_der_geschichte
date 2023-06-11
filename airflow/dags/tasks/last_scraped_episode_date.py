from airflow.hooks.postgres_hook import PostgresHook
from datetime import datetime, timedelta


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

    # Set last_date to 3 months ago
    last_date = datetime.now() - timedelta(days=90)
    last_date = last_date.strftime("%Y-%m-%d")

    ti.xcom_push(key="last_scraped_date", value=last_date)

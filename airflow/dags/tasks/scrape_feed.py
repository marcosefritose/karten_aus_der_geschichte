from airflow.hooks.postgres_hook import PostgresHook


def scrape_feed(ti):
    import feedparser
    import pandas as pd

    # Download and parse the feed
    feed_url = "https://geschichten-aus-der-geschichte.podigee.io/feed/mp3"
    episode_feed = feedparser.parse(feed_url)

    # Create a dataframe with the relevant information
    df = pd.DataFrame(episode_feed['entries'])
    df['key'] = df['title']
    df = df[['key', 'title', 'subtitle', 'summary', 'published', 'link', 'image']]
    df['published'] = pd.to_datetime(df['published'], errors='coerce')

    df['image'] = df['image'].astype(str).str.replace('\'', '"')

    # Remove episodes that are already in the database
    last_scraped_episode_date = ti.xcom_pull(
        task_ids='get_last_scraped_episode', key='last_scraped_date')
    if last_scraped_episode_date:
        df = df[df.published > last_scraped_episode_date]

    episode_list = list(df.itertuples(index=False, name=None))

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')
    postgres_sql.insert_rows('episodes_raw', episode_list,
                             replace=True, replace_index="id",
                             target_fields=['key', 'title', 'subtitle', 'summary', 'published', 'link', 'image'])

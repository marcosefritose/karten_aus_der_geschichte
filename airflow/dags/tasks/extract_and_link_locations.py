from airflow.hooks.postgres_hook import PostgresHook


def extract_and_link_locations():
    import spacy

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')

    episode_df = postgres_sql.get_pandas_df(
        "SELECT id, summary, title, subtitle FROM episodes_target WHERE status = 'preprocessed' AND is_spacy_integrated = false")

    episode_df['text'] = episode_df['title'] + ' ' + \
        episode_df['subtitle'] + ' ' + episode_df['summary']
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

    locations_names = locations.keys()
    locations_tup = [tuple([loc, 'spacy']) for loc in locations_names]

    postgres_sql.insert_rows('locations', locations_tup,
                             target_fields=['name', 'origin'],
                             replace=True, replace_index='name')

    locations_df = postgres_sql.get_pandas_df(
        "SELECT id, name FROM locations")

    for loc, ep_ids in locations.items():
        # get location id by name and parse numpy.int64 to int
        location_id = locations_df[locations_df['name']
                                   == loc]['id'].astype(int).values[0]
        location_id = int(location_id)
        ep_ids = list(set(ep_ids))

        episodes_locations_tup = [
            tuple([ep_id, location_id]) for ep_id in ep_ids]
        postgres_sql.insert_rows('episodes_locations', episodes_locations_tup,
                                 target_fields=['episode_id', 'location_id'],
                                 replace=True, replace_index=['episode_id', 'location_id'])

    # Set status flag "is_spacy_integrated" of processed episodes to true
    for ep_id in episode_df['id']:
        postgres_sql.run(
            f"UPDATE episodes_target SET is_spacy_integrated = true WHERE id = {ep_id}")

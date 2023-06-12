from airflow.hooks.postgres_hook import PostgresHook


def get_address_from_coordinates(reverse_geocode, latitude, longitude):
    response = reverse_geocode((latitude, longitude))

    if not response or not response.raw:
        return None

    response_raw = response.raw

    if response_raw and 'country_code' in response_raw['address']:
        return response_raw['address']['country_code']

    return None


def generate_update_query(locations_data):
    update_query = "UPDATE locations SET country = x.country, continent = x.continent FROM (VALUES "

    for location_data in locations_data:
        update_query += f"({location_data[0]}, '{location_data[1]}', '{location_data[2]}'),"

    update_query = update_query[:-1]
    update_query += ") AS x(id, country, continent) WHERE x.id = locations.id"

    return update_query


def get_country_continent_for_locations():
    import pandas as pd
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    continent_mapping_file_path = '/opt/airflow/dags/data/continents.csv'

    geolocator = Nominatim(user_agent="kag")
    reverse_geocode = RateLimiter(
        geolocator.reverse, min_delay_seconds=1.1, max_retries=5)

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')

    # Get all locations joined with only the first active coordinate related to them
    locations_df = postgres_sql.get_pandas_df(
        "SELECT l.id, l.name, c.longitude, c.latitude FROM locations l LEFT JOIN coordinates c ON l.id = c.location_id WHERE c.status = 'active'")

    # Drop all duplicate locations by their IDs
    locations_df = locations_df.drop_duplicates(subset=['id'])
    locations_ids = locations_df['id'].tolist()

    # Get the country for each location by their longitude and latitude values
    locations_df['country_code'] = locations_df.apply(
        lambda row: get_address_from_coordinates(reverse_geocode, row['latitude'], row['longitude']), axis=1
    )

    # Drop all locations with no country_code
    locations_df = locations_df[locations_df['country_code'].notnull()]

    continents_df = pd.read_csv(continent_mapping_file_path)

    continents_df = continents_df.rename(columns={'alpha-2': 'country_code'})
    continents_df['country_code'] = continents_df['country_code'].str.lower()

    locations_df = locations_df.merge(
        continents_df, on='country_code', how='left')

    locations_df = locations_df.rename(
        columns={'region': 'continent', 'country_code': 'country'})

    locations_df = locations_df[['id', 'country', 'continent']]

    update_data = [(row[0], row[1], row[2])
                   for row in locations_df.itertuples(index=False, name=None)]

    # Generate update querries in chunks of 100
    for i in range(0, len(update_data), 100):
        update_query = generate_update_query(update_data[i:i+100])
        postgres_sql.run(update_query)

    # Update "is_country_continent_integrated" flag for processed location ids
    postgres_sql.run(f"""
        UPDATE locations
        SET is_country_continent_integrated = true
        WHERE id IN ({','.join(str(id) for id in locations_ids)})
    """)

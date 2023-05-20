from airflow.hooks.postgres_hook import PostgresHook


def get_coordinates_for_locations():
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')

    # Get all locations where no coordinaes that were found by spacy are available
    locations_df = postgres_sql.get_pandas_df(
        "SELECT id, name FROM locations WHERE id NOT IN (SELECT location_id FROM coordinates WHERE origin = 'Nominatim')")

    geolocator = Nominatim(user_agent="karten_aus_der_geschichte")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    locations_df['coordinates'] = locations_df['name'].apply(geocode)

    coordinates_df = locations_df[locations_df['coordinates'].notnull()][[
        'id', 'coordinates']]

    coordinates_df = coordinates_df.rename(columns={'id': 'location_id'})

    coordinates_df['longitude'] = coordinates_df['coordinates'].apply(
        lambda loc: loc.longitude if loc else None)
    coordinates_df['latitude'] = coordinates_df['coordinates'].apply(
        lambda loc: loc.latitude if loc else None)
    coordinates_df['origin'] = 'Nominatim'

    # Todo: Get default service used for geocoding from config
    coordinates_df['status'] = 'active'

    target_df = coordinates_df[['location_id', 'status',
                                'longitude', 'latitude', 'origin']]
    coordinates_values = list(target_df.itertuples(index=False, name=None))

    postgres_sql.insert_rows('coordinates', coordinates_values,
                             target_fields=list(target_df.columns))

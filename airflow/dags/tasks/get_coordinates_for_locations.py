from airflow.hooks.postgres_hook import PostgresHook


def get_coordinates_for_locations():
    from geopy.geocoders import Nominatim
    from geopy.extra.rate_limiter import RateLimiter

    postgres_sql = PostgresHook(
        postgres_conn_id='postgres_be', schema='kag')

    # Get all locations where no coordinaes that were found by Nominatim API are available and join with related coordinates
    locations_df = postgres_sql.get_pandas_df("""
        SELECT locations.id, locations.name, coordinates.id AS coordinate_id
        FROM locations 
        LEFT JOIN coordinates ON locations.id = coordinates.location_id
        WHERE locations.id NOT IN (SELECT location_id FROM coordinates WHERE origin = 'Nominatim') 
        AND is_coordinate_integrated = false
    """)

    locations_df['has_coordinate'] = locations_df['coordinate_id'].notnull()
    locations_df = locations_df.drop_duplicates(subset=['name'])
    locations_ids = locations_df['id'].tolist()

    geolocator = Nominatim(user_agent="karten_aus_der_geschichte")
    geocode = RateLimiter(geolocator.geocode,
                          min_delay_seconds=1.1, max_retries=5)

    print("Getting coordinates for locations", flush=True)
    locations_df['coordinates'] = locations_df['name'].apply(
        geocode)

    coordinates_df = locations_df[locations_df['coordinates'].notnull()][[
        'id', 'coordinates', 'has_coordinate']]

    coordinates_df = coordinates_df.rename(columns={'id': 'location_id'})

    coordinates_df['longitude'] = coordinates_df['coordinates'].apply(
        lambda loc: loc.longitude if loc else None)
    coordinates_df['latitude'] = coordinates_df['coordinates'].apply(
        lambda loc: loc.latitude if loc else None)
    coordinates_df['origin'] = 'Nominatim'

    print("Setting status for coordinates", flush=True)
    # Todo: Get default service used for geocoding from config
    selected_integration = 'GPT'
    # Set all coordinates to active if Nominatim is the configure service
    if selected_integration == 'Nominatim':
        coordinates_df['status'] = 'active'
    # Set only coordinate active if it is the first coordinate for a location
    else:
        coordinates_df['status'] = coordinates_df.apply(
            lambda row: 'inactive' if row['has_coordinate'] else 'active', axis=1)

    target_df = coordinates_df[['location_id', 'status',
                                'longitude', 'latitude', 'origin']]
    coordinates_values = list(target_df.itertuples(index=False, name=None))

    print(
        f'Inserting {len(coordinates_values)} coordinates into database', flush=True)
    postgres_sql.insert_rows('coordinates', coordinates_values,
                             target_fields=list(target_df.columns),
                             replace=False, replace_index=['location_id', 'longitude', 'latitude'])

    if len(locations_ids) != 0:
        print(f'Updating {len(locations_ids)} locations in database', flush=True)
        # Update status flag "is_coordinate_integrated" for processed locations
        postgres_sql.run(f"""
            UPDATE locations
            SET is_coordinate_integrated = true
            WHERE id IN ({','.join(str(id) for id in locations_ids)})
        """)

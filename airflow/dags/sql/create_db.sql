
-- Create database
CREATE TABLE IF NOT EXISTS episodes_raw (
    id SERIAL PRIMARY KEY,
    key VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    subtitle VARCHAR,
    summary VARCHAR NOT NULL,
    link VARCHAR NOT NULL,
    image VARCHAR,
    published TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS episodes_target (
    id SERIAL PRIMARY KEY,
    key VARCHAR NOT NULL UNIQUE,
    status VARCHAR DEFAULT 'preprocessed',
    title VARCHAR NOT NULL,
    subtitle VARCHAR,
    summary VARCHAR NOT NULL,
    link VARCHAR NOT NULL,
    image VARCHAR,
    thumbnail VARCHAR,
    published DATE,
    story_time_start INT,
    story_time_end INT,
    story_time_description VARCHAR,
    is_gpt_integrated BOOLEAN DEFAULT FALSE,
    is_spacy_integrated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    name VARCHAR NOT NULL UNIQUE,
    continent VARCHAR,
    country VARCHAR,
    origin VARCHAR,
    is_coordinate_integrated BOOLEAN DEFAULT FALSE,
    is_country_continent_integrated BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS coordinates (
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'hidden',
    longitude VARCHAR,
    latitude VARCHAR,
    origin VARCHAR,
    location_id INT REFERENCES locations(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

ALTER TABLE coordinates DROP CONSTRAINT IF EXISTS unique_location_coordinates;
ALTER TABLE coordinates ADD CONSTRAINT unique_location_coordinates UNIQUE (location_id, longitude, latitude);


CREATE TABLE IF NOT EXISTS episodes_locations(
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    context VARCHAR,
    episode_id INT REFERENCES episodes_target(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    location_id INT REFERENCES locations(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

ALTER TABLE episodes_locations DROP CONSTRAINT IF EXISTS unique_episode_location_combination;
ALTER TABLE episodes_locations ADD CONSTRAINT unique_episode_location_combination UNIQUE (episode_id, location_id);

CREATE TABLE IF NOT EXISTS topics(
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    name VARCHAR NOT NULL UNIQUE,
    origin VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS episodes_topics(
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    context VARCHAR,
    episode_id INT REFERENCES episodes_target(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    topic_id INT REFERENCES topics(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

ALTER TABLE episodes_topics DROP CONSTRAINT IF EXISTS unique_episode_topic_combination;
ALTER TABLE episodes_topics ADD CONSTRAINT unique_episode_topic_combination UNIQUE (episode_id, topic_id);
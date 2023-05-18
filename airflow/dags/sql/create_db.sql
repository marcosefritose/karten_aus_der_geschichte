
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
    key VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'pending',
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS locations (
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    name VARCHAR NOT NULL,
    continent VARCHAR,
    country VARCHAR,
    origin VARCHAR,
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

CREATE TABLE IF NOT EXISTS episodes_locations(
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    context VARCHAR,
    episode_id INT REFERENCES episodes_target(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    location_id INT REFERENCES locations(id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE IF NOT EXISTS topics(
    id SERIAL PRIMARY KEY,
    status VARCHAR DEFAULT 'active',
    name VARCHAR NOT NULL,
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
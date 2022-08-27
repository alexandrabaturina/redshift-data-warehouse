import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

ARN = config.get('IAM_ROLE', 'ARN')

LOG_DATA = config.get('S3','LOG_DATA')
LOG_JSONPATH = config.get('S3', 'LOG_JSONPATH')
SONG_DATA = config.get('S3', 'SONG_DATA')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create = """
    CREATE TABLE IF NOT EXISTS staging_events (
        artist VARCHAR,
        auth VARCHAR,
        first_name VARCHAR,
        gender CHAR(1),
        item_in_session INT,
        last_name VARCHAR,
        length FLOAT,
        level VARCHAR,
        location VARCHAR,
        method VARCHAR,
        page VARCHAR,
        registration BIGINT,
        session_id INT,
        song VARCHAR,
        status INT,
        ts TIMESTAMP,
        user_agent VARCHAR,
        user_id INT);
"""

staging_songs_table_create = """
    CREATE TABLE IF NOT EXISTS staging_songs (
        num_songs INT,
        artist_id CHAR(18),
        artist_latitude FLOAT,
        artist_longitude FLOAT,
        artist_location VARCHAR,
        artist_name VARCHAR,
        song_id CHAR(18),
        title VARCHAR,
        duration FLOAT,
        year INT);
"""

songplay_table_create = """
    CREATE TABLE IF NOT EXISTS songplays (
        songplay_id INT IDENTITY(0,1) PRIMARY KEY,
        start_time TIMESTAMP NOT NULL,
        user_id INT NOT NULL,
        level VARCHAR NOT NULL,
        song_id CHAR(18),
        artist_id CHAR(18) NOT NULL,
        session_id INT NOT NULL,
        location VARCHAR NOT NULL,
        user_agent VARCHAR NOT NULL);
"""

user_table_create = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INT NOT NULL PRIMARY KEY,
        first_name VARCHAR,
        last_name VARCHAR,
        gender CHAR(1),
        level VARCHAR);
"""

song_table_create = """
    CREATE TABLE IF NOT EXISTS songs (
        song_id CHAR(18) NOT NULL PRIMARY KEY,
        title VARCHAR NOT NULL,
        artist_id CHAR(18) NOT NULL,
        year int NOT NULL,
        duration FLOAT NOT NULL);
"""

artist_table_create = """
    CREATE TABLE IF NOT EXISTS artists (
        artist_id CHAR(18) NOT NULL PRIMARY KEY,
        name VARCHAR NOT NULL,
        location VARCHAR,
        latitude FLOAT,
        longitude FLOAT);
"""

time_table_create = """
    CREATE TABLE IF NOT EXISTS time (
        start_time TIMESTAMP NOT NULL PRIMARY KEY,
        hour INT,
        day INT,
        week INT,
        month INT,
        year INT,
        weekday INT);
"""

# STAGING TABLES

staging_events_copy = ("""
    copy staging_events from {}
    credentials 'aws_iam_role={}'
    region 'us-west-2'
    json {}
    timeformat 'epochmillisecs'
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs from {}
    credentials 'aws_iam_role={}'
    json 'auto'
    region 'us-west-2'
""").format(SONG_DATA, ARN)

# FINAL TABLES

songplay_table_insert = """
    INSERT INTO songplays (
        start_time,
        user_id,
        level,
        song_id,
        artist_id,
        session_id,
        location,
        user_agent)
    SELECT
        se.ts,
        se.user_id,
        se.level,
        ss.song_id,
        ss.artist_id,
        se.session_id,
        se.location,
        se.user_agent
    FROM staging_events se
    JOIN staging_songs ss
    ON (se.song = ss.title AND se.artist = ss.artist_name)
    AND se.page = 'NextSong'
"""

user_table_insert = """
    INSERT INTO users (
        user_id,
        first_name,
        last_name,
        gender,
        level)
    SELECT
        user_id,
        first_name,
        last_name,
        gender,
        level
    FROM staging_events
    WHERE user_id IS NOT NULL
"""

song_table_insert = """
    INSERT INTO songs (
        song_id,
        title,
        artist_id,
        year,
        duration)
    SELECT
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs
    WHERE song_id IS NOT NULL
"""

artist_table_insert = """
    INSERT INTO artists (
        artist_id,
        name,
        location,
        latitude,
        longitude)
    SELECT
        artist_id,
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
"""

time_table_insert = """
    INSERT INTO time (
        start_time,
        hour, 
        day,
        week,
        month,
        year,
        weekday)
    SELECT
        ts,
        EXTRACT (HOUR FROM ts),
        EXTRACT (DAY FROM ts),
        EXTRACT (WEEK FROM ts),
        EXTRACT (MONTH FROM ts),
        EXTRACT (YEAR FROM ts),
        EXTRACT (DAYOFWEEK from ts)
    FROM staging_events
    WHERE ts IS NOT NULL
"""

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]

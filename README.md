# Data Engineering ND #3: Data Warehouse
## Overview
**Data Warehouse** is the third project of Udacity [Data Engineering Nanodegree](https://d20vrrgs8k4bvw.cloudfront.net/documents/en-US/Data+Engineering+Nanodegree+Program+Syllabus.pdf). The goal of the project is to work with data warehouses and [AWS](https://aws.amazon.com/). It requires to build an [ETL](https://en.wikipedia.org/wiki/Extract,_transform,_load) pipeline that:
* Extracts music streaming data from [Amazon S3](https://aws.amazon.com/s3/) buckets
* Stages extracted data in [Redshift](https://aws.amazon.com/redshift/)
* Transforms data into a set of dimensional tables for analytics team
## Repo Contents
The repo contains the following files:
* ```create_tables.py```: drops existing tables and creates new ones.
* ```etl.py```: loads data from S3 to Redshift staging tables, and inserts extracted data into analytics tables.
* ```sql_queries.py```: contains all SQL queries.
## Database
### Database Purpose
A music streaming startup, *Sparkify*, wants to move their processes and data onto the cloud. They need a set of dimensional tables for their analytics team to find insights in what songs their users are listening to. 
### Project Datasets
*Sparkify* data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.
#### Song Dataset ```s3://udacity-dend/song_data```
The first dataset is a subset of real data from the [Million Song Dataset](http://millionsongdataset.com/). Each file is in JSON format and contains metadata about a song and the artist of that song. 

Below is an example of what a single song file ```data/song_data/A/A/B/TRAABJV128F1460C49.json``` looks like.
```
{
  "num_songs": 1, 
  "artist_id": "ARIK43K1187B9AE54C", 
  "artist_latitude": null, 
  "artist_longitude": null, 
  "artist_location": "Beverly Hills, CA", 
  "artist_name": "Lionel Richie", 
  "song_id": "SOBONFF12A6D4F84D8", 
  "title": "Tonight Will Be Alright", 
  "duration": 307.3824, 
  "year": 1986
}
```
#### Log Dataset ```s3://udacity-dend/log_data```
Log data json path: ```s3://udacity-dend/log_json_path.json```.

This dataset consists of log files in JSON format generated by [eventsim](https://github.com/Interana/eventsim) event simulator based on the songs in the song dataset. These simulate activity logs from a music streaming app based on specified configurations.

Below is an example of what a single line of a single file ```data/log_data/2018/11/2018-11-09-events.json``` looks like.
```
{
  "artist":"Beastie Boys",
  "auth":"Logged In",
  "firstName":"Harper",
  "gender":"M",
  "itemInSession":2,
  "lastName":"Barrett",
  "length":161.56689,
  "level":"paid",
  "location":"New York-Newark-Jersey City, NY-NJ-PA",
  "method":"PUT",
  "page":"NextSong",
  "registration":1540685364796.0,
  "sessionId":275,
  "song":"Lighten Up",
  "status":200,
  "ts":1541722186796,
  "userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"",
  "userId":"42"
}
```
## Database Design
### Step 1: Staging Tables
On step 1, data is loaded from S3 into two staging tables.
#### ```staging_events``` table
The ```staging_event``` table has the following fields:
* artist: VARCHAR
* auth: VARCHAR
* first_name: VARCHAR
* gender: CHAR(1)
* item_in_session: INT
* last_name: VARCHAR
* length: FLOAT
* level: VARCHAR
* location: VARCHAR
* method: VARCHAR
* page: VARCHAR
* registration: BIGINT
* session_id: INT
* song: VARCHAR
* status: INT
* ts: TIMESTAMP
* user_agent: VARCHAR
* user_id: INT
#### ```staging_songs``` table
The ```staging_songs``` table has the following fields:
* num_songs: INT
* artist_id: CHAR(18)
* artist_latitude: FLOAT
* artist_longitude: FLOAT
* artist_location: VARCHAR
* artist_name: VARCHAR
* song_id: CHAR(18)
* title: VARCHAR
* duration: FLOAT
* year: INT
### Step 2: Analytics Tables
The database for analytics team contains the following tables:
* Fact table
    * **songplays**: records in log data associated with song plays, i.e. records with page NextSong
* Dimension tables
    * **users**: users in the app
    * **songs**: songs in music database
    * **artists**: artists in music database
    * **time**: timestamps of records in songplays broken down into specific units
    
The database schema is shown below. Primary and foreign keys are marked as ```PK``` and ```FK```, respectively.
![image](https://user-images.githubusercontent.com/53233637/187318753-c965452d-65ac-47b6-bcba-c34c623f989e.png)

## Getting Started
### Prerequisites
To run ETL, it's required to launch a Redshift cluster and create an IAM role that has read access to S3. The data should be saved in ```dwh.cfg``` file. Below is an example of what ```dwh.cfg``` looks like.
```
[CLUSTER]
HOST=YOUR_HOST
DB_NAME=YOUR_DATABASE_NAME
DB_USER=YOUR_DATABASE_USER
DB_PASSWORD=YOUR_DATABASE_PASSWORK
DB_PORT=YOUR_DATABASE_PORT

[IAM_ROLE]
ARN=YOUR_IAM_ROLE

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```
### Running ETL Locally
To run ETL locally,
1. Clone this repo.
2. ```cd``` into project directory.
3. Put ```dwh.cfg``` into project directory.
4. Run ```create_tables.py``` to reset tables.
```
root@1a2dc16602ee:/home/workspace# python create_tables.py 
Tables are dropped.
Tables are created.
```
> Remember to run create_tables.py every time before running etl.py to reset tables.
5. Run ```etl.py```. Query execution progress is displayed in terminal.
```
root@1a2dc16602ee:/home/workspace# python etl.py
Loading staging tables...
Query 1 of 2 executed.
Query 2 of 2 executed.
Insert data into analytics tables...
Query 1 of 5 executed.
Query 2 of 5 executed.
Query 3 of 5 executed.
Query 4 of 5 executed.
Query 5 of 5 executed.
```
## Authors
[Alexandra Baturina](https://www.linkedin.com/in/alexandrabaturina/)

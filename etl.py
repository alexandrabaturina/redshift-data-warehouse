import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    print('Loading staging tables...')
    total = len(copy_table_queries)
    count = 0

    for query in copy_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
        count += 1
        print(f"Query {count} of {total} executed.")


def insert_tables(cur, conn):
    print('Insert data into analytics tables...')
    total = len(insert_table_queries)
    count = 0

    for query in insert_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
        count += 1
        print(f"Query {count} of {total} executed.")


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
        .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

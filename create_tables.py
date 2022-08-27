import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Function to drop each table using queries in drop_table_queries list.

    Args:
        cur (refcursor): Cursor to execute database queries
        conn (object): Database connection object
    Returns:
        no value
    """
    for query in drop_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
    print('Tables are dropped.')


def create_tables(cur, conn):
    """
    Function to create each table using queries in create_table_queries list.

    Args:
        cur (refcursor): Cursor to execute database queries
        conn (object): Database connection object
    Returns:
        no value
    """
    for query in create_table_queries:
        try:
            cur.execute(query)
            conn.commit()
        except Exception as e:
            print(e)
    print('Tables are created.')


def main():
    """
    Function to parse dwh.cfg file, establish connection to the database,
    drop existing tables, and create new ones.

    Args:
        no value
    Returns:
        no value
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}"
                            .format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()

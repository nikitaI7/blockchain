import psycopg2
from psycopg2 import OperationalError


def create_connection(db, user, user_password, db_host):
    print(db,user,user_password)
    connection = None
    try:
        connection = psycopg2.connect(
            database=db,
            user=user,
            password=user_password,
            host=db_host,
            port="5432",
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

from database import create_connection
from tables import a,b
import os


def main():
    conn = create_connection(os.getenv("name"), os.getenv("user"), os.getenv("password"), "database")
    cur = conn.cursor()
    cur.execute(a)
    conn.commit()
    cur = conn.cursor()
    cur.execute(b)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    main()

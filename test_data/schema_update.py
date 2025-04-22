from pathlib import Path

from pymysql import connect
from pymysql.cursors import DictCursor

from chat_api.dependencies import get_settings


def get_connection():
    settings = get_settings()
    conn = connect(
        host=settings.mysql_host,
        user=settings.mysql_user,
        password=settings.mysql_password,
        database=settings.mysql_database,
        port=settings.mysql_port,
        autocommit=True,
        cursorclass=DictCursor,
    )
    conn.ping(reconnect=True)
    try:
        yield conn
    finally:
        conn.close()


def run_queries(data: str):
    queries = data.split(";")
    print(queries)
    for conn in get_connection():
        with conn.cursor() as cur:
            for query in queries:
                print("query to be processed:", query)
                if not query:
                    continue
                cur.execute(query)
    print("done with queries")


def read_file(file_name: str):
    schema_file = Path(__file__).parents[1] / "chat_api" / "schema" / file_name
    if not schema_file.exists():
        raise FileNotFoundError("provided file not found")
    with schema_file.open() as f:
        return f.read()


def load_query(file_name: str):
    queries = read_file(file_name)
    run_queries(queries)


def main():
    files = [
        "user_schema.sql",
        "message_schema.sql",
    ]
    for file in files:
        print(f"loading data from {file}")
        load_query(file)


if __name__ == "__main__":
    main()

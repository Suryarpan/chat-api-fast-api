from typing import Any, Sequence

from pymysql import Connection, connect
from pymysql.cursors import DictCursor

from chat_api.config import Settings


class MysqlDB:
    conn: Connection[DictCursor] | None = None

    def __init__(self, setting: Settings):
        self.config: dict[str, Any] = {
            "host": setting.mysql_host,
            "user": setting.mysql_user,
            "password": setting.mysql_password,
            "database": setting.mysql_database,
            "port": setting.mysql_port,
        }
        self._connect()

    def _connect(self):
        if self.conn is None:
            self.conn = connect(**self.config, cursorclass=DictCursor, autocommit=False)
        self.conn.ping(reconnect=True)

    async def read(self, query: str, data: dict[str, Any]):
        self._connect()
        assert self.conn is not None
        with self.conn.cursor() as cur:
            cur.execute(query, data)
            result = cur.fetchall()
        return result

    async def insert(self, query: str, data: Sequence[dict[str, Any]]):
        if len(data) == 0:
            raise ValueError("no data to insert")
        self._connect()
        assert self.conn is not None
        try:
            self.conn.begin()
            with self.conn.cursor() as cur:
                if len(data) == 1:
                    ins_rows = cur.execute(query, data[0])
                else:
                    ins_rows = cur.executemany(query, data)
                result = (ins_rows, cur.lastrowid)
        except:
            self.conn.rollback()
            return (None, 0)
        else:
            self.conn.commit()
        return result

    async def upd_del(self, query: str, data: dict[str, Any]):
        if len(data) == 0:
            raise ValueError("no data to modify")
        self._connect()
        assert self.conn is not None
        try:
            self.conn.begin()
            with self.conn.cursor() as cur:
                result = cur.execute(query, data)
        except:
            self.conn.rollback()
            result = 0
        else:
            self.conn.commit()
        return result

    def close(self):
        if self.conn is not None:
            self.conn.close()
        self.conn = None

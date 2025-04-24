from contextlib import contextmanager
from queue import Empty, Full, Queue, ShutDown
from typing import Any, Sequence

from pymysql import Connection, connect
from pymysql.cursors import DictCursor

from chat_api.config import Settings


class MysqlDB:
    con_queue: "Queue[Connection[DictCursor]]"
    config: dict[str, Any]

    def __init__(self) -> None:
        pass

    def setup(self, setting: Settings):
        self.con_queue = Queue(maxsize=setting.mysql_pool)
        self.config: dict[str, Any] = {
            "host": setting.mysql_host,
            "user": setting.mysql_user,
            "password": setting.mysql_password,
            "database": setting.mysql_database,
            "port": setting.mysql_port,
        }
        self._connect()

    def _connect(self) -> None:
        for _ in range(self.con_queue.maxsize):
            conn = connect(**self.config, cursorclass=DictCursor, autocommit=False)
            try:
                self.con_queue.put_nowait(conn)
            except Full:
                conn.close()
                break
        return

    @contextmanager
    def get_con(self):
        conn = self.con_queue.get(block=True)
        conn.ping(reconnect=True)

        yield conn

        try:
            self.con_queue.put(conn)
        except ShutDown:
            conn.close()

    async def read(self, query: str, data: dict[str, Any]):
        with self.get_con() as conn, conn.cursor() as cur:
            cur.execute(query, data)
            result = cur.fetchall()

        return result

    async def insert(self, query: str, data: Sequence[dict[str, Any]]):
        if len(data) == 0:
            raise ValueError("no data to insert")

        with self.get_con() as conn:
            try:
                conn.begin()
                with conn.cursor() as cur:
                    if len(data) == 1:
                        ins_rows = cur.execute(query, data[0])
                    else:
                        ins_rows = cur.executemany(query, data)
                    result = (ins_rows, cur.lastrowid)
            except:
                conn.rollback()
                result = (None, 0)
            else:
                conn.commit()
        return result

    async def upd_del(self, query: str, data: dict[str, Any]):
        if len(data) == 0:
            raise ValueError("no data to modify")
        with self.get_con() as conn:
            try:
                conn.begin()
                with conn.cursor() as cur:
                    result = cur.execute(query, data)
            except:
                conn.rollback()
                result = 0
            else:
                conn.commit()
        return result

    def close(self):
        self.con_queue.shutdown()
        while True:
            try:
                conn = self.con_queue.get_nowait()
                conn.close()
            except Empty:
                break

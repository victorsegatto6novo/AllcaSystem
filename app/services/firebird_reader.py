from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

import fdb


@dataclass
class FirebirdConfig:
    dsn: str
    user: str
    password: str
    charset: str = "UTF8"


class FirebirdEventReader:
    """
    Conector para leitura de eventos no banco receptorip.fdb.

    Ajuste a query em `read_events_since` para refletir seu schema real.
    """

    def __init__(self, config: FirebirdConfig):
        self.config = config

    def _connect(self):
        return fdb.connect(
            dsn=self.config.dsn,
            user=self.config.user,
            password=self.config.password,
            charset=self.config.charset,
        )

    def read_events_since(self, since: datetime) -> Iterable[dict]:
        query = """
            SELECT CLIENT_CODE, EVENT_CODE, PARTITION, ZONE, DESCRIPTION, CREATED_AT
            FROM EVENTS
            WHERE CREATED_AT > ?
            ORDER BY CREATED_AT ASC
        """
        with self._connect() as conn:
            cur = conn.cursor()
            cur.execute(query, (since,))
            for row in cur.fetchall():
                yield {
                    "client_code": row[0],
                    "event_code": row[1],
                    "partition": row[2],
                    "zone": row[3],
                    "message": row[4],
                    "created_at": row[5],
                    "source": "receptor_ip",
                }

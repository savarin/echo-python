import datetime as dt
import sys
from typing import List

from alembic.config import Config
import alembic
import sqlalchemy

import echo_log_entity
import echo_models


class EchoLogStore:
    URL: str = "sqlite:///echo.db"

    @staticmethod
    def connect() -> sqlalchemy.orm.Session:
        engine = sqlalchemy.create_engine(EchoLogStore.URL)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        return Session()

    @staticmethod
    def migrate() -> None:
        alembic_cfg = Config("alembic.ini")
        alembic.command.upgrade(alembic_cfg, "head")

    @staticmethod
    def insert(log_entity: echo_log_entity.EchoLogEntity) -> None:
        session: sqlalchemy.orm.Session = EchoLogStore.connect()

        try:
            log_record = log_entity.to_record()
            session.add(log_record)
            session.commit()
        finally:
            session.close()

    @staticmethod
    def fetch_records() -> List[echo_models.EchoLog]:
        session: sqlalchemy.orm.Session = EchoLogStore.connect()

        try:
            return session.query(echo_models.EchoLog).all()
        finally:
            session.close()

    @staticmethod
    def get_all() -> List[echo_log_entity.EchoLogEntity]:
        return [
            echo_log_entity.EchoLogEntity.from_record(record)
            for record in EchoLogStore.fetch_records()
        ]

    @staticmethod
    def print_logs() -> None:
        for record in EchoLogStore.fetch_records():
            print(
                f"ID: {record.id}, Message: {record.message}, Created At: {record.created_at}"
            )


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        EchoLogStore.migrate()

    else:
        EchoLogStore.insert(
            echo_log_entity.EchoLogEntity(
                "id1",
                "Hello, World!",
                dt.datetime.now(dt.timezone.utc),
            )
        )
        EchoLogStore.print_logs()

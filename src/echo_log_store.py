import datetime as dt
import sys

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
    def print_logs() -> None:
        session: sqlalchemy.orm.Session = EchoLogStore.connect()

        try:
            for record in session.query(echo_models.EchoLog).all():
                print(
                    f"ID: {record.id}, Message: {record.message}, Created At: {record.created_at}"
                )
        finally:
            session.close()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "migrate":
        EchoLogStore.migrate()

    else:
        EchoLogStore.insert(
            echo_log_entity.EchoLogEntity(
                "id1",
                "Hello, World!",
                dt.datetime.strptime("2023-08-18 10:30:00", "%Y-%m-%d %H:%M:%S"),
            )
        )
        EchoLogStore.print_logs()

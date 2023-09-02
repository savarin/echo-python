from typing import List
import datetime as dt
import sys

from alembic.config import Config
import alembic
import sqlalchemy

import echo_log_entity
import echo_models


class EchoLogStore:
    """
    Class responsible for database operations related to echo logs.
    Provides methods to perform migrations, insert records, and fetch records.
    Uses SQLite for storage.
    """

    # Database connection URL
    URL: str = "sqlite:///echo.db"

    @staticmethod
    def connect() -> sqlalchemy.orm.Session:
        """
        Establishes a connection to the SQLite database and returns a session.

        :return: SQLAlchemy Session object.
        """
        # Create SQLAlchemy engine
        engine = sqlalchemy.create_engine(EchoLogStore.URL)

        # Create session factory bound to this engine
        Session = sqlalchemy.orm.sessionmaker(bind=engine)

        return Session()

    @staticmethod
    def migrate() -> None:
        """
        Executes database migration to the latest version using Alembic.
        """
        # Configure Alembic settings
        alembic_cfg = Config("alembic.ini")

        # Perform migration to latest version
        alembic.command.upgrade(alembic_cfg, "head")

    @staticmethod
    def insert(log_entity: echo_log_entity.EchoLogEntity) -> None:
        """
        Inserts a log entity into the database.

        :param log_entity: The EchoLogEntity object to insert.
        """
        # Establish database session
        session = EchoLogStore.connect()

        try:
            # Convert log entity to a database record
            log_record = log_entity.to_record()

            # Add record to the session
            session.add(log_record)

            # Commit transaction
            session.commit()
        finally:
            # Close the session
            session.close()

    @staticmethod
    def fetch_records() -> List[echo_models.EchoLog]:
        """
        Fetches all echo log records from the database.

        :return: List of EchoLog records.
        """
        # Establish database session
        session = EchoLogStore.connect()

        try:
            # Query all records and return
            return session.query(echo_models.EchoLog).all()
        finally:
            # Close the session
            session.close()

    @staticmethod
    def get_all() -> List[echo_log_entity.EchoLogEntity]:
        """
        Retrieves all log entities from the database and converts them to EchoLogEntity objects.

        :return: List of EchoLogEntity objects.
        """
        return [
            echo_log_entity.EchoLogEntity.from_record(record)
            for record in EchoLogStore.fetch_records()
        ]

    @staticmethod
    def print_logs() -> None:
        """
        Prints all echo logs in a human-readable format.
        """
        for record in EchoLogStore.fetch_records():
            print(
                f"ID: {record.id}, Message: {record.message}, Created At: {record.created_at}"
            )


if __name__ == "__main__":
    """
    Entry point for the script.
    If 'migrate' is passed as a command-line argument, database migrations will be performed.
    Otherwise, an example record will be inserted, and all records will be printed.
    """
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

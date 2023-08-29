import sqlite3


from alembic.config import Config
import alembic


class EchoLogStore:
    URL: str = "echo.db"

    @staticmethod
    def connect() -> sqlite3.Connection:
        return sqlite3.connect(EchoLogStore.URL)

    @staticmethod
    def migrate() -> None:
        alembic_cfg = Config("alembic.ini")
        alembic.command.upgrade(alembic_cfg, "head")

    @staticmethod
    def insert_log(id: str, message: str, created_at: str) -> None:
        with EchoLogStore.connect() as conn:
            conn.execute(
                """
            INSERT INTO echo_log (id, message, created_at) 
            VALUES (?, ?, ?)
            """,
                (id, message, created_at),
            )

    @staticmethod
    def print_logs() -> None:
        with EchoLogStore.connect() as conn:
            cursor: sqlite3.Cursor = conn.execute("SELECT * FROM echo_log")
            for record in cursor.fetchall():
                print(f"ID: {record[0]}, Message: {record[1]}, Created At: {record[2]}")


if __name__ == "__main__":
    EchoLogStore.migrate()
    EchoLogStore.insert_log("id1", "Hello, World!", "2023-08-18 10:30:00")
    EchoLogStore.print_logs()

import sqlite3


class EchoLogStore:
    URL: str = "echo.db"

    @staticmethod
    def connect() -> sqlite3.Connection:
        return sqlite3.connect(EchoLogStore.URL)

    @staticmethod
    def create_table() -> None:
        with EchoLogStore.connect() as conn:
            conn.execute(
                """
            CREATE TABLE IF NOT EXISTS echo_log (
                id VARCHAR(255) NOT NULL PRIMARY KEY,
                message VARCHAR(255) NOT NULL,
                created_at TIMESTAMP NOT NULL
            );
            """
            )

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
    EchoLogStore.create_table()
    EchoLogStore.insert_log("id1", "Hello, World!", "2023-08-18 10:30:00")
    EchoLogStore.print_logs()

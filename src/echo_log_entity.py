from typing import Optional
import dataclasses
import datetime as dt
import uuid

import echo_models


@dataclasses.dataclass
class EchoLogEntity:
    """
    Dataclass that represents an echo log entity.
    Each instance of this class will hold information for a single echo log,
    which includes its ID, the message, and when it was created.

    :param id: Unique identifier for the log.
    :param message: The message being logged.
    :param created_at: The datetime at which the log was created.
    """

    id: str
    message: str
    created_at: dt.datetime

    def to_record(self) -> echo_models.EchoLog:
        """
        Converts the EchoLogEntity to a database record using the EchoLog model.

        :return: A database record in the form of an EchoLog object.
        """
        # Create a new EchoLog record and populate its fields from this entity
        record = echo_models.EchoLog(
            id=self.id,
            message=self.message,
            created_at=self.created_at.astimezone(dt.timezone.utc),
        )

        # Assert that the record is an instance of EchoLog for type safety
        assert isinstance(record, echo_models.EchoLog)

        return record

    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        message: str = "",
        now: Optional[dt.datetime] = None,
    ) -> "EchoLogEntity":
        """
        Class method to create a new EchoLogEntity with optional parameters.

        :param id: Optional unique identifier. If not given, a UUID will be generated.
        :param message: The message to be logged.
        :param now: The datetime for the log. If not provided, the current time will be used.
        :return: A new EchoLogEntity instance.
        """
        # Generate a UUID if an ID is not provided
        if id is None:
            id = str(uuid.uuid4())

        # Use the current time if a datetime is not provided
        if now is None:
            now = dt.datetime.now(dt.timezone.utc)

        return cls(id=id, message=message, created_at=now)

    @classmethod
    def from_record(cls, record: echo_models.EchoLog) -> "EchoLogEntity":
        """
        Class method to create an EchoLogEntity from an EchoLog database record.

        :param record: The EchoLog database record.
        :return: A new EchoLogEntity with fields populated from the record.
        """
        # Create a new EchoLogEntity and populate its fields from the record
        return cls(
            id=str(record.id),
            message=str(record.message),
            created_at=record.created_at.replace(tzinfo=dt.timezone.utc),
        )

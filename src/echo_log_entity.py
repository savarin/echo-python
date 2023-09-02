from typing import Optional
import dataclasses
import datetime as dt

import uuid

import echo_models


@dataclasses.dataclass
class EchoLogEntity:
    id: str
    message: str
    created_at: dt.datetime

    def to_record(self) -> echo_models.EchoLog:
        record = echo_models.EchoLog(
            id=self.id,
            message=self.message,
            created_at=self.created_at.astimezone(dt.timezone.utc),
        )

        assert isinstance(record, echo_models.EchoLog)
        return record

    @classmethod
    def create(
        cls,
        id: Optional[str] = None,
        message: str = "",
        now: Optional[dt.datetime] = None,
    ) -> "EchoLogEntity":
        if id is None:
            id = str(uuid.uuid4())

        if now is None:
            now = dt.datetime.now(dt.timezone.utc)

        return cls(id=id, message=message, created_at=now)

    @classmethod
    def from_record(cls, record: echo_models.EchoLog) -> "EchoLogEntity":
        return cls(
            id=str(record.id),
            message=str(record.message),
            created_at=record.created_at.replace(tzinfo=dt.timezone.utc),
        )

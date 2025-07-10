from peewee import SqliteDatabase


db = SqliteDatabase('aqua_sense.db')

def init_db() -> None:
    db.connect()
    from om.infrastructure.models import PondRecord
    from om.infrastructure.models import FeedEvent
    from sdp.infrastructure.models import SchedulePlaning
    from iam.infrastructure.models import Device
    db.create_tables([Device, PondRecord, FeedEvent, SchedulePlaning], safe=True)
    db.close()
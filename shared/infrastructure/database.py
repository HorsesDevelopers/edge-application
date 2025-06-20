from peewee import SqliteDatabase


db = SqliteDatabase('aqua_sense.db')

def init_db() -> None:
    db.connect()
    from pond.infrastructure.models import PondRecord
    from feed.infrastructure.models import FeedEvent
    from iam.infrastructure.models import Device
    db.create_tables([Device, PondRecord, FeedEvent], safe=True)
    db.close()
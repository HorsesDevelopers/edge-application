from peewee import Model, AutoField, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db

class FeedEvent(Model):
    """
    ORM model representing a feed event in the database.
    Maps to the 'feed_events' table.
    """

    id = AutoField()
    device_id = CharField()
    dispensed_at = DateTimeField()
    duration = FloatField()

    class Meta:
        database = db
        table_name = 'feed_events'

class PondRecord(Model):
    """
    ORM model representing a pond sensor record in the database.
    Maps to the 'sensor_records' table.
    """
    id = AutoField()
    device_id = CharField()
    temp = FloatField()
    ph = FloatField()
    turbidity = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'sensor_records'

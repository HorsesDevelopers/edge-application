from peewee import Model, AutoField, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db

class FeedEvent(Model):

    id = AutoField()
    device_id = CharField()
    dispensed_at = DateTimeField()
    duration = FloatField()

    class Meta:
        database = db
        table_name = 'feed_events'

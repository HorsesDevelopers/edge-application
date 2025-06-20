from peewee import Model, AutoField, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db

class FeedEvent(Model):

    id = AutoField()
    device_id = CharField()
    duration = FloatField()
    dispensed_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'health_records'

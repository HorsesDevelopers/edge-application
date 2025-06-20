"""Peewee model for health records."""
from peewee import Model, AutoField, CharField, FloatField, DateTimeField
from shared.infrastructure.database import db

class PondRecord(Model):

    id = AutoField()
    device_id = CharField()
    record_type = CharField()
    value = FloatField()
    created_at = DateTimeField()

    class Meta:
        database = db
        table_name = 'sensor_records'

"""Peewee models for the IAM service."""
from peewee import Model, CharField, DateTimeField
from shared.infrastructure.database import db

class Device(Model):
    device_id   = CharField(primary_key=True)
    api_key     = CharField(null=True)
    created_at  = DateTimeField(null=True)

    class Meta:
        database    = db
        table_name  = 'devices'
from peewee import Model, AutoField, DateTimeField, FloatField
from shared.infrastructure.database import db

class SchedulePlaning(Model):
    """
    ORM model representing a schedule planning entry in the database.
    Maps to the 'schedules' table.
    """
    id = AutoField()  # Unique identifier for the schedule
    start_time = DateTimeField()  # Start time of the schedule
    duration = FloatField()  # Duration in seconds

    class Meta:
        database = db
        table_name = 'schedules'
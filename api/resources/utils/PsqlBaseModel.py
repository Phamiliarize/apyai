import config

from peewee import PostgresqlDatabase, Model

# Establish database connection
psql_db = PostgresqlDatabase(**config.database)

class PsqlBaseModel(Model):
    """A base model that will use our Postgresql database"""
    class Meta:
        database = psql_db


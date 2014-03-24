import os

from sqlalchemy import Table, MetaData, Column, ForeignKey, Integer, String, create_engine, Boolean
from sqlalchemy.orm import mapper, sessionmaker, relationship

from diopy.client.models import DiopyClient
from diopy.resources.models import Droplet, Region, Size, Image

def setup_backend(config=None):
    """Sets up SQLAlchemy backend and create the sqlalchemy tables for the diopy models (currently only SQLite).
    Requires the config to contain the following:
        'Database' settings block with:
            - file: The path to the database file, if not provided an in-memory sqlite dabatase will be used.
    """
    db_file_path = config['Database'].get('file_path', None)
    if not db_file_path:
        db_file_path = ":memory:"

    db_file_path = "sqlite:///{0}".format(db_file_path)


    db_engine = create_engine(db_file_path)
    Session = sessionmaker(bind=db_engine)
    db_session = Session()

    metadata = MetaData()

    # Define the tables for our models
    diopy_client_table = Table(
        'diopy_client', metadata,
        Column('id', Integer, primary_key=True),
        Column('client_id', String(50)),
        Column('api_key', String(50)),
    )

    droplet_table = Table(
        'droplet', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(30)),
        Column('api_key', String(30)),
        Column('size_id', ForeignKey('size.id')),
        Column('image_id', Integer),
        Column('client_id', Integer),
        Column('backups', String(30)),
        Column('locked', Boolean),
        Column('status', String(20)),
        Column('snapshots', String(30)),
        Column('event_id', Integer),
        Column('region_id', Integer),
        Column('ip_address', String(30)),
        Column('created_at', String(30)),
        Column('backups_active', Boolean),
        Column('private_ip_address', String(30)),
    )

    region_table = Table(
        'region', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(30)),
        Column('slug', String(30)),
    )

    size_table = Table(
        'size', metadata,
        Column('id', Integer, primary_key=True),
        Column('cpu', String(30)),
        Column('name', String(30)),
        Column('slug', String(30)),
        Column('disk', String(30)),
        Column('memory', String(30)),
        Column('cost_per_hour', String(30)),
        Column('cost_per_month', String(30)),
    )

    image_table = Table(
        'image', metadata,
        Column('id', Integer, primary_key=True),
        Column('name', String(30)),
        Column('slug', String(30)),
        Column('public', String(30)),
        Column('regions', String(30)),
        Column('distributions', String(30)),
        Column('region_slugs', String(30)),
    )

    # Don't forget to map the model to previously created table
    mapper(DiopyClient, diopy_client_table)
    mapper(Droplet, droplet_table)
    mapper(Region, region_table)
    mapper(Size, size_table, properties={
        'droplets': relationship(Droplet, backref='size')
    })
    mapper(Image, image_table)

    # Create all the tables
    metadata.create_all(db_engine)

    return db_session

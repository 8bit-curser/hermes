from os import environ
from uuid import uuid1

from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, Float,
                        ForeignKey, Integer, String, Text, UniqueConstraint,
                        create_engine, func)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker


engine = create_engine('postgresql://postgres@db/hermes')
session = scoped_session(sessionmaker(engine))


def generate_uuid():
    return uuid1().__str__()


class Base_(object):
    query = session.query_property()


Base = declarative_base(cls=Base_)


class Address(Base):
    __tablename__ = 'addresses'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)


class Country(Base):
    __tablename__ = 'countries'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)


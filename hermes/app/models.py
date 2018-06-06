from datetime import datetime
from os import environ
from uuid import uuid1

from sqlalchemy import (Boolean, Column, DateTime, Enum, Float,
                        ForeignKey, Integer, String,  UniqueConstraint,
                        create_engine, func)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, scoped_session, sessionmaker

from werkzeug.security import check_password_hash, generate_password_hash

from enums import UserTypeEnum


engine = create_engine(environ.get('SQLALCHEMY_DATABASE_URI'))
session = scoped_session(sessionmaker(engine))


def generate_uuid():
    """Obtain a UUID string."""
    return uuid1().__str__()


class Base_(object):
    query = session.query_property()


Base = declarative_base(cls=Base_)


class User(Base):
    """User table ORM representation."""

    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String)
    email = Column(String)
    category = Column(Enum(UserTypeEnum))
    UniqueConstraint(email)

    def is_authenticated(self):
        """Check if user is authenticated."""
        return True

    def is_active(self):
        """Check if user is active."""
        return True

    def is_anonymous(self):
        """Check if user is anonoymous."""
        return False

    def get_id(self):
        """Return users identification."""
        return str(self.email)

    def set_password(self, password):
        """Encrypt the user's password.
        Arguments:
        self -- the user instance
        password -- the password received from the form
        """
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Validate password.
        Arguments:
        self -- the user instance
        password -- the password received from the form
        """
        return check_password_hash(self.password, password)


class Country(Base):
    """Country ORM representation."""
    __tablename__ = 'countries'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    code = Column(Integer)


class Address(Base):
    """Address ORM representation."""
    __tablename__ = 'addresses'

    id = Column(String, primary_key=True, default=generate_uuid)
    country_id = Column(String, ForeignKey("countries.id"))
    country = relationship("Country")
    city = Column(String)
    area = Column(String)
    postal_code = Column(String)
    street = Column(String, nullable=False)
    street_num = Column(Integer)
    notes = Column(String)


class ItemType(Base):
    """Item Type ORM representation."""
    __tablename__ = 'item_types'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)


class Item(Base):
    """Item ORM representation."""
    __tablename__ = 'items'

    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String)
    amount = Column(Integer)
    price = Column(Float)
    type_id = Column(String, ForeignKey("item_types.id"))
    type = relationship("ItemType")
    provier_id = Column(String, ForeignKey("users.id"))
    provider = relationship("User")


class Request(Base):
    """Request ORM representation."""
    __tablename__ = 'requests'

    id = Column(String, primary_key=True, default=generate_uuid)
    active = Column(Boolean, default=True)
    amount = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)
    item_id = Column(String, ForeignKey("items.id"))
    item = relationship("Item")
    client_id = Column(String, ForeignKey("users.id"))
    client = relationship("User")


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

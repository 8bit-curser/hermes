from wtforms import (DecimalField, FloatField, Form, IntegerField, SelectField,
                     StringField, SubmitField, PasswordField, validators)
from wtforms_components import TimeField
from wtforms.fields.html5 import EmailField

from hermes.app.models import Item

USER_LEVEL = {
    'client': 'client',
    'provider': 'provider',
}

items = []
for item in Item.query.all():
    items.append((item.id, item.title))


class LoginForm(Form):
    """ Gives a form to login a user """
    email = EmailField('Email',)
    password = PasswordField('Password')
    submit = SubmitField('Login')


class SignUp(Form):
    """ Gives a form to sign up a user """
    email = EmailField('Email')
    name = StringField('First Name')
    lastname = StringField('Last Name')
    password = PasswordField('Password')
    role = SelectField('Type', choices=set(USER_LEVEL.items()))
    submit = SubmitField('Signup!')


class RequestForm(Form):
    """Make a request form."""
    choice = SelectField('Item', choices=items)
    amount = IntegerField('Amount', default=0)
    submit = SubmitField('Place order')

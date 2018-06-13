from wtforms import (DecimalField, FloatField, Form, IntegerField, SelectField,
                     StringField, SubmitField, PasswordField, validators)
from wtforms_components import TimeField
from wtforms.fields.html5 import EmailField

from hermes.app.models import Item, ItemType

USER_LEVEL = {
    'client': 'client',
    'provider': 'provider',
}

# FIXME: When an ItemType has been added it doesnt show on the ItemForm later

class LoginForm(Form):
    """Gives a form to login a user."""
    email = EmailField('Email',)
    password = PasswordField('Password')
    submit = SubmitField('Login')


class SignUp(Form):
    """Gives a form to sign up a user."""
    email = EmailField('Email')
    name = StringField('First Name')
    lastname = StringField('Last Name')
    password = PasswordField('Password')
    role = SelectField('Type', choices=set(USER_LEVEL.items()))
    submit = SubmitField('Signup!')


class RequestForm(Form):
    """Make a request form."""

    items = []
    for item in Item.query.all():
        items.append((item.id, item.title))

    choice = SelectField('Item', choices=items)
    amount = IntegerField('Amount', default=0)
    submit = SubmitField('Place order')


class ItemTypeForm(Form):
    """Add an item type."""
    title = StringField('Type')
    submit = SubmitField('Add the new type!')


class ItemForm(Form):
    """Add an Item registry."""

    item_types = []

    for type_ in ItemType.query.all():
        item_types.append((type_.id, type_.title))

    title = StringField('Title')
    amount = IntegerField('Amount', default=0)
    price = FloatField('Price', default=0.0)
    item_type = SelectField('Type', choices=item_types)
    submit = SubmitField('Add your item!')


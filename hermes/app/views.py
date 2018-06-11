from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)

from flask_login import current_user, login_required, login_user, logout_user

from hermes.app.enums import RequestStateEnum, UserTypeEnum
from hermes.app.forms import (ItemForm, ItemTypeForm, LoginForm, RequestForm,
                              SignUp)
from hermes.app.models import Item, ItemType, Request, User, session


@login_required
def index():
    """Index view."""
    return render_template('index.html', user=current_user)


@login_required
def items():
    """Items view."""
    items = Item.query.all()
    return render_template('items.html', items=items)


@login_required
def item(item_id):
    """Items detail view."""
    item = Item.query.get(item_id)
    return render_template('item.html', item=item)


@login_required
def add_item():
    """Add item registry view."""
    form = ItemForm(request.form)
    ret = None
    if request.method == 'GET':
        ret = render_template('item_form.html', form=form)
    else:
        if form.validate():
            item = Item(
                    title=form.title.data,
                    amount=form.amount.data,
                    price=form.price.data,
                    type_id=form.item_type.data,
                    provider_id=current_user.id)
            session.add(item)
            session.commit()
            flash('Your item has been added!')
            ret = redirect(url_for('item', item_id=item.id))
    return ret


@login_required
def add_item_type():
    """Add item type registry view."""
    form = ItemTypeForm(request.form)
    ret = None
    if request.method == 'GET':
        ret = render_template('item_type_form.html', form=form)
    else:
        if form.validate():
            item_type = ItemType(title=form.title.data)
            session.add(item_type)
            session.commit()
            flash('Your item type has been added!')
            ret = redirect(url_for('add_item'))
    return ret


@login_required
def providers():
    """Providers view."""
    providers = User.query.all()
    providers = [prov for prov in providers
                 if prov.category == UserTypeEnum.provider]
    return render_template('providers.html', providers=providers)


@login_required
def provider(provider_id):
    """Providers view."""
    provider = User.query.get(provider_id)
    items = Item.query.filter(Item.provider_id == provider_id)
    return render_template('provider.html', provider=provider, items=items)


@login_required
def requests():
    """Requests view."""
    form = RequestForm(request.form)
    ret = None
    if request.method == 'GET':
        ret = render_template('requests.html', form=form, user=current_user)
    else:
        if form.validate():
            request_ = Request(
                    item_id=form.choice.data,
                    client_id=current_user.id,
                    amount=form.amount.data,
                    state=RequestStateEnum.ready)
            session.add(request_)
            session.commit()
            if form.amount.data <= request_.item.amount:
                flash("Your order has been placed")
                request_.item.amount -= form.amount.data
                session.commit()
                from hermes.app.tasks import mail_send
                total_amount = form.amount.data * request_.item.price
                mail_send.delay("""Your order will arrive in an estimate of:{}
                                   The total to pay is: {}"""
                                .format(10, total_amount))
            else:
                flash("That amount excedes the one available for the item")
            ret = redirect(url_for('requests'))
    return ret


def login():
    """Log in a user."""
    form = LoginForm(request.form)
    title = 'Login'
    ret = None
    if request.method == 'GET':
        ret = render_template('login.html', form=form, title=title)
    else:
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None:
                if user.check_password(form.password.data):
                    login_user(user)
                    ret = redirect(url_for('index'))
                else:
                    flash("Incorrect password")
                    ret = redirect(url_for("login"))
            else:
                flash("Non existent user")
                ret = redirect(url_for("login"))
        else:
            ret = "form not validated"
    return ret


def signup():
    """Sign up a user."""
    form = SignUp(request.form)
    title = 'Registro'
    ret = None
    if request.method == 'GET':
        ret = render_template('signup.html', form=form, title=title)
    else:
        if form.validate():
            user = User(email=form.email.data,
                        name=form.name.data,
                        lastname=form.lastname.data,
                        category=form.role.data)
            user.set_password(form.password.data)
            session.add(user)
            session.commit()
            flash("User created succesfuly.")
            ret = redirect(url_for('index'))
        else:
            flash("There was an error creating the user.")
            ret = render_template('signup.html', form=form, title=title)

    return ret


@login_required
def logout():
    """Log out a user."""
    logout_user()
    flash("You been logged out!")
    return redirect(url_for('index'))

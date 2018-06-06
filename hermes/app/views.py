from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)

from flask_login import current_user, login_required, login_user, logout_user

from hermes.app.enums import UserTypeEnum
from hermes.app.forms import LoginForm, RequestForm, SignUp
from hermes.app.models import Item, Request, User, session
from hermes.app.tasks import test_task


@login_required
def index():
    """Index view."""
    test_task.delay()
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
def providers():
    """Providers view."""
    providers = User.query.all()
    current_app.logger.info(providers[1].category)
    current_app.logger.info(UserTypeEnum.provider)
    providers = [prov for prov in providers
                 if prov.category == UserTypeEnum.provider]
    return render_template('providers.html', providers=providers)


@login_required
def provider(provider_id):
    """Providers view."""
    provider = User.query.get(provider_id)
    items = Item.query.filter(Item.provier_id == provider_id)
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
                    amount=form.amount.data)
            session.add(request_)
            session.commit()
            flash("Your order has been placed")
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

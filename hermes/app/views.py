from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)

from flask_login import current_user, login_required, login_user, logout_user

from hermes.app.enums import RequestStateEnum, UserTypeEnum
from hermes.app.forms import (ItemForm, ItemTypeForm, LoginForm, RequestForm,
                              SignUp)
from hermes.app.models import Item, ItemType, Request, User, session


# FIXME: Only the user that created the item is the one that can edit or
# restock it
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
    reqs = Request.query.filter(Request.item_id == item_id,
                                Request.state == RequestStateEnum.sent).all()
    total_amounts = sum([req.amount for req in reqs])
    if total_amounts > 0:
        flash("Hey you need to restock this item for a min of {}"
              .format(str(total_amounts - item.amount)))

    return render_template('item.html', item=item, amount=total_amounts)


@login_required
def restock(item_id):
    item = Item.query.get(item_id)
    amount = int(request.args.get('amount', 0))
    reqs = Request.query.filter(Request.item_id == item_id,
                                Request.state == RequestStateEnum.sent).all()
    total_amounts = sum([req.amount for req in reqs])
    if (total_amounts - item.amount) > amount:
        flash('That amount is below the minimun!')
    else:
        item.amount += amount
        session.commit()
        flash('Your item has been restocked for {}'.format(amount))
        from hermes.app.tasks import update_item_after_restock, update_reqs
        update_item_after_restock.delay(item_id)

    return redirect(url_for('item', item_id=item_id))


@login_required
def add_item():
    """Add item  view."""
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
    # TODO: The email messages must be moved to constants
    form = RequestForm(request.form)
    ret = None
    if request.method == 'GET':
        ret = render_template('requests.html', form=form, user=current_user)
    else:
        from hermes.app.tasks import mail_send
        if form.validate():
            request_ = Request(
                item_id=form.choice.data,
                client_id=current_user.id,
                amount=form.amount.data,
                state=RequestStateEnum.ready)
            session.add(request_)
            session.commit()
            flash("Your order has been placed")
            total_amount = form.amount.data * request_.item.price
            if form.amount.data <= request_.item.amount:
                request_.item.amount -= form.amount.data
                request_.state = RequestStateEnum.done
                session.commit()
            else:
                min_amnt = form.amount.data - request_.item.amount
                # This mail goes to the provider
                mail_send.delay(
                    """An order has been placed that excedes the amount of
                    items currently available for {}, a minimun of that amount
                    extra is required.
                    For item {}""".format(str(min_amnt), request_.item.title))
                request_.state = RequestStateEnum.sent
                session.commit()
            ret = redirect(url_for('requests'))
            # This mail goes to the user that required the product
            mail_send.delay(
                """Your order will arrive in an estimate of:{}
                   The total to pay is: {}""".format(10, total_amount))

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

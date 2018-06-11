from hermes.app.views import (add_item, add_item_type, index, item, items,
                              login, logout, provider, providers, requests,
                              signup)


def map_urls(app):
    """Url map function."""
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/items', view_func=items)
    app.add_url_rule('/items/add', view_func=add_item, methods=['GET', 'POST'])
    app.add_url_rule('/items/add/type/', view_func=add_item_type,
                     methods=['GET', 'POST'])
    app.add_url_rule('/items/<item_id>', view_func=item)
    app.add_url_rule('/providers', view_func=providers)
    app.add_url_rule('/providers/<provider_id>', view_func=provider)
    app.add_url_rule('/requests', view_func=requests, methods=['GET', 'POST'])
    app.add_url_rule('/requests/<id>', view_func=requests,
                     methods=['GET', 'POST'])
    app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)
    app.add_url_rule('/signup', view_func=signup, methods=['GET', 'POST'])

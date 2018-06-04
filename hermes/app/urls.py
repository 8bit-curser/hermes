from views import index, items, providers, requests, login, logout, signup


def map_urls(app):
    """Url map function."""
    app.add_url_rule('/', view_func=index)
    app.add_url_rule('/items', view_func=items)
    app.add_url_rule('/providers', view_func=providers)
    app.add_url_rule('/requests', view_func=requests, methods=['GET', 'POST'])
    app.add_url_rule('/login', view_func=login, methods=['GET', 'POST'])
    app.add_url_rule('/logout', view_func=logout)
    app.add_url_rule('/signup', view_func=signup, methods=['GET', 'POST'])

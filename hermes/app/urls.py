from views import index


def map_urls(app):
    """Url map function."""
    app.add_url_rule('/', view_func=index)

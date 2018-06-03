from flask import (abort, current_app, flash, redirect, render_template,
                   request, url_for)


def index():
    """Index view."""
    return render_template('index.html')
    

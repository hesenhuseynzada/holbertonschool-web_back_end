#!/usr/bin/env python3
""" Route module for the API - Infer appropriate time zone"""


from flask import Flask, request, render_template, g
from flask_babel import Babel
from os import getenv
import pytz
from typing import Union, Optional

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

app = Flask(__name__)


class Config(object):
    """ Babel configuration """
    LANGUAGES = ['en', 'fr']
    # these are the inherent defaults just btw
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# set the above class object as the configuration for the app
app.config.from_object('6-app.Config')


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """ GET /
    Return: 6-index.html
    """
    return render_template('6-index.html')


def get_user() -> Union[dict, None]:
    """ Returns user dict if ID can be found """
    if request.args.get('login_as'):
        # have to type cast  the param to be able to search the user dict
        user = int(request.args.get('login_as'))
        if user in users:
            return users.get(user)
    return None


@app.before_request
def before_request() -> None:
    """ Finds user and sets as global on flask.g.user """
    g.user = get_user()


def get_locale() -> Optional[str]:
    """ Determines best match for supported languages """
    # check if there is a locale parameter/query string
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    # check if there is a locale in an existing user's profile
    if g.user and g.user.get('locale') in app.config['LANGUAGES']:
        return g.user.get('locale')
    # default to return as a failsafe
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_timezone() -> Optional[str]:
    """ Determines best match for supported timezones """
    # check if there is a timezone parameter/query string
    tz = request.args.get('timezone')
    if tz:
        try:
            return pytz.timezone(tz).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    # check if there is a timezone in an existing user's profile
    if g.user and g.user.get('timezone'):
        try:
            return pytz.timezone(g.user.get('timezone')).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    # default to return as a failsafe
    return app.config['BABEL_DEFAULT_TIMEZONE']


babel = Babel(app, locale_selector=get_locale, timezone_selector=get_timezone)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

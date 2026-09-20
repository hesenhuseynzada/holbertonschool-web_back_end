#!/usr/bin/env python3
''' Flask app '''

from flask import Flask, request, render_template
from flask_babel import Babel

app = Flask(__name__)


class Config:
    ''' App config '''
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_locale():
    ''' return best languages '''
    locale = request.args.get('locale')
    if locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, locale_selector=get_locale)


@app.route("/", methods=["GET"], strict_slashes=False)
def hello_world():
    ''' return the template '''
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run()

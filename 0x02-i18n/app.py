#!/usr/bin/env python3
""" Basic babel setup"""


from flask import Flask, request, render_template, g
from flask_babel import Babel, gettext
from os import getenv

app = Flask(__name__)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config(object):
    """ configure babel """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)


@app.route('/', methods=['GET'], strict_slashes=False)
def index() -> str:
    """
    Return: 1-index.html
    """
    return render_template('6-index.html')


@babel.localeselector
def get_locale() -> str:
    """ Force Locale with URL parameter"""
    localLang = request.args.get('locale')
    supportLang = app.config['LANGUAGES']
    if localLang in supportLang:
        return localLang
    userId = request.args.get('login_as')
    if userId:
        localLang = users[int(userId)]['locale']
        if localLang in supportLang:
            return localLang
    localLang = request.headers.get('locale')
    if localLang in supportLang:
        return localLang
    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """ returns a user dictionary or None if not found"""
    try:
        userId = request.args.get('login_as')
        return users[int(userId)]
    except Exception:
        return None


@app.before_request
def before_request():
    """ use get_user to find a user if any"""
    g.user = get_user()
    utcNow = pytz.utc.localize(datetime.datetime.utcnow())
    local_time_now = utcNow.astimezone(pytz.timezone(get_timezone()))


@babel.timezoneselector
def get_timezone():
    """ Infer appropriate time zone """
    localTimezone = request.args.get('timezone')
    if localTimezone in pytz.all_timezones:
        return localTimezone
    else:
        raise pytz.exceptions.UnknownTimeZoneError
    userId = request.args.get('login_as')
    localTimezone = users[int(userId)]['timezone']
    if localTimezone in pytz.all_timezones:
        return localTimezone
    else:
        raise pytz.exceptions.UnknownTimeZoneError
    return app.config['BABEL_DEFAULT_TIMEZONE']


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)

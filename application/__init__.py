from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from application.userland.controller import mod_userland
from application.userland.controllers import home_controller, root_controller

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('./config/prp.cfg', silent=True)
    # app.config.from_pyfile('./config/dev.cfg', silent=True)
    # app.config.from_pyfile('./config/prod.cfg', silent=True)

    db.init_app(app)

    ma.init_app(app)

    class UrlSchemeDetector(object):
        def __init__(self, _app, prefered_scheme):
            self.app = _app
            self.preferred_scheme = prefered_scheme or 'http'

        def __call__(self, environ, start_response):
            environ['wsgi.url_scheme'] = self.preferred_scheme
            return self.app(environ, start_response)

    app.wsgi_app = UrlSchemeDetector(app.wsgi_app, app.config.get('PREFERRED_URL_SCHEME', 'https'))

    migrate.init_app(app, db)

    load_blueprints(app)

    from application.core.db_models import MobileApplication

    return app


def load_blueprints(app):
    from application.userland.controller import mod_userland
    from application.userland.controllers.root_controller import mod_userland as root_module
    from application.userland.controllers.home_controller import mod_userland as home_module
    from application.userland.controllers.app_controller import mod_userland as app_module

    app.register_blueprint(mod_userland)

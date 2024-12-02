import os

from flask import Flask

from instance import config

from werkzeug.middleware.proxy_fix import ProxyFix

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY=config.SECRET_KEY,
            DATABASE=os.path.join(app.instance_path, 'openbook.sqlite'),
            )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    # @app.route('/hello')
    # def hello():
        # return 'Hello, World!'

    from . import root
    app.register_blueprint(root.bp)
    # app.add_url_rule('/blog', endpoint='index')

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/blog', endpoint='index')

    # app.add_url_rule('/', endpoint='index')

    from . import games
    app.register_blueprint(games.bp)

    from . import user
    app.register_blueprint(user.bp)

    from . import playground
    app.register_blueprint(playground.bp)

    from . import league
    app.register_blueprint(league.bp)

    # from . import movies
    # app.register_blueprint(movies.bp)

    # from . import books
    # app.register_blueprint(books.bp)

    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    return app

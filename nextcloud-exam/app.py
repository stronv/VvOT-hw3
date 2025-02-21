from flask import Flask
from flask_apscheduler import APScheduler
from flask_mail import Mail

scheduler = APScheduler()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")

    scheduler.init_app(app)
    scheduler.start()
    mail.init_app(app)

    from views import deployer
    app.register_blueprint(deployer)

    return app

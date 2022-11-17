from flask import Flask


def create_app():
    app = Flask(__name__)

    from .controller import diagnose_controller
    app.register_blueprint(diagnose_controller.bp)

    return app

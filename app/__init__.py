from flask import Flask
from .controller import diagnose_controller


app = Flask(__name__)

app.register_blueprint(diagnose_controller.bp)

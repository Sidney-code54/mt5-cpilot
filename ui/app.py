from flask import Flask
from routes.ask_routes import ask_bp

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# Register blueprint
app.register_blueprint(ask_bp)

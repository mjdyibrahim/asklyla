from flask import Flask
from .modules.group.group import group_bp

app = Flask(__name__)
app.register_blueprint(group_bp)
# Import routes after creating app to avoid circular imports
from app.modules.event import event_routes
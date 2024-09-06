from flask import Flask

app = Flask(__name__)
# Import routes after creating app to avoid circular imports

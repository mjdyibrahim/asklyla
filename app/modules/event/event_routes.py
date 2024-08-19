from flask import Blueprint

event_routes = Blueprint('event_routes', __name__)

# Define your routes here
@event_routes.route('/some-event-route')
def some_event_function():
    # Your code here
    pass
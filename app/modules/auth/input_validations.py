from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    travel_from = DateField('Travel From', format='%Y-%m-%d', validators=[DataRequired()])
    travel_to = DateField('Travel To', format='%Y-%m-%d', validators=[DataRequired()])
    accommodation_type = SelectField('Accommodation Type', choices=[('hotel', 'Hotel'), ('airbnb', 'Airbnb')], validators=[DataRequired()])
    food_type = SelectField('Food Type', choices=[('vegetarian', 'Vegetarian'), ('vegan', 'Vegan'), ('gluten-free', 'Gluten-Free')], validators=[DataRequired()])
    activity_type = SelectField('Activity Type', choices=[('sightseeing', 'Sightseeing'), ('beach', 'Beach'), ('cultural', 'Cultural')], validators=[DataRequired()])
    transportation_type = SelectField('Transportation Type', choices=[('car', 'Car'), ('public', 'Public Transportation')], validators=[DataRequired()])
Then, in your get_bot_response function, you can create an instance of the form and validate the user input before storing it:

from .forms import UserForm

@app.route("/", methods=["POST"])
def get_bot_response():
    form = UserForm(request.form)
    if form.validate():
        # Store user information
        name = form.name.data
        email = form.email.data
        travel_from = form.travel_from.data
        travel_to = form.travel_to.data
        accommodation_type = form.accommodation_type.data
        food_type = form.food_type.data
        activity_type = form.activity_type.data
        transportation_type = form.transportation_type.data

        user_info = {
            "name": name,
            "contact_info": email,
            "travel_dates": {"from": travel_from, "to": travel_to},
            "preferences": {
                "accommodation_type": accommodation_type,
                "food_type": food_type,
                "activity_type": activity_type,
                "transportation_type": transportation_type
            },
            "itinerary": []
        }

        # Continue with chatbot logic
        ...
    else:
        # Handle validation errors
        errors = form.errors
        ...
# If any of the fields fail validation, the form.errors dictionary will contain the error messages for each field. You can then display these messages to the user and prompt them to correct their input.


from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField 
from wtforms.validators import DataRequired, Email, EqualTo

app.secret_key = 'your_secret_key'

class SignupForm(FlaskForm): 
    name = StringField('Name', validators=[DataRequired()]) 
    email = StringField('Email', validators=[DataRequired(), Email()]) 
    password = PasswordField('Password', validators=[DataRequired()]) 
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) 
    submit = SubmitField('Sign Up')

@app.route("/signup", methods=["GET", "POST"]) 
def signup(): 
    form = SignupForm() 
    if form.validate_on_submit(): # Store the user's information in a database or file 
        name = form.name.data 
        email = form.email.data 
        password = form.password.data # Add code to store the user's information in a database or file

    # Redirect the user to the home page
    return redirect(url_for('home'))

return render_template("signup.html", form=form)





from flask import Flask, render_template, request, jsonify, session, redirect, url_for from dotenv import load_dotenv import openai import os

# Next, we need to initialize the Flask app and set a secret key for the session:

app = Flask(name) app.secret_key = os.environ.get("SECRET_KEY")

Then, we need to create a login page where users can create an account or log in if they already have one:

@app.route("/login", methods=["GET", "POST"]) def login(): if request.method == "POST": # Check if the user is already registered email = request.form.get("email") password = request.form.get("password") user = get_user(email)

    if user and user["password"] == password:
        # Store the user in the session
        session["user"] = user
        return redirect(url_for("home"))
    else:
        # Display an error message
        error = "Invalid email or password"
        return render_template("login.html", error=error)

else:
    return render_template("login.html")
@app.route("/register", methods=["GET", "POST"]) def register(): if request.method == "POST": # Get the user's information from the form name = request.form.get("name") email = request.form.get("email") password = request.form.get("password")

    # Add the user to the database
    add_user(name, email, password)

    # Store the user in the session
    user = get_user(email)
    session["user"] = user

    return redirect(url_for("home"))

else:
    return render_template("register.html")
In the login function, we check if the user is already registered and if the password matches the email. If so, we store the user in the session and redirect them to the home page. If not, we display an error message.

In the register function, we get the user's information from the form, add them to the database, and store them in the session.

We also need to modify the get_bot_response function to check if the user is logged in before proceeding:

@app.route("/", methods=["POST"]) def get_bot_response(): if "user" not in session: # Redirect the user to the login page return redirect(url_for("login"))

name = request.form.get("name")
email = request.form.get("email")
travel_from = request.form.get("travel_from")
travel_to = request.form.get("travel_to")
accommodation_type = request.form.get("accommodation_type")
food_type = request.form.get("food_type")
activity_type = request.form.get("activity_type")
transportation_type = request.form.get("transportation_type")

# Rest of the code
Here, we check if the "user" key is in the session. If not, we redirect the user to the login page.

Finally, we need to modify the home function to display the appropriate page depending on whether the user is logged in:

@app.route("/") def home(): if "user" in session: return render_template("index.html") else: return redirect(url_for("login"))

In this function, we check if the "user" key is in the session. If so, we render the index.html template. If not, we redirect the user to the login page.

Overall, these modifications will help attract information from users and get them to create an account, creating a more complete app.

from flask import requests
import app
from functions import register, login

@app.route("/", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/register", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/login", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/recover_password", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/book-accommodation", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/confirm-booking", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/book-experience", methods=["POST"])
def onboarding():
    return onboarding(text)

@app.route("/budget", methods=["POST"]) 
@app.route("/itineraries", methods=["POST"])
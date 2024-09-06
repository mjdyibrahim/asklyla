from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    country = db.Column(db.String(100), nullable=False)
    population = db.Column(db.String(50))
    language = db.Column(db.String(100))
    currency = db.Column(db.String(100))
    time_zone = db.Column(db.String(100))
    emergency_number = db.Column(db.String(20))
    nearest_airport = db.Column(db.String(100))
    transportation = db.Column(db.String(2000))  # Adjust the length as needed
    
    # Attractions and Activities
    attractions = db.relationship('Attraction', backref='city', lazy=True)
    
    # Local Cuisine
    must_try_dishes = db.Column(db.String(1000))  # Store as comma-separated values
    
    # Recommended Restaurants
    recommended_restaurants = db.relationship('Restaurant', backref='city', lazy=True)
    
    # Shopping
    popular_districts = db.Column(db.String(1000))  # Store as comma-separated values
    souvenirs = db.Column(db.String(1000))  # Store as comma-separated values
    
    # Nightlife
    cafes_bars = db.Column(db.String(1000))  # Store as comma-separated values
    nightclubs = db.Column(db.String(1000))  # Store as comma-separated values
    
    # Safety Tips
    safety_tips = db.Column(db.String(2000))  # Store as comma-separated values
    
    # Local Etiquette
    etiquette = db.Column(db.String(2000))  # Store as comma-separated values
    
    # Weather
    climate = db.Column(db.String(200))
    average_temperature_spring = db.Column(db.String(20))
    average_temperature_summer = db.Column(db.String(20))
    average_temperature_autumn = db.Column(db.String(20))
    average_temperature_winter = db.Column(db.String(20))
    
    # Best Time to Visit
    best_time_to_visit = db.Column(db.String(200))
    
    # Helpful Phrases
    hello_phrase = db.Column(db.String(100))
    thank_you_phrase = db.Column(db.String(100))
    ask_directions_phrase = db.Column(db.String(100))
    ask_prices_phrase = db.Column(db.String(100))

class Attraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    opening_hours = db.Column(db.String(100))
    admission_fee = db.Column(db.String(100))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cuisine = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    contact_information = db.Column(db.String(100))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

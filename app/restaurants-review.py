@app.route("/review", methods=["POST"]) 

def add_review(): 
    restaurant_name = request.form.get("restaurant_name") 
    cuisine_type = request.form.get("cuisine_type") 
    rating = request.form.get("rating") 
    review = request.form.get("review") 
    image = request.files.get("image")

# Save the image to a folder and get the image path
image_path = save_image(image)

# Create a dictionary to store the review information
review_info = {
    "restaurant_name": restaurant_name,
    "cuisine_type": cuisine_type,
    "rating": rating,
    "review": review,
    "image_path": image_path
}

# Save the review to a database
save_review(review_info)

return jsonify({"message": "Review added successfully!"})
Helper function to save the image to a folder
def save_image(image): # Generate a unique filename for the image filename = secure_filename(image.filename) filename = str(uuid.uuid4()) + "_" + filename

# Save the image to a folder
image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

# Return the image path
return os.path.join(app.config["UPLOAD_FOLDER"], filename)
Helper function to save the review to a database
def save_review(review_info): # Save the review to a database # You can use a database of your choice, e.g. SQLite, MySQL, MongoDB, etc. # Here's an example using SQLite: conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("INSERT INTO reviews (restaurant_name, cuisine_type, rating, review, image_path) VALUES (?, ?, ?, ?, ?)", (review_info["restaurant_name"], review_info["cuisine_type"], review_info["rating"], review_info["review"], review_info["image_path"])) conn.commit() conn.close()

Add a route to display all the reviews
@app.route("/reviews") def show_reviews(): # Retrieve all the reviews from the database conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("SELECT * FROM reviews") reviews = c.fetchall() conn.close()

# Render the reviews template with the reviews data
return render_template("reviews.html", reviews=reviews)
Add a route to display a single review
@app.route("/reviews/int:review_id") def show_review(review_id): # Retrieve the review with the given ID from the database conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("SELECT * FROM reviews WHERE id=?", (review_id,)) review = c.fetchone() conn.close()

# Render the review template with the review data
return render_template("review.html", review=review)
Add a route to delete a review
@app.route("/reviews/int:review_id/delete", methods=["POST"]) def delete_review(review_id): # Delete the review with the given ID from the database conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("DELETE FROM reviews WHERE id=?", (review_id,)) conn.commit() conn.close()

return jsonify({"message": "Review deleted successfully!"})
Add a route to update a review
@app.route("/reviews/int:review_id/update", methods=["POST"]) def update_review(review_id): restaurant_name = request.form.get("restaurant_name") cuisine_type = request.form.get("cuisine_type") rating = request.form.get("rating") review = request.form.get("review") image = request.files.get("image")

# Save the image to a folder and get the image path
if image:
    image_path = save_image(image)
else:
    image_path = request.form.get("image_path")

# Update the review in the database
conn = sqlite3.connect("reviews.db")
c = conn.cursor()
c.execute("UPDATE reviews SET restaurant_name=?, cuisine_type=?, rating=?, review=?, image_path=? WHERE id=?", (restaurant_name, cuisine_type, rating, review, image_path, review_id))
conn.commit()
conn.close()

return jsonify({"message": "Review updated successfully!"})
Add a route to get all the restaurant types
@app.route("/restaurant_types") def get_restaurant_types(): # Retrieve all the restaurant types from the database conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("SELECT DISTINCT cuisine_type FROM reviews") restaurant_types = [row[0] for row in c.fetchall()] conn.close()

return jsonify({"restaurant_types": restaurant_types})
Add a route to get all the reviews for a specific restaurant type
@app.route("/reviews/string:restaurant_type") def get_reviews_by_restaurant_type(restaurant_type): # Retrieve all the reviews for the given restaurant type from the database conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("SELECT * FROM reviews WHERE cuisine_type=?", (restaurant_type,)) reviews = c.fetchall() conn.close()

# Render the reviews template with the reviews data
return render_template("reviews.html", reviews=reviews)
Add a route to get the average rating for a specific restaurant type
@app.route("/average_rating/string:restaurant_type") def get_average_rating_by_restaurant_type(restaurant_type): # Retrieve the average rating for the given restaurant type from the database conn = sqlite3.connect("reviews.db") c = conn.cursor() c.execute("SELECT AVG(rating) FROM reviews WHERE cuisine_type=?", (restaurant_type,)) average_rating = c.fetchone()[0] conn.close()

return jsonify({"average_rating": average_rating})
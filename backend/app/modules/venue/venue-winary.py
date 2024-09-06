import requests

@app.route("/recommend_winery", methods=["POST"])
def recommend_winery():
    location = request.form.get("location")
    wine_type = request.form.get("wine_type")
    price_range = request.form.get("price_range")

    # Use Yelp Fusion API to search for wineries and vineyards
    api_key = "YOUR_YELP_API_KEY"
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "location": location,
        "categories": "wineries, vineyards",
        "attributes": f"price_range:{price_range}",
        "term": wine_type
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Extract the relevant information from the API response
    businesses = data["businesses"]
    recommendations = []
    for business in businesses:
        name = business["name"]
        address = ", ".join(business["location"]["display_address"])
        rating = business["rating"]
        review_count = business["review_count"]
        url = business["url"]
        recommendations.append({
            "name": name,
            "address": address,
            "rating": rating,
            "review_count": review_count,
            "url": url
        })

    return jsonify({"recommendations": recommendations})
# In this implementation, we first retrieve the user's location, wine type, and price range preferences from the request data. We then use the Yelp API to search for wineries and vineyards that match those preferences. We pass in the user's location, wine type, and price range as parameters to the API request, and we also specify that we want businesses in the "wineries" and "vineyards" categories.

# Once we get the response from the API, we extract the relevant information (name, address, rating, review count, and URL) for each business and store it in a list of recommendations. We then return this list as a JSON response.

# Note that in order to use the Yelp Fusion API, you will need to obtain an API key from Yelp and replace "YOUR_YELP_API_KEY" in the code above with your actual API key.

# With this new route in place, we can now update the "get_bot_response" route to call the "/recommend_winery" route if the user's input includes a request for winery/vineyard recommendations. We can add the following code to the "get_bot_response" route:

if "winery" in user_response or "vineyard" in user_response:
    recommendations_response = requests.post(
        "http://localhost:5000/recommend_winery",
        data={
            "location": user_info["preferences"]["location"],
            "wine_type": user_info["preferences"]["wine_type"],
            "price_range": user_info["preferences"]["price_range"]
        }
    )
    recommendations = recommendations_response.json()["recommendations"]
    ai_response = "Here are some wineries and vineyards you might like:\n"
    for recommendation in recommendations:
        ai_response += f"{recommendation['name']} - {recommendation['address']}\n" \
                        f"Rating: {recommendation['rating']} ({recommendation['review_count']} reviews)\n" \
                        f"URL: {recommendation['url']}\n\n"
# This code checks if the user's input includes the words "winery" or "vineyard". If it does, we make a POST request to the "/recommend_winery" route, passing in the user's location, wine type, and price range preferences as data. We then extract the recommendations from the response and format them into a string that we can include in the AI's response.

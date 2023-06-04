   # Make request to ArtFairCalendar API
    url = f"https://www.artfaircalendar.com/api?key={ARTFAIR_API_KEY}&interests={interests}&location={location}"
    response = requests.get(url)
    data = response.json()

    # Extract list of recommended art fairs from API response
    recommended_fairs = []
    for fair in data["fairs"]:
        name = fair["name"]
        date = fair["date"]
        location = fair["location"]
        # Add more fields as desired

        # Create dictionary for each recommended fair
        recommended_fairs.append({
            "name": name,
            "date": date,
            "location": location,
            # Add more fields as desired
        })

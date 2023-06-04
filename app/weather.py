
Define a function get_alert_info that takes in the destination city and returns any active emergency alerts. You can use an API like the National Weather Service to get the alert information:

def get_alert_info(city):
    url = f'https://api.weather.gov/alerts/active?point=<LATITUDE>,<LONGITUDE>'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        alerts = []
        for alert in data['features']:
            alerts.append(alert['properties']['event'])
        return alerts
    else:
        return None
Modify the get_bot_response function to include the weather and alert information in the AI response. You can add the following code after the ai_response variable is assigned:

# Get weather and alert information for the destination
weather_info = get_weather_info(travel_to)
alert_info = get_alert_info(travel_to)

# Add weather and alert information to the AI response
if weather_info:
    ai_response += f" The current temperature in {travel_to} is {weather_info['temperature']} degrees and the forecast is {weather_info['description']}."
else:
    ai_response += " I'm sorry, I couldn't find weather information for your destination."

if alert_info:
    ai_response += f" There is currently an active emergency alert in {travel_to}: {', '.join(alert_info)}."
else:
    ai_response += " There are no active emergency alerts in your destination."
Replace <YOUR_API_KEY>, <LATITUDE>, and <LONGITUDE> with the appropriate values for your weather and alert APIs.

With these changes, your Flask app will now provide real-time updates on local weather and natural disasters in the user's destination as part of the AI response.

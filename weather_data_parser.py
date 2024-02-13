from datetime import datetime
import requests

# Function constants.
WEEK_DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
# Holds flag icon API country-code resolution json.
COUNTRY_CODES = {country: code for code, country in requests.get("https://flagcdn.com/en/codes.json").json().items()}
API_KEY = "DTJW3UL5K6Q6VDDKWACAT75XV"
API_ENDPOINT = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/" \
               f"timeline/ /next7days/?iconSet=icons2&unitGroup=metric&key={API_KEY}"
# Url for git with with weather icons. icon names appear in data response.
ICON_URL = "https://raw.githubusercontent.com/visualcrossing/WeatherIcons/main/PNG/2nd%20Set%20-%20Color/"


def parse_weather_data(country_city):
    """Receives city/country and calls weather forecast API.
    Returns formatted data from API."""

    data = requests.get(API_ENDPOINT.replace(" ", country_city))
    if data.status_code == 200:
        data = data.json()
        today = datetime.now().strftime("%A")
        # General location and current weather data
        w_data = {"country_city": data["resolvedAddress"],
                  "flag_code": None,
                  "description": data["description"],
                  "forecast": [],
                  "current": data["currentConditions"]}
        try:
            # Try to locate a flag icon from flags API.
            w_data["flag_code"] = COUNTRY_CODES[data["resolvedAddress"].split(", ")[1:3][1]]
        except Exception:
            pass

        # Populate forecast list with per-dat weather data
        for day in data["days"]:
            w_data["forecast"].append(
                {"day": WEEK_DAYS[(data["days"].index(day) + WEEK_DAYS.index(today)) % 7], #add week day
                 "date": "".join([i+"-" for i in day["datetime"].split("-")][::-1])[:-1], # reverse date representation
                 "day_temp": day["tempmax"],
                 "night_temp": day["tempmin"],
                 "humidity": day["humidity"],
                 "icon": f"{ICON_URL}{day['icon']}.png"})
        w_data["search_time"] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        return w_data
    # If request failed return None.
    return None


def get_current_location():
    """Gets client's current location based on I.P using a location API"""

    location_api_key = "f6af83bf995349fabcfc8edac805cd34"
    response = requests.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key={location_api_key}").json()
    try:
        return response["city"]
    except KeyError:
        return "Tel Aviv"

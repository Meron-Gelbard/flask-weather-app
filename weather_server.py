from flask import Flask, render_template, request, url_for, redirect, session, make_response, jsonify
from weather_data_parser import *
import json
import os

app = Flask(__name__)
app.secret_key = "secret..."  # Needed for the use of session variables.
BG_COLOR = os.getenv("BG_COLOR")


@app.route("/", methods=['GET'])
def home_redirect():
    return redirect("/home")


def update_history_json(new_data):
    if not os.path.exists("./history/weather_history.json"):
        history_data = [new_data]
        with open("./history/weather_history.json", 'w') as history_json:
            json.dump(history_data, history_json, indent=2)
    else:
        with open("./history/weather_history.json", 'r') as history_json:
            history_data = json.load(history_json)
        history_data.append(new_data)
        with open("./history/weather_history.json", 'w') as history_json:
            json.dump(history_data, history_json, indent=2)


@app.route("/home", methods=['GET', 'POST'])
def home():
    """Home page for sending weather forecast request"""
    # If request posted, redirect city/country parameter to weather checker page
    if request.method == "POST":
        country_city = request.form.get('city_country')
        return redirect(f"/weather_result/{country_city}")

    # If no request sent, check for errors and generate home page.
    location = get_current_location()
    w_data = parse_weather_data(location)
    if session.get("api_error"):
        # If error session var found, generate home with error, clear error var.
        error = session.get("api_error")
        session.clear()
        return render_template("index.html", w_data=w_data, location=location, error=error, bgcolor=BG_COLOR)
    else:
        # If no error and no request posted, generate regular home page.
        return render_template("index.html", w_data=w_data, location=location, bgcolor=BG_COLOR)


@app.route("/weather_result/", methods=['GET', 'POST'])
def empty_location():
    session["api_error"] = "Please enter a location."
    return redirect(url_for("home"))


@app.route("/weather_result/<country_city>", methods=['GET', 'POST'])
def weather_result(country_city):
    """Page that shows weather forecast result"""
    # takes search value and passes to weather data function
    w_data = parse_weather_data(country_city)
    if not w_data:
        # If data returns None, generate error session var and redirect to home.
        session["api_error"] = "Location not found."
        return redirect(url_for("home"))
    # If data is good, render result page with correct titles and data.
    # write result data to history json file
    update_history_json(w_data)
    title = f"{w_data['country_city']}"
    subtitle = f"Now: {w_data['description']}"
    return render_template("weather_forecast.html", country_city=country_city, w_data=w_data,
                           title=title, subtitle=subtitle, bgcolor=BG_COLOR)


@app.route("/history", methods=['GET'])
def history():
    try:
        with open("./history/weather_history.json", 'r') as json_file:
            history_data = json.load(json_file)
    except FileNotFoundError:
        history_data = [{"search_time": None, "country_city": None, "forecast": [{"night_temp": 0, "day_temp": 0}]}]
    return render_template("history.html", history=history_data, bgcolor=BG_COLOR)


@app.route('/download_history/<index>', methods=['GET'])
def download_json(index):

    with open("./history/weather_history.json", 'r') as json_file:
        history_data = json.load(json_file)

    json_str = jsonify(history_data[int(index)])
    response = make_response(json_str)
    response.headers['Content-Type'] = 'application/json'
    response.headers['Content-Disposition'] = 'attachment; filename=weather_forcast_data.json'
    return response


if __name__ == "__main__":
    app.run(port=8080, debug=True)

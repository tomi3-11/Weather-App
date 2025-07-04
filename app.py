from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv 

load_dotenv() # Load environment variables from .env

app = Flask(__name__)

API_KEY = os.getenv("API_KEY") # get key from .env


# Defining the / route
@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None
    
    if request.method == "POST":
        city = request.form.get("city", "").strip()
        
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"].title(),
                }
            else:
                error = data.get("message", "City not found. Please try again.")
        
    return render_template("index.html", weather=weather_data, error=error)


if __name__ == "__main__":
    app.run(debug=True)
    
    
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Azure Computer Vision API credentials
AZURE_ENDPOINT =("https://skyguardian-aiazure.cognitiveservices.azure.com/")
AZURE_KEY =("3WoULIpaWAl2aBzJl1yGeFA2D66mc5nhr9hXNDj4QJxOe6VOkQw5JQQJ99BCACYeBjFXJ3w3AAAFACOGewqE")

if not AZURE_ENDPOINT or not AZURE_KEY:
    raise ValueError("AZURE_ENDPOINT or AZURE_KEY is missing.")

AZURE_ANALYZE_URL = AZURE_ENDPOINT + "/vision/v3.2/analyze"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/meet/<character>")
def meet_character(character):
    messages = {
        "luma": "🌟 Luma: Hello, Guardian! Light pollution is a growing issue affecting our night skies...",
        "nox": "🌙 Nox: Greetings, traveler. Light pollution disrupts wildlife and wastes energy..."
    }
    return messages.get(character, "Error: Character not found!")

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"].read()

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }
    params = {"visualFeatures": "Categories,Description,Color"}

    response = requests.post(AZURE_ANALYZE_URL, headers=headers, params=params, data=image)
    result = response.json()

    categories = result.get("categories", [])
    description = result.get("description", {}).get("captions", [])

    pollution_level = "Unknown"
    for category in categories:
        name = category["name"]
        if "outdoor_" in name:
            pollution_level = "Low"
        elif "night_" in name:
            pollution_level = "Moderate"
        elif "streetlight" in name:
            pollution_level = "High"

    return jsonify({
        "pollution_level": pollution_level,
        "description": description[0]["text"] if description else "No description available."
    })

@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.get_json()
    message = data.get("message", "").lower()

    if "hello" in message or "who are you" in message:
        response = "I am Luma, the guardian of the night sky! I protect the stars from light pollution. Are you ready to learn?"
    elif "nox" in message:
        response = "I am Nox, the bringer of darkness! Artificial lights disrupt nature. Can you stop me?"
    elif "light pollution" in message:
        response = "Light pollution is the excessive use of artificial light, blocking our view of the stars and affecting wildlife."
    else:
        response = "Ask me anything about light pollution! 🌌"

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

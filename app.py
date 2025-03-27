from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Azure Computer Vision API credentials
AZURE_ENDPOINT="https://skyguardian-aiazure.cognitiveservices.azure.com/"
AZURE_KEY="3WoULIpaWAl2aBzJl1yGeFA2D66mc5nhr9hXNDj4QJxOe6VOkQw5JQQJ99BCACYeBjFXJ3w3AAAFACOGewqE"

# Ensure AZURE_ENDPOINT is set before running
if not AZURE_ENDPOINT:
    raise ValueError("AZURE_ENDPOINT is not set. Please define it before running the app.")

if not AZURE_KEY:
    raise ValueError("AZURE_KEY is not set. Please define it before running the app.")

AZURE_ENDPOINT += "/vision/v3.2/analyze"
print(f"Using Azure Endpoint: {AZURE_ENDPOINT}")  # Debugging line

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/meet/<character>")
def meet_character(character):
    messages = {
        "luma": "🌟 Luma: Hello, Guardian! Light pollution is a growing issue affecting our night skies. "
                "To help, use shielded outdoor lights, switch to warm LEDs, and turn off unnecessary lights. "
                "Let's protect the stars together! 🌠",
        "nox": "🌙 Nox: Greetings, traveler. While darkness is feared, it is also necessary. "
               "Light pollution disrupts wildlife, wastes energy, and erases the beauty of the cosmos. "
               "Balance the light and dark, for the night must remain sacred. ⚫"
    }
    return messages.get(character, "Error: Character not found!")

@app.route("/analyze", methods=["POST"])
def analyze_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"].read()
    
    # Azure Vision API parameters
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/octet-stream"
    }
    params = {"visualFeatures": "Categories,Description,Color"}

    # Send request to Azure Vision API
    response = requests.post(AZURE_ENDPOINT, headers=headers, params=params, data=image)
    result = response.json()

    # Extract pollution-related information
    categories = result.get("categories", [])
    description = result.get("description", {}).get("captions", [])

    pollution_level = "Unknown"
    for category in categories:
        if "outdoor_" in category["name"]:
            pollution_level = "Low"
        if "night_" in category["name"]:
            pollution_level = "Moderate"
        if "streetlight" in category["name"]:
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
        response = "Light pollution is the excessive use of artificial light, blocking our view of the stars and affecting wildlife. Let's save the night!"
    else:
        response = "Ask me anything about light pollution! 🌌"

    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(debug=True)

import cv2  

camera = cv2.VideoCapture(0)  # Use default camera  
ret, frame = camera.read()  

if ret:  
    cv2.imwrite("static/captured_sky.jpg", frame)  # Save image  
camera.release() 

import cv2

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("❌ Camera is not accessible. It may be in use by another application.")
else:
    print("✅ Camera is working.")
    camera.release()

from flask_ngrok import run_with_ngrok
app = Flask(__name__)
run_with_ngrok(app)

print("Received Image: ", request.files)  # Debugging ke liye





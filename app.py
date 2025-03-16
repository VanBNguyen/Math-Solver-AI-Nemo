"""
AI Math Solver - Flask Backend
This script sets up a Flask web server to handle math equation solving using the Gemini API.

Author: Van Nguyen
Credit to: Matthew Fewer, Siddig Ahmed, Yashvi Nayak
Date: 2025-03-15
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import json

# Initialize the Flask application
app = Flask(__name__, static_folder='static', template_folder='templates')

# cross-origin type stuff
CORS(app) 

# Define the API key + URL
GEMINI_API_KEY = ""
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Define the route for the homepage
@app.route('/')
def index():
    # Frontend HTML template
    return render_template('index.html')

# Define the route for solving queries
@app.route('/solve', methods=['POST'])
def solve():
    # Get JSON data from the POST request
    data = request.json

    # Extract the "query" field from the JSON data
    prompt_text = data.get("query", "")

    # If no query is provided, return an error response
    if not prompt_text:
        return jsonify({"error": "No input provided"}), 400

    # Set the request headers to send JSON data
    headers = {
        "Content-Type": "application/json"
    }

    # Format the payload according to API requirements
    payload = {
        "contents": [{"parts": [{"text": prompt_text}]}]
    }

    # Send the request to the Gemini API
    response = requests.post(GEMINI_API_URL, headers=headers, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        try:
            # Extract the generated response text from the API response
            answer = result["candidates"][0]["content"]["parts"][0]["text"]
            return jsonify({"solution": answer})  # JSON format return
        # Handle unexpected response format
        except KeyError:
            return jsonify({"error": "Unexpected response format"}), 500 
    else:
        # Return an error message if the request fails
        return jsonify({"error": f"Error {response.status_code}: {response.text}"}), response.status_code

# Run the Flask application if the script is executed directly
# Start the Flask server on port 5000 with debugging enabled
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  
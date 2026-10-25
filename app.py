"""
Flask API for the Projectile Motion Calculator.

How a request moves through this file:
1. The web page sends velocity and angle to POST /calculate.
2. This file checks that the numbers make sense.
3. physics.py does the math.
4. This file sends the results back as JSON.

Run this file from the backend folder:
    python app.py
"""

import math

from flask import Flask, jsonify, request
from flask_cors import CORS

from physics import calculate_projectile

app = Flask(__name__)

# The HTML page is opened from a different address than this API.
# CORS tells the browser that this local learning project may answer that page.
# There are no passwords or private data here.
CORS(app)


def error_response(message):
    """Return a friendly error message and HTTP status 400 (bad input)."""
    return jsonify({"error": message}), 400


@app.route("/calculate", methods=["POST"])
def calculate():
    """Accept velocity and angle, then return the projectile results."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("Please send velocity and angle as JSON.")

    try:
        velocity = float(data["velocity"])
        angle = float(data["angle"])
    except (KeyError, TypeError, ValueError):
        return error_response("Velocity and angle must be numbers.")

    # float("nan") and float("inf") do not raise ValueError, so check them here.
    if not math.isfinite(velocity) or not math.isfinite(angle):
        return error_response("Velocity and angle must be numbers.")

    if velocity <= 0:
        return error_response("Velocity must be greater than 0.")

    # 0 degrees is flat along the ground. 90 degrees is straight up.
    if angle < 0 or angle > 90:
        return error_response("Angle must be between 0 and 90 degrees.")

    result = calculate_projectile(velocity, angle)
    return jsonify(result)


if __name__ == "__main__":
    # debug=True reloads the server when you save a Python file.
    # Use that only on your own computer while learning.
    # The address below must match API_URL in frontend/script.js.
    app.run(debug=True, host="127.0.0.1", port=5000)


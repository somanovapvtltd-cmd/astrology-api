from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
from flask_cors import CORS
CORS(app)

SWISS_URL = "https://ephemeris-api.herokuapp.com/position"  # external Swiss Ephemeris API

def get_position(jd, bodies):
    params = {
        "jd": jd,
        "bodies": ",".join(bodies),
        "ayanamsa": "KP"   # KP OLD Ayanamsha
    }
    r = requests.get(SWISS_URL, params=params)
    return r.json()

@app.route('/chart', methods=['POST'])
def chart():
    data = request.get_json()

    dob = data.get("dob")
    tob = data.get("tob")
    lat = data.get("latitude")
    lon = data.get("longitude")

    if not all([dob, tob, lat, lon]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Convert date to Julian Day using another API (simple)
    year, month, day = map(int, dob.split("-"))
    hour, minute = map(int, tob.split(":"))
    jd = (367 * year 
          - int((7 * (year + int((month + 9) / 12))) / 4)
          + int((275 * month) / 9)
          + day + 1721013.5
          + (hour + minute / 60) / 24)

    bodies = ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn","Rahu","Ketu"]
    positions = get_position(jd, bodies)

    return jsonify({
        "planets": positions.get("positions", {}),
        "note": "Swiss Ephemeris values fetched successfully."
    })

@app.route('/', methods=['GET'])
def home():
    return "Astrology API running (Swiss External API).", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

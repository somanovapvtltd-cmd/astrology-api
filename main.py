from flask import Flask, request, jsonify
import swisseph as swe

app = Flask(__name__)

# Set KP Old Ayanamsha
swe.set_ayanamsa(swe.SIDM_KRISHNAMURTI)

PLANETS = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,
    "Ketu": swe.MEAN_NODE  # will correct to opposite of Rahu
}


def ketu_from_rahu(rahu_deg):
    return (rahu_deg + 180) % 360


@app.route('/chart', methods=['POST'])
def chart():
    data = request.get_json()

    dob = data.get("dob")
    tob = data.get("tob")
    lat = data.get("latitude")
    lon = data.get("longitude")

    # Validate input
    if not all([dob, tob, lat, lon]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Convert date + time to Julian day
    year, month, day = map(int, dob.split("-"))
    hour, minute = map(int, tob.split(":"))
    jd = swe.julday(year, month, day, hour + minut

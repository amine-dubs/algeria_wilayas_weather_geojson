import json
import requests
import time
from shapely.geometry import shape

#  ✅ Load your GeoJSON file (downloaded one)
with open('all-wilayas.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("Loaded wilayas:", len(data['features']))

def fetch_weather(lat, lon):
    """Get real forecast (current hour) weather data for a location"""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relativehumidity_2m,"
        "windspeed_10m,pressure_msl"
        "&timezone=Africa%2FAlgiers"
    )
    r = requests.get(url)
    if r.status_code == 200:
        d = r.json()
        idx = -1  # latest hour in array
        return {
            "time": d["hourly"]["time"][idx],
            "temperature": d["hourly"]["temperature_2m"][idx],
            "humidity": d["hourly"]["relativehumidity_2m"][idx],
            "windspeed": d["hourly"]["windspeed_10m"][idx],
            "pressure": d["hourly"]["pressure_msl"][idx],
        }
    return None

# ✅ Loop through all wilayas, get weather, attach data
for feature in data['features']:
    geom = shape(feature['geometry'])
    centroid = geom.centroid
    lat, lon = centroid.y, centroid.x

    print(f"Fetching for {feature['properties'].get('name', 'Unknown')} ...")
    weather = fetch_weather(lat, lon)

    if weather:
        feature['properties'].update(weather)

    time.sleep(0.2)  # avoid hammering API

# ✅ Save updated GeoJSON with weather info
with open('all-wilayas.geojson', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ DONE! File saved as all-wilayas.geojson")

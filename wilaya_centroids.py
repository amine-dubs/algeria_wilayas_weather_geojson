import json
from shapely.geometry import shape, mapping

# Input: your polygon GeoJSON file (with properties including temperature/humidity)
IN = "all-wilayas.geojson"
OUT = "wilaya_centroids.geojson"

with open(IN, "r", encoding="utf-8") as f:
    gj = json.load(f)

pts = {"type":"FeatureCollection","features":[]}
for feat in gj["features"]:
    geom = shape(feat["geometry"])
    cen = geom.centroid
    props = feat.get("properties", {})
    h = props.get("humidity") or 0
    radius = 3 + (float(h)/100.0) * 10  # 3..13 px
    p = {
        "type":"Feature",
        "geometry": mapping(cen),
        "properties": {
            "name": props.get("name"),
            "temperature": props.get("temperature"),
            "humidity": props.get("humidity"),
            "windspeed": props.get("windspeed"),
            "pressure": props.get("pressure"),
            "weather_time": props.get("weather_time"),
            "radius": radius
        }
    }
    pts["features"].append(p)

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(pts, f, ensure_ascii=False, indent=2)

print("Saved", OUT)

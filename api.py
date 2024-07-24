from flask import Flask, jsonify
import json
import random
import math

app = Flask(__name__)

# Cargar los datos desde el archivo JSON
with open("taxpayers.json", "r") as file:
    taxpayers = json.load(file)

# Ubicación de la oficina de Fixat (en coordenadas de latitud y longitud)
office_location = {
    "latitude": 19.3797208,
    "longitude": -99.1940332
}

def haversine(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos en la Tierra utilizando la fórmula de Haversine.
    """
    R = 6371  # Radio de la Tierra en kilómetros
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def calculate_score(taxpayer):
    """
    Calcula la puntuación de un contribuyente basado en su comportamiento y proximidad a la oficina.
    """
    if taxpayer["accepted_offers"] + taxpayer["canceled_offers"] == 0:
        return random.randint(7, 10)
    
    # Calcular la tasa de aceptación de ofertas
    acceptance_rate = taxpayer["accepted_offers"] / (taxpayer["accepted_offers"] + taxpayer["canceled_offers"])
    # Tiempo promedio de respuesta
    average_reply_time = taxpayer["average_reply_time"]
    
    # Calcular la distancia a la oficina de Fixat
    distance = haversine(
        taxpayer["location"]["latitude"],
        taxpayer["location"]["longitude"],
        office_location["latitude"],
        office_location["longitude"]
    )
    
    # Calcula la puntuación base
    score = acceptance_rate * 10 - average_reply_time / 3600 * 2
    # Ajusta la puntuación en función de la proximidad
    score += max(0, 10 - distance / 50)  # Añade puntos por proximidad, ajustado a una escala de 10 puntos
    # Asegura que la puntuación esté entre 1 y 10
    score = max(1, min(10, score))
    return score

# Asigna una puntuación a cada contribuyente
for taxpayer in taxpayers:
    taxpayer["score"] = calculate_score(taxpayer)

def get_top_10_taxpayers():
    """
    Obtiene los 10 mejores contribuyentes basados en su puntuación.
    """
    sorted_taxpayers = sorted(taxpayers, key=lambda x: x["score"], reverse=True)
    return sorted_taxpayers[:10]

@app.route("/", methods=["GET"])
def home():
    """
    Ruta principal que muestra un mensaje de confirmación.
    """
    return "API de Fixat está en funcionamiento. Usa el endpoint /get_top_taxpayers para obtener los datos."

@app.route("/get_top_taxpayers", methods=["GET"])
def get_top_taxpayers_route():
    """
    Ruta que devuelve los 10 mejores contribuyentes como un JSON.
    """
    top_10 = get_top_10_taxpayers()
    return jsonify(top_10)

if __name__ == "__main__":
    # Ejecuta la aplicación Flask en modo de depuración
    app.run(debug=True)


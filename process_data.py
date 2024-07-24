import json
import random

# Cargar los datos desde el archivo JSON
with open("taxpayers.json", "r") as file:
    taxpayers = json.load(file)

def calculate_score(taxpayer):
    """
    Calcula la puntuación de un contribuyente basado en su comportamiento.
    """
    # Si el número total de ofertas (aceptadas + canceladas) es 0, asigna una puntuación aleatoria entre 7 y 10
    if taxpayer["accepted_offers"] + taxpayer["canceled_offers"] == 0:
        return random.randint(7, 10)
    
    # Calcula la tasa de aceptación de ofertas
    acceptance_rate = taxpayer["accepted_offers"] / (taxpayer["accepted_offers"] + taxpayer["canceled_offers"])
    # Tiempo promedio de respuesta
    average_reply_time = taxpayer["average_reply_time"]
    
    # Calcula la puntuación
    score = acceptance_rate * 10 - average_reply_time / 3600 * 2
    score = max(1, min(10, score))  # Asegurar que la puntuación esté entre 1 y 10
    return score

# Calcula y asigna la puntuación a cada contribuyente
for taxpayer in taxpayers:
    taxpayer["score"] = calculate_score(taxpayer)

def get_top_10_taxpayers(taxpayers):
    sorted_taxpayers = sorted(taxpayers, key=lambda x: x["score"], reverse=True)
    return sorted_taxpayers[:10]

top_10_taxpayers = get_top_10_taxpayers(taxpayers)

# Imprimir los 10 mejores contribuyentes
for taxpayer in top_10_taxpayers:
    print(f"Name: {taxpayer['name']}, Score: {taxpayer['score']}")

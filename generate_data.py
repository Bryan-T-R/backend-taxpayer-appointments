###########################################################
#                                                         #
#   Script para generar datos de contribuyentes           #
#   Uso:                                                  #
#     1. Instala la biblioteca Faker: pip3 install Faker  #
#     2. Ejecuta el script: python3 generate_data.py      #
#                                                         #
###########################################################

from faker import Faker
import json

fake = Faker()
Faker.seed(0)

# Lista para almacenar los datos de los contribuyentes
taxpayers = []

# Generar datos
for _ in range(1000):
    # Generar datos falsos de geolocalización
    geolocation = fake.local_latlng(country_code="MX")
    taxpayer = {
        "id": fake.uuid4(),
        "name": fake.name(),
        "location": {
            "latitude": float(geolocation[0]),
            "longitude": float(geolocation[1])
        },
        "age": fake.random_int(18, 90),
        "accepted_offers": fake.random_int(0, 100),
        "canceled_offers": fake.random_int(0, 100),
        "average_reply_time": fake.random_int(1, 3600),
    }
    taxpayers.append(taxpayer)

# Guardar los datos generados en un archivo JSON
with open("taxpayers.json", "w") as outfile:
    json.dump(taxpayers, outfile, indent=4)  # Guardar con formato legible

# Imprimir mensaje de confirmación
print("Datos generados y guardados en taxpayers.json")

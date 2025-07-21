import requests
import urllib.parse
import os

key = "58e18b34-9b51-4906-a65a-72d5ab40b39e"
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

#latitud y longitud ciudad
def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    if replydata.status_code == 200 and len(json_data["hits"]) > 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        return lat, lng
    else:
        print("No se encontraron resultados.")
        return None, None

#distancia y duración del viaje
def calculate_trip_distance(lat1, lng1, lat2, lng2, vehicle, key):
    op = f"&point={lat1}%2C{lng1}"
    dp = f"&point={lat2}%2C{lng2}"
    vehicle_param = f"&vehicle={vehicle}"
    paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp + vehicle_param
    paths_response = requests.get(paths_url)
    if paths_response.status_code == 200:
        paths_data = paths_response.json()
        distance_km = paths_data["paths"][0]["distance"] / 1000 
        distance_miles = distance_km / 1.61  
        duration_sec = paths_data["paths"][0]["time"] / 1000  
        hours = int(duration_sec // 3600)
        minutes = int((duration_sec % 3600) // 60)
        seconds = int(duration_sec % 60)
        return distance_km, distance_miles, hours, minutes, seconds
    else:
        print("No se pudo obtener la ruta.")
        return None, None, None, None, None

#bucle principal
while True:
    os.system("clear")
    
    print("=======================================")
    loc1 = input("Ciudad de Origen (o 's' para salir): ")
    if loc1.lower() == 's':
        break
    loc2 = input("Ciudad de Destino (o 's' para salir): ")
    if loc2.lower() == 's':
        break

    #latitudes y longitudes
    lat1, lng1 = geocoding(loc1, key)
    lat2, lng2 = geocoding(loc2, key)

    if lat1 and lat2:
        transport = input("Selecciona el medio de transporte (Auto, Bicicleta, Caminar): ")
        if transport.lower() == "auto":
            vehicle = "car"
        elif transport.lower() == "bicicleta":
            vehicle = "bike"
        elif transport.lower() == "Caminar":
            vehicle = "foot"
        else:
            print("Medio de transporte no válido. Usaremos 'Auto' como valor por defecto.")
            vehicle = "car"

        print(f"Viajarás en: {transport}")

        #distancia y duración del viaje
        distance_km, distance_miles, hours, minutes, seconds = calculate_trip_distance(lat1, lng1, lat2, lng2, vehicle, key)

        if distance_km is not None:
            print(f"Distancia entre {loc1} y {loc2}: {distance_km:.2f} km / {distance_miles:.2f} millas")
            print(f"Duración del viaje: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
            print(f"Viajarás desde {loc1}, hacia {loc2} ¡Buen viaje!.")

    print("=======================================")
    user_input = input("Presiona enter para continuar o 's' para salir: ")
    if user_input.lower() == 's':
        break
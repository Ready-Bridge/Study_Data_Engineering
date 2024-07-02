import requests

lat = 42.36
lon = 71.05
lat_log_params = {"lat" : lat, "lon" : lon}

api_response = requests.get("http://api.open-notify.org/iss-pass.json", params=lat_log_params)

print(api_response.content)
#Note! For the code to work you need to replace all the placeholders with
#Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/weather?q=Auckland&appid=a748f283bc87656474b62d6292529cad"
api_key = os.environ.get("a748f283bc87656474b62d6292529cad")
account_sid = "AC3c1952838e332a6441a335fbda03c355"
auth_token = os.environ.get("c3daf729c3396d51195bce75529d6611")

weather_params = {
    "lat": -36.976330,
    "lon": 174.915180,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body ="It's going to rain today. Remember to bring an ☔️",
        from_="+12184603929",
        to ="+64273003411"
    )
    print(message.status)

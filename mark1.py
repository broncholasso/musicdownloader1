import os
from dotenv import load_dotenv
import base64   
import requests
import json
from requests import post, get

load_dotenv()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers= headers, data= data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

token = get_token()

# def get_auth(token):
#     return {"authorization" : "bearer " + token}

# def extract_id(usr_url):
#     id = None
#     if "open.spotify.com/playlist/" in usr_url:
#         seg1 = usr_url.split("/")
#         seg2 = seg1[-1]
#         seg3 = seg2.split("?")
#         id = seg3[0] 
#     else:
#      print("PLEASE PROVIDE VALID PLAYLIST LINK")

#     return id
   

# usr_url = input("please provide your playlist link : ")

# id = extract_id(usr_url)

id = "4uhywAuvqNRPLs8Z7MYYG5"


access_token = token
market = 'ES'
fields = 'items(track(name))'

endpoint = f"https://api.spotify.com/v1/playlists/{id}/tracks"

headers = {
   
    "Authorization" : "Bearer " + access_token
}

query = {
   
   'market':market,
   'fields':fields
}

response = requests.get(endpoint, headers=headers, params=query)

if response.status_code == 200:
   playlist_data = response.json()
   tracks = playlist_data['items']
   for item in tracks:
        track_names = item['track']['name']
else:
     print(f"unable to parse any data.{response.status_code}error")

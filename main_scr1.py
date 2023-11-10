import os
from dotenv import load_dotenv
import base64   
import requests
import json
from requests import post, get
from googleapiclient.discovery import build
import yt_dlp


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

def extract_id(usr_url):
    id = None
    if "open.spotify.com/playlist/" in usr_url:
        seg1 = usr_url.split("/")
        seg2 = seg1[-1]
        seg3 = seg2.split("?")
        id = seg3[0] 
    else:
     print("PLEASE PROVIDE VALID PLAYLIST LINK")

    return id
   

usr_url = input("please provide your playlist link : ")

id = extract_id(usr_url)

# id = "4uhywAuvqNRPLs8Z7MYYG5"


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
        print(track_names)
        with open('fetched_data/tracknames.text', 'a') as l:
            l.write(track_names + '\n')
else:
     print(f"unable to parse any data.{response.status_code}error")

#2 ----

api_key = os.getenv('API_KEY')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

youtube = build("youtube", "v3", developerKey=api_key)

with open ('fetched_data/tracknames.text', 'r') as p:
    for line in p:
        search_query = line.strip() + '\n'
        search_response = youtube.search().list(
            q=search_query,
            type="video",
            part="id",
            maxResults=3
        )
        response = search_response.execute()
        if 'items' in response:
            first_video_id = response['items'][0]['id']['videoId']
            link = f'https://www.youtube.com/watch?v={first_video_id}'
            print(link)
        else:
            print("No video results found.")

#3-----
        path = 'fetched_data/song'
        url = link


        ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{path}/%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            original_file = ydl.prepare_filename(info_dict)

        new_file = os.path.splitext(original_file)[0] + '.mp3'
        os.rename(original_file, new_file)

        # print(f'Successfully renamed to MP3: {new_file}')





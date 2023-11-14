import os
from dotenv import load_dotenv
import base64   
import requests
import json
from requests import post, get
from googleapiclient.discovery import build
import yt_dlp
import asyncio
import aiohttp
import threading


load_dotenv()


client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")


async def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"

    }
    data = {"grant_type": "client_credentials"}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            json_result = await response.json()
            token = json_result["access_token"]
            return token

async def extract_id(usr_url):
    id = None
    if "open.spotify.com/playlist/" in usr_url:
        seg1 = usr_url.split("/")
        seg2 = seg1[-1]
        seg3 = seg2.split("?")
        id = seg3[0] 
    else:
     print("PLEASE PROVIDE VALID PLAYLIST LINK")

    return id
   

async def fetch_track_names(id, access_token):
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

    async with aiohttp.ClientSession() as session:
        async with session.get(endpoint, headers = headers, params = query) as response:
            if response.status == 200:
                playlist_data = await response.json()
                return [item['track']['name'] for item in playlist_data.get('items',[])]
            else:
                print(f"Unable to parse any data. {response.status} error")
                return []

async def search_youtube(track_names, api_key):
    youtube_links = []

    def get_youtube_results(track_name):
        nonlocal youtube_links
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"
        youtube = build('youtube', 'v3', developerKey=api_key)
        search_query = track_name + '\n'
        search_response = youtube.search().list(
            q=search_query,
            type='video',
            part='id',
            maxResults=1,
        ).execute()

        if 'items' in search_response:
            video_id = search_response['items'][0]['id']['videoId']
            link = f'https://www.youtube.com/watch?v={video_id}'
            print(link)
            youtube_links.append(link)
        else:
            print("No video results found.")

    threads = []
    for track_name in track_names:
        thread = threading.Thread(target=get_youtube_results, args=(track_name,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return youtube_links


async def download_song(url, semaphore):
    path = 'fetched_data/song'
    async with semaphore:  
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{path}/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = await asyncio.to_thread(ydl.extract_info, url, download=True)
            title = info_dict.get('title', None)
            if title:
                mp3_file = os.path.join(path, f"{title}.mp3")
                if os.path.exists(mp3_file):
                    print(f"Song '{title}' already exists. Skipping download.")
                else:
                    print(f'Successfully downloaded: {mp3_file}')
                    original_file = ydl.prepare_filename(info_dict)
                    new_file = os.path.splitext(original_file)[0] + '.mp3'
                    os.rename(original_file, new_file)
                    print(f'Successfully renamed to MP3: {new_file}')
            else:
                print("Failed to retrieve song information.")

async def download_songs(youtube_links):
    semaphore = asyncio.Semaphore(9) 
    await asyncio.gather(*(download_song(url, semaphore) for url in youtube_links))

async def main():
    access_token = await get_token()
    usr_url = input(f'please provide your playlist link: \n')
    id = await extract_id(usr_url)
    

    if id:
        track_names = await fetch_track_names(id,access_token)
        youtube_links = await search_youtube(track_names, os.getenv("API_KEY1"))
        await download_songs(youtube_links)

if __name__ == "__main__":
    asyncio.run(main())
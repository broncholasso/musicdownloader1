# import os
# from googleapiclient.discovery import build
# from dotenv import load_dotenv

# load_dotenv()

# api_key = os.getenv('API_KEY')

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

# youtube = build("youtube", "v3", developerKey=api_key)

# search_query = "maps maroon5"

# search_response = youtube.search().list(
#     q=search_query,
#     type="video",
#     part="id",
#     maxResults=3
# )
# response = search_response.execute()

# # print(response)

# if 'items' in response:
#     first_video_id = response['items'][0]['id']['videoId']
#     link = f'https://www.youtube.com/watch?v={first_video_id}'
#     print(link)
# else:
#     print("No video results found.")
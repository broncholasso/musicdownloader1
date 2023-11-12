# import yt_dlp
# import os

# path = 'fetched_data/song'
# url = "https://www.youtube.com/watch?v=RPtImg9oYyc"


# ydl_opts = {
#     'format': 'bestaudio/best',
#     'outtmpl': f'{path}/%(title)s.%(ext)s',
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info_dict = ydl.extract_info(url, download=True)
#     original_file = ydl.prepare_filename(info_dict)

# # Rename the file from .webm to .mp3
# new_file = os.path.splitext(original_file)[0] + '.mp3'
# os.rename(original_file, new_file)

# print(f'Successfully renamed to MP3: {new_file}')
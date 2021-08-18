import requests
import os




def get_youtube_video(id: str):

    YOUTUBE_TOKEN = os.getenv('YOUTUBE_API_TOKEN')

    req = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={id}&key={YOUTUBE_TOKEN}')

    data = req.json()

    return data['items'][0]



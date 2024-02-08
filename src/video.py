import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        self.name = self.video['items'][0]["snippet"]['title']
        self.url = f'https://www.youtube.com/{self.video_id}'
        self.quantity_view = self.video['items'][0]['statistics']['viewCount']
        self.quantity_like = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.name


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
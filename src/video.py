import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        try:
            self.title = self.video['items'][0]["snippet"]['title']
            self.url = f'https://www.youtube.com/{self.video_id}'
            self.quantity_view = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']
        except IndexError:
            print(IndexError('несуществующий id'))
        finally:
            self.title = None
            self.url = None
            self.quantity_view = None
            self.like_count = None

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id
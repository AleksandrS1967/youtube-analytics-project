import os
from datetime import datetime as dt
from datetime import timedelta
from googleapiclient.discovery import build

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class PlayList:
    """инициализирует id плейлиста"""

    def __init__(self, plist_id):
        self.__plist_id = plist_id
        self.__plist_items = youtube.playlistItems().list(part='snippet,contentDetails',
                                                          playlistId=self.__plist_id).execute()
        self.url = f'https://www.youtube.com/playlist?list={self.__plist_id}'
        self.__channel_id = self.__plist_items['items'][0]['snippet']['channelId']
        self.title = self.__get_title()
        self.__video_list = self.__get_video_list()

    @property
    def total_duration(self):
        """возвращает объект класса datetime.timedelta с суммарной длительностью плейлиста"""
        total = timedelta()  # hours=0, minutes=0, seconds=0
        for video in self.__video_list['items']:
            str_duration = video['contentDetails']['duration']
            if 'S' in str_duration:
                dt_video_duration = dt.strptime(str_duration, 'PT%MM%SS').time()
            else:
                dt_video_duration = dt.strptime(str_duration, 'PT%MM').time()
            hours, minutes, seconds = str(dt_video_duration).split(":")
            total += timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        return total

    def show_best_video(self):
        """возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)"""
        like_count = 0
        url = ''
        for video in self.__video_list['items']:
            if like_count < int(video['statistics']['likeCount']):
                like_count = int(video['statistics']['likeCount'])
                url = f"https://youtu.be/{video['id']}"
        return url

    def __get_title(self):
        title = ''
        plists = youtube.playlists().list(channelId=self.__channel_id, part='contentDetails,snippet',
                                          maxResults=10, ).execute()
        for plist in plists['items']:
            if plist['id'] == self.__plist_id:
                title = plist['snippet']['title']
        return title

    def __get_video_list(self):
        video_id_list = [video['contentDetails']['videoId'] for video in self.__plist_items['items']]
        video_list = youtube.videos().list(part='contentDetails,statistics', id=','.join(video_id_list)).execute()
        return video_list

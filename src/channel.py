import os
from googleapiclient.discovery import build
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)


class Channel:
    """Класс для ютуб-канала"""
    object_list = []
    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]["snippet"]['title']
        self.channel_description = self.channel['items'][0]["snippet"]["description"]
        self.url = f'https://www.youtube.com/channel/{channel_id}'
        self.channel_description = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.count_views = self.channel['items'][0]['statistics']['viewCount']
        self.object_list.append(self)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        item = json.dumps(self.channel, indent=2, ensure_ascii=False)
        i = json.loads(item)
        return i

    def to_json(self, path):
        """ сохраняет в файл значения атрибутов экземпляра Channel"""
        data = {
            'id': f'{self.__channel_id}',
            'title': f'{self.title}',
            'channel_description': f'{self.channel_description}',
            'url': f'{self.url}',
            'video_count': f'{self.video_count}',
            'count_views': f'{self.count_views}'
        }
        with open(path, 'a') as f:
            if os.stat(path).st_size == 0:
                json.dump([data], f)
            else:
                with open(path) as f_:
                    list_ = json.load(f_)
                    list_.append(data)
                with open(path, 'w') as f_1:
                    json.dump(list_, f_1)

    @classmethod
    def get_service(cls):
        """возвращает объект для работы с YouTube API"""
        return cls.object_list[0]

    def chec(self, data):
        if data.isdigit():
            return int(data)
        else:
            return False


    def __str__(self):
        return f"'{self.title} ({self.url})'"

    def __add__(self, other):
        return self.chec(self.channel_description) + self.chec(other.channel_description)

    def __sub__(self, other):
        return self.chec(self.channel_description) - self.chec(other.channel_description)

    def __gt__(self, other):
        return self.chec(self.channel_description) > self.chec(other.channel_description)

    def __ge__(self, other):
        return self.chec(self.channel_description) >= self.chec(other.channel_description)

    def __lt__(self, other):
        return self.chec(self.channel_description) < self.chec(other.channel_description)

    def __le__(self, other):
        return int(self.channel_description) <= int(other.channel_description)

    def __eq__(self, other):
        return int(self.channel_description) == int(other.channel_description)




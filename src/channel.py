import json
import os

from src.mixinapi import MixinAPI


class Channel(MixinAPI):
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.channel = self.get_service().channels().list(
            id=channel_id, part='snippet,statistics'
        ).execute()

        self.id = self.channel['items'][0]['id']
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.custom_url = self.channel['items'][0]['snippet']['customUrl']
        self.url = f'https://www.youtube.com/{self.custom_url}'
        self.number_of_subscribers = int(self.channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.channel['items'][0]['statistics']['videoCount'])
        self.total_views = int(self.channel['items'][0]['statistics']['viewCount'])

    def __str__(self):
        """Метод выводит информацию о названии канала
        и выводит ссылку на этот канал"""
        return f'{self.title}({self.url})'

    def __add__(self, other):
        """Метод складывает количество подписчиков"""
        return self.number_of_subscribers + other.number_of_subscribers

    def __sub__(self, other):
        """Метод вычитает количество подписчиков"""
        return self.number_of_subscribers - other.number_of_subscribers

    def __lt__(self, other):
        """Метод сравнивает меньше ли первый канал
        по подписчикам чем второй канал"""
        return self.number_of_subscribers < other.number_of_subscribers

    def __le__(self, other):
        """Метод сравнивает меньше или равно количество
        подписчиков первого канала по сравнению со вторым"""
        return self.number_of_subscribers <= other.number_of_subscribers

    def __gt__(self, other):
        """Метод сравнивает больше ли первый канал
        по подписчикам чем второй канал"""
        return self.number_of_subscribers > other.number_of_subscribers

    def __ge__(self, other):
        """Метод сравнивает больше или равно количество
        подписчиков первого канала по сравнению со вторым"""
        return self.number_of_subscribers >= other.number_of_subscribers

    def __eq__(self, other):
        """Метод сравнивает равно ли количество подписчиков двух каналов"""
        return self.number_of_subscribers == other.number_of_subscribers

    @property
    def channel_id(self):
        """Декоратор позволяет обращаться к ID как к аргументу"""
        return self.__channel_id

    def to_json(self, path):
        my_data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'custom_url': self.custom_url,
            'url': self.url,
            'number_of_subscribers': self.number_of_subscribers,
            'video_count': self.video_count,
            'total_views': self.total_views
        }
        with open(path, 'w') as file:
            json.dump(my_data, file, indent=2, ensure_ascii=False)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.channel, indent=2, ensure_ascii=False))

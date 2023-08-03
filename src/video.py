from src.mixinapi import MixinAPI


class Video(MixinAPI):
    def __init__(self, video_id):
        self.__video_id = video_id
        self.video = self.get_service().videos().list(
            id=video_id, part='snippet,statistics'
        ).execute()
        self.id = self.__video_id
        try:
            self.title = self.video['items'][0]['snippet']['title']
        except IndexError:
            self.title = None
            self.url = None
            self.video_count = None
            self.like_count = None
        else:
            self.url = f'https://youtu.be/{self.__video_id}'
            self.video_count = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

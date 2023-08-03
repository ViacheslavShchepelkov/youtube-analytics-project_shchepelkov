import datetime as dt

import isodate

from src.mixinapi import MixinAPI


class PlayList(MixinAPI):
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlists = self.get_service().playlists().list(id=self.playlist_id,
                                                        part='contentDetails,snippet',
                                                        ).execute()

        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def __str__(self):
        return f'{self.total_duration}'

    def get_playlist_videos(self):
        playlist_videos = self.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                                  part='contentDetails',
                                                                  maxResults=50,
                                                                  ).execute()

        _video_id = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(_video_id)
                                                          ).execute()
        return video_response

    @property
    def total_duration(self):
        video_response = self.get_playlist_videos()
        my_duration = dt.timedelta()
        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_duration = video['contentDetails']['duration']
            my_duration += isodate.parse_duration(iso_duration)
        return my_duration

    def show_best_video(self):
        playlists = self.get_playlist_videos()
        likes_count = 0
        video_id = ''
        for video in playlists['items']:
            point_like = int(video['statistics']['likeCount'])
            if point_like > likes_count:
                likes_count = point_like
                video_id = (video['id'])
        return f'https://youtu.be/{video_id}'

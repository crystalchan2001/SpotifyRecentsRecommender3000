import json
import requests
from track import Track
from playlist import Playlist


client_id = "92e6033330c34aeca3ec7b17c2d33351"
client_secret = "938d194839ed4c59ac6f13bb00a1993e"
authorization_url = "https://accounts.spotify.com/authorize"
redirect_uri = "http://localhost/"
token_url = "https://accounts.spotify.com/api/token"

scope = "playlist-modify-public playlist-modify-private playlist-read-private user-read-recently-played user-read-private user-read-email"

class SpotifyBrain:
    """SpotifyClient performs operations using the Spotify API"""

    def __init__(self):
        self.uris = []
        self.access_token = self.obtain_access_token()
        self.headers_authentication = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        self.user_id = self.obtain_id()

    def obtain_id(self):
        url = " https://api.spotify.com/v1/me"
        response = self._place_get_api_request(url).json()
        try:
            response["id"]
        except:
            print(response["error"])
        else:
            return response["id"]

    def obtain_access_token(self):
        authorization_params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": {redirect_uri},
            "scope": scope
        }
        response_url = requests.get(authorization_url, params=authorization_params).url
        print(response_url)
        authorization_code = input("Enter the authorization code: ")
        # Step 2: Exchange authorization code for access token

        data = {
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        response_json = requests.post(token_url, data=data).json()
        access_token = response_json["access_token"]

        return access_token

    def _place_get_api_request(self, url):
        response = requests.get(
            url,
            headers = self.headers_authentication
        )
        return response
    
    def _place_post_api_request(self, url, data):
        response = requests.post(
            url,
            data = data,
            headers = self.headers_authentication
        )
        return response

    def get_last_played_tracks(self, limit=10):
        """Get the last number (limit) tracks played
        :param limit (int): Number of tracks to get
        :return tracks (list of Track): List of last played tracks 
        """
        url = f"https://api.spotify.com/v1/me/player/recently-played?limit={limit}"
        response = self._place_get_api_request(url).json()
        try:
            response["items"]
        except:
            print(response["error"])
        else:
            tracks = [Track(track["track"]["name"], track["track"]["id"], track["track"]["artists"][0]["name"], track["track"]["album"]["name"]) for track
                        in response["items"]]
            return tracks
    
    def get_track_recommendations(self, seed_tracks, limit):
        """Get a list of recommended tracks starting from a number of seed tracks.
        :param seed_tracks (list of Track): Should be five or less
        :param limit (int): Number of recommended to be returned
        :param tracks (list of Track): Recommended tracks list
        """
        seed_tracks_url = ""
        for seed_track in seed_tracks:
            seed_tracks_url += seed_track.id + ","
        seed_tracks_url = seed_tracks_url[:-1]
        url = f"https://api.spotify.com/v1/recommendations?seed_tracks={seed_tracks_url}&limit={limit}"
        response = self._place_get_api_request(url).json()
        try:
            response["tracks"]
        except:
            response["error"]
        else:
            tracks = [Track(track["name"], track["id"], track["artists"][0]["name"], track["album"]["name"]) for track
                        in response["tracks"]]
            return tracks

    def create_playlist(self, name):
        data = json.dumps({
            "name": name,
            "description": "Recommended tracks using a python program. The first module in creating project #1.",
            "public": True
        })
        url = f"https://api.spotify.com/v1/users/{self.user_id}/playlists"
        response = self._place_post_api_request(url, data).json()

        # create the playlist
        try:
            response["id"]
        except:
            response["error"]
        else:
            playlist_id = response["id"]
            playlist = Playlist(name, playlist_id)
            return playlist

    def populate_playlist(self, playlist, tracks):
        tracks_uris = [track.create_spotify_uri() for track in tracks]
        data = json.dumps(tracks_uris)
        url = f"https://api.spotify.com/v1/playlists/{playlist.id}/tracks"
        response = self._place_post_api_request(url, data).json()
        return response
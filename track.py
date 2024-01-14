class Track:
    """Represents a piece of music on Spotify."""

    def __init__(self, name, id, artist, album):
        """
        :param name (str): Track name
        :param id (int): Track id
        :param artist (str): Track artist
        """
        self.name = name
        self.id = id
        self.artist = artist
        self.album = album
    
    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"
    
    def __str__(self):
        return f"{self.name} by {self.artist} from {self.album}"
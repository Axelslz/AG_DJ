from typing import List


class Song:
    def __init__(self, title: str, artist: str, album: str, danceability: float, energy: float, loudness: float, tempo: float) -> None:
        # Song information
        self.title: str = title
        self.artist: str = artist
        self.album: str = album
        # Genes parameters
        self.danceability: float = danceability
        self.energy: float = energy
        self.loudness: float = loudness
        self.tempo: float = tempo

    def __str__(self) -> str:
        return f"Title: {self.title} Artist: {self.artist} Album: {self.album}\nDanceability: {self.danceability} Energy: {self.energy} Loudness{self.loudness} Tempo: {self.tempo}"


class Playlist:
    def __init__(self, songs: List[Song]) -> None:
        self.songs: List[Song] = songs

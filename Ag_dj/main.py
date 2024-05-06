from tkinter import Tk
from models import Song
from gui import MusicalizerGUI
from song_pool import initialize_song_pool

def main():

    song_pool = initialize_song_pool()
    window = Tk()
    musicalizer_gui = MusicalizerGUI(window, song_pool=song_pool)
    musicalizer_gui.run()


if __name__ == "__main__":
    main()

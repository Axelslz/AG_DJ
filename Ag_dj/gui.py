from tkinter.ttk import Scrollbar, Treeview
from typing import List
from genetic_algorithm import Musicalizer
from models import Song, Playlist
from tkinter import BOTH, END, EXTENDED, LEFT, MULTIPLE, SINGLE, VERTICAL, W, Y, Label, Listbox, Entry, Button, Variable
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MusicalizerGUI:

    def __init__(self, master, song_pool: List[Song]):
        self.master = master
        self.song_pool: list = song_pool
        self.setup_gui()

    def setup_gui(self):
        self.master.title("Musicalizer")
        self.master.geometry("1000x800")
        self.master.configure(background='white')

        def execute_algorithm():
            energy: tuple = (float(energy_start_entry.get()),
                             float(energy_end_entry.get()))
            
            tempo: tuple = (float(tempo_start_entry.get()),
                            float(tempo_end_entry.get()))
            
            loudness: tuple = (
                float(loudness_start_entry.get()), float(loudness_end_entry.get()))
            
            danceability: tuple = (float(danceability_start_entry.get()), float(
                danceability_end_entry.get()))

            musicalizer: Musicalizer = Musicalizer(population_size=500,
                                                   crossover_rate=0.8,
                                                   mutation_rate=0.1,
                                                   num_generations=500,
                                                   song_pool=self.song_pool,
                                                   danceability=danceability,
                                                   energy=energy, loudness=loudness,
                                                   tempo=tempo,
                                                   playlist_size=10)

            playlist: Playlist = musicalizer.run()
            self.graph(musicalizer)
            self.display_playlist(playlist)

        energy_label = Label(self.master, text="Energy:")
        energy_label.grid(row=0, column=0, padx=10, pady=10)
        energy_start_entry = Entry(self.master)
        energy_start_entry.insert("end", "0.4")
        energy_start_entry.grid(row=1, column=0, padx=10, pady=10)
        energy_end_entry = Entry(self.master)
        energy_end_entry.insert("end", "0.6")
        energy_end_entry.grid(row=1, column=1, padx=10, pady=10)

        tempo_label = Label(self.master, text="Tempo:")
        tempo_label.grid(row=2, column=0, padx=10, pady=10)
        tempo_start_entry = Entry(self.master)
        tempo_start_entry.insert("end", "60.0")
        tempo_start_entry.grid(row=3, column=0, padx=10, pady=10)
        tempo_end_entry = Entry(self.master)
        tempo_end_entry.insert("end", "80.0")
        tempo_end_entry.grid(row=3, column=1, padx=10, pady=10)

        loudness_label = Label(self.master, text="Loudness:")
        loudness_label.grid(row=4, column=0, padx=10, pady=10)
        loudness_start_entry = Entry(self.master)
        loudness_start_entry.insert("end", "-0.15")
        loudness_start_entry.grid(row=5, column=0, padx=10, pady=10)
        loudness_end_entry = Entry(self.master)
        loudness_end_entry.insert("end", "-0.10")
        loudness_end_entry.grid(row=5, column=1, padx=10, pady=10)

        danceability_label = Label(self.master, text="Danceability:")
        danceability_label.grid(row=6, column=0, padx=10, pady=10)
        danceability_start_entry = Entry(self.master)
        danceability_start_entry.insert("end", "0.2")
        danceability_start_entry.grid(row=7, column=0, padx=10, pady=10)
        danceability_end_entry = Entry(self.master)
        danceability_end_entry.insert("end", "0.4")
        danceability_end_entry.grid(row=7, column=1, padx=10, pady=10)

        get_all_data_button = Button(
            self.master, text="Run", command=execute_algorithm)
        get_all_data_button.grid(row=8, column=0, columnspan=2, pady=10)


    def run(self):
        self.master.resizable(False, False)
        self.master.mainloop()


    
    def graph(self, ga: Musicalizer):
        figure2 = plt.figure()
        plt.plot(np.arange(0, ga.num_generations), ga.best_cases, label="Best cases")
        plt.plot(np.arange(0, ga.num_generations), ga.worst_cases, label="Worst cases")
        plt.plot(np.arange(0, ga.num_generations), ga.avg_cases, label="Average cases")
        plt.legend()
        plt.title("Evolución de la población")
        plt.xlabel("Generaciones/Iteraciones")
        plt.ylabel("Valor de aptitud")
        linear = FigureCanvasTkAgg(figure2, self.master)
        linear.get_tk_widget().grid(row=0, column=3, rowspan=8)
        

    def display_playlist(self, playlist:Playlist):
        column_headings = ["Danceability", "Energy", "Loudness", "Tempo"]
        tree = Treeview(self.master, columns=("Title", "Artist", "Album", "Danceability", "Energy", "Loudness", "Tempo"), show="headings")

        # Set column headings
        tree.heading("Title", text="Title")
        tree.heading("Artist", text="Artist")
        tree.heading("Album", text="Album")
        tree.heading("Danceability", text="Danceability")
        tree.heading("Energy", text="Energy")
        tree.heading("Loudness", text="Loudness")
        tree.heading("Tempo", text="Tempo")

        for song in playlist.songs:
            tree.insert("", "end", values=(song.title, song.artist, song.album, song.danceability, song.energy, song.loudness, song.tempo))

        # Set column alignment
        for col in column_headings:
            tree.column(col, anchor="center")  # Set anchor to center align the column values

        for column in column_headings:
            tree.column(column, width=80, anchor="center")
                

        tree.grid(row=9, column=0, columnspan=5)
    

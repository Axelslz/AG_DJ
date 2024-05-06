import random
from typing import List
from models import Song, Playlist
from statistics import mean


class Musicalizer:
    def __init__(
        self,
        population_size: int,
        crossover_rate: float,
        mutation_rate: float,
        num_generations: int,
        song_pool: List[Song],
        danceability: tuple,
        energy: tuple,
        loudness: tuple,
        tempo: tuple,
        playlist_size: int,
    ):
        self.population_size: int = population_size
        self.crossover_rate: float = crossover_rate
        self.mutation_rate: float = mutation_rate
        self.num_generations: int = num_generations

        self.song_pool: List[Song] = song_pool

        self.danceability_preference: tuple = danceability
        self.energy_preference: tuple = energy
        self.loudness_preference: tuple = loudness
        self.tempo_preference: tuple = tempo
        self.playlist_size: int = playlist_size

        self.best_cases = []
        self.avg_cases = []
        self.worst_cases = []

    def generate_initial_population(self) -> List[Playlist]:
        """
            Genera la población escogiendo N cantidad de canciones aleatorias del song_pool.
            N : playlist_size
        Returns:
            List[Playlist]: La lista de Playlist generada. El tamaño corresponden a population_size
        """
        return [
            Playlist(random.sample(self.song_pool, self.playlist_size))
            for _ in range(self.population_size)
        ]

    def fitness_function(self, playlist: Playlist) -> float:
        """
            Función de aptitud. Esta función llama a otras 3, las cuales califican a la playlist de acuerdo a:
            - Energia, Bailabilida, Tempo y sonoridad.
        Args:
            playlist (Playlist): playlist a evaluar

        Returns:
            float: Valor de aptitud de la función
        """
        total_score = 1.0
        total_score += self.get_energy_score(playlist)
        total_score += self.get_danceability_score(playlist)
        total_score += self.get_loudness_score(playlist)

        return total_score

    def get_energy_score(self, playlist: Playlist) -> float:
        """
            Calcula el valor de aptitud de acuerdo a la energía de la canción y el rango de energía configurado.
            - Compara la energía de una canción con la siguiente (evaluación de transición).
            - Compara la energía de una canción con el rango configurado.
        Args:
            playlist (Playlist): Playlist a evaluar

        Returns:
            float: valor de aptitud de la energía.
        """
        total_energy_score = 0.0
        energy_compatibility_weight = 10
        for i in range(1, len(playlist.songs)):
            current_energy = playlist.songs[i - 1].energy
            next_energy = playlist.songs[i].energy
            energy_score = (
                energy_compatibility_weight if current_energy == next_energy else 0.0
            )
            energy_score += (
                energy_compatibility_weight
                if self.energy_preference[0]
                < current_energy
                < self.energy_preference[1]
                else 0.0
            )
            total_energy_score += energy_score
        return total_energy_score

    def get_danceability_score(self, playlist: Playlist) -> float:
        """
            Calcula el valor de aptitud de acuerdo a la bailabilidad y al tempo de la canción.
            - Compara que la bailabilidad esté dentro del rango.
            - Compara que el tempo esté dentro del rango.
        Args:
            playlist (Playlist): Playlist a evaluar

        Returns:
            float: Valor de aptitud por bailabilidad
        """
        total_danceability_score: float = 0.0
        danceability_weight = 3
        tempo_weight = 10
        for song in playlist.songs:
            danceability_score = (
                danceability_weight
                if self.danceability_preference[0]
                < song.danceability
                < self.danceability_preference[1]
                else 0.0
            )
            tempo_score = (
                tempo_weight
                if self.tempo_preference[0] < song.tempo < self.tempo_preference[1]
                else 0.0
            )
            total_danceability_score += danceability_score + tempo_score
        return total_danceability_score

    def get_loudness_score(self, playlist: Playlist) -> float:
        """
            Calcula el valor de aptitud con base en el sonoridad de la canción.
            La sonoridad global de una canción se mide en decibelios (dB).
            Los valores de sonoridad se promedian en toda la pista y son útiles para comparar la sonoridad relativa de las pistas.
            La sonoridad es la cualidad de un sonido que es el principal correlato psicológico de la fuerza física (amplitud).
            Los valores suelen oscilar entre -60 y 0 db.
        Args:
            playlist (Playlist): Playlist a evaluar
        Returns:
            float: Valor de aptitud calculado
        """
        total_loudness_score = 0.0
        energy_compatibility_weight = 10
        for i in range(1, len(playlist.songs)):
            current_loudness = playlist.songs[i - 1].loudness
            loudness_score = (
                energy_compatibility_weight
                if self.loudness_preference[1]
                < current_loudness
                < self.loudness_preference[0]
                else 0.0
            )
            total_loudness_score += loudness_score
        return total_loudness_score

    def crossover(self, parent1: Playlist, parent2: Playlist) -> Playlist:
        """
            Realiza la 'Cruza' entre dos Playlist.
        Args:
            parent1 (Playlist): Playlist padre
            parent2 (Playlist): Playlist padre

        Returns:
            Playlist: Playlist resultante (offspring)
        """
        crossover_point = random.randint(1, len(parent1.songs) - 1)

        child_songs = parent1.songs[:crossover_point] + parent2.songs[crossover_point:]

        # Se eliminan canciones duplicadas
        unique_child_songs = list(set(child_songs))

        #  Se rellenan las canciones que falten con canciones seleccionadas al azar del fondo de canciones.
        remaining_songs = len(parent1.songs) - len(unique_child_songs)
        additional_songs = random.sample(self.song_pool, remaining_songs)
        unique_child_songs.extend(additional_songs)

        return Playlist(unique_child_songs)

    def mutate(self, playlist: Playlist) -> Playlist:
        """
            Se realiza la mutación de la Playlist.
        Args:
            playlist (Playlist): Playlist a mutar

        Returns:
            Playlist: Playlist mutada
        """
        mutated_playlist = Playlist(playlist.songs[:])  # Create a copy
        for i in range(len(mutated_playlist.songs)):
            if random.uniform(0, 1) < self.mutation_rate:
                mutated_playlist.songs[i] = random.choice(self.song_pool)
        return mutated_playlist


    def prune(self, population: List[Playlist]):
        return population[:self.population_size]


    def run(self) -> Playlist:

        population = self.generate_initial_population()

        for _ in range(self.num_generations):
            fitness_scores = [
                self.fitness_function(playlist) for playlist in population
            ]

            # Select playlists for crossover based on fitness scores
            selected_playlists = random.choices(
                population, weights=fitness_scores, k=self.population_size
            )

            # Perform crossover
            new_population = []
            for j in range(0, self.population_size, 2):
                parent1, parent2 = selected_playlists[j], selected_playlists[j + 1]
                if random.uniform(0, 1) < self.crossover_rate:
                    child1 = self.crossover(parent1, parent2)
                    child2 = self.crossover(parent2, parent1)
                else:
                    child1, child2 = parent1, parent2
                new_population.extend([child1, child2])

            # Perform mutation
            new_population = [self.mutate(playlist) for playlist in new_population]

            # Replace the old population with the new one

            population = new_population

            # Save avg, worst and best cases per generation
            fitness_scores = sorted(fitness_scores, reverse=True)
            self.best_cases.append(fitness_scores[0])
            self.avg_cases.append(mean([x for x in fitness_scores]))
            self.worst_cases.append(fitness_scores[-1])
            if len(population) > self.population_size:
                population = self.prune(population)

        # Return the best playlist from the final population
        best_playlist = max(
            population, key=lambda playlist: self.fitness_function(playlist)
        )
        
        return best_playlist

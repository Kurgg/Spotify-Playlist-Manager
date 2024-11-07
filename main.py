import spotipy
from spotipy.oauth2 import SpotifyOAuth
import numpy as np
from collections import Counter

class SpotifyPlaylistManager:
    def __init__(self, client_id, client_secret, redirect_uri, playlist_id):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                            client_secret=client_secret,
                                                            redirect_uri=redirect_uri,
                                                            scope="playlist-modify-private playlist-modify-public"))
        self.playlist_id = playlist_id

    def get_playlist_info(self):
        """
        Retrieves information about the tracks in the Spotify playlist.
        
        Returns:
            dict: A dictionary containing the genres, danceability, and energy of the tracks.
        """
        print("Analyzing the playlist, please wait...")
        results = self.sp.playlist_tracks(self.playlist_id)
        genres = []
        danceability = []
        energy = []
        
        for item in results['items']:
            track = item['track']
            artist_info = self.sp.artist(track['artists'][0]['id'])
            genres.extend(artist_info['genres'])
            
            audio_features = self.sp.audio_features([track['id']])[0]
            danceability.append(audio_features['danceability'])
            energy.append(audio_features['energy'])
        
        print("Playlist analysis complete.")
        return {
            'genres': genres,
            'danceability': danceability,
            'energy': energy
        }

    def get_average_playlist_info(self):
        """
        Calculates the average genre, danceability, and energy of the tracks in the playlist.
        
        Returns:
            dict: A dictionary containing the average genre, danceability, and energy.
        """
        playlist_info = self.get_playlist_info()
        
        genre_counts = Counter(playlist_info['genres'])
        average_genre = max(genre_counts, key=genre_counts.get)
        genre_subgenres = [genre for genre in playlist_info['genres'] if genre.startswith(average_genre)]
        
        average_danceability = np.mean(playlist_info['danceability'])
        average_energy = np.mean(playlist_info['energy'])
        
        return {
            'average_genre': average_genre,
            'average_genre_subgenres': genre_subgenres,
            'average_danceability': average_danceability,
            'average_energy': average_energy
        }

    def update_playlist(self, target_genre, target_danceability, target_energy):
        """
        Updates the Spotify playlist with new tracks that match the target genre, danceability, and energy.
        
        Args:
            target_genre (str): The target genre to search for new tracks.
            target_danceability (float): The target danceability range (0.0 to 1.0) for new tracks.
            target_energy (float): The target energy range (0.0 to 1.0) for new tracks.
        """
        print(f"Updating playlist with tracks matching: genre='{target_genre}', danceability={target_danceability:.2f}, energy={target_energy:.2f}")
        track_uris = self.get_matching_tracks(target_genre, target_danceability, target_energy)
        self.sp.playlist_replace_items(self.playlist_id, [])
        self.sp.playlist_add_items(self.playlist_id, track_uris)
        print("Playlist update complete.")

    def get_matching_tracks(self, target_genre, target_danceability, target_energy):
        """
        Retrieves a list of Spotify track URIs that match the target genre, danceability, and energy.
        
        Args:
            target_genre (str): The target genre to search for.
            target_danceability (float): The target danceability range (0.0 to 1.0) for new tracks.
            target_energy (float): The target energy range (0.0 to 1.0) for new tracks.
        
        Returns:
            list: A list of Spotify track URIs.
        """
        print(f"Searching for tracks matching: genre='{target_genre}', danceability={target_danceability:.2f}, energy={target_energy:.2f}")
        results = self.sp.search(q=f'genre:"{target_genre}"', type='track', limit=50)
        matching_tracks = []
        
        for track in results['tracks']['items']:
            audio_features = self.sp.audio_features([track['id']])[0]
            if (target_danceability - 0.1 <= audio_features['danceability'] <= target_danceability + 0.1 and
                target_energy - 0.1 <= audio_features['energy'] <= target_energy + 0.1):
                matching_tracks.append(track['uri'])
        
        print(f"Found {len(matching_tracks)} matching tracks.")
        return matching_tracks

def main():
    client_id = input("Enter your Spotify API Client ID: ")
    client_secret = input("Enter your Spotify API Client Secret: ")
    redirect_uri = input("Enter your Spotify API Redirect URI: ")
    playlist_id = input("Enter the Spotify Playlist ID: ")

    manager = SpotifyPlaylistManager(client_id, client_secret, redirect_uri, playlist_id)
    playlist_info = manager.get_average_playlist_info()

    print(f"The average genre of the playlist is: {playlist_info['average_genre']}")
    print(f"The average genre subgenres are: {', '.join(playlist_info['average_genre_subgenres'])}")
    print(f"The average danceability of the playlist is: {playlist_info['average_danceability']:.2f}")
    print(f"The average energy of the playlist is: {playlist_info['average_energy']:.2f}")

    update_playlist = input(f"Do you want to update the playlist with new tracks that match the current average genre, danceability, and energy? (y/n) ")
    if update_playlist.lower() == 'y':
        manager.update_playlist(playlist_info['average_genre'],
                                playlist_info['average_danceability'],
                                playlist_info['average_energy'])
    else:
        print("Playlist update cancelled.")

if __name__ == "__main__":
    main()
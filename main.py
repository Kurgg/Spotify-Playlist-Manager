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
            'genres': list(set(genres)),
            'danceability': danceability,
            'energy': energy
        }

    def get_average_playlist_info(self):
        """
        Calculates the average genre, danceability, and energy of the tracks in the playlist.
        
        Returns:
            dict: A dictionary containing the top 5 average genres, danceability, and energy.
        """
        playlist_info = self.get_playlist_info()
        
        genre_counts = Counter(playlist_info['genres'])
        top_genres = [genre for genre, count in genre_counts.most_common(5)]
        
        average_danceability = np.mean(playlist_info['danceability'])
        average_energy = np.mean(playlist_info['energy'])
        
        return {
            'top_genres': top_genres,
            'average_danceability': average_danceability,
            'average_energy': average_energy
        }

    def update_playlist(self, target_genres, target_danceability, target_energy, min_tracks=20, max_tracks=20):
        """
        Updates the Spotify playlist with new tracks that match the target genres, danceability, and energy.
        
        Args:
            target_genres (list): The target genres to search for new tracks.
            target_danceability (float): The target danceability range (0.0 to 1.0) for new tracks.
            target_energy (float): The target energy range (0.0 to 1.0) for new tracks.
            min_tracks (int): The minimum number of tracks to add to the playlist (default is 20).
            max_tracks (int): The maximum number of tracks to add to the playlist (default is 20).
        """
        print(f"Updating playlist with tracks matching: genres={', '.join(target_genres)}, danceability={target_danceability:.2f}, energy={target_energy:.2f}")
        track_uris = self.get_matching_tracks(target_genres, target_danceability, target_energy, min_tracks)
        
        # Get current playlist tracks
        current_tracks = self.sp.playlist_tracks(self.playlist_id)['items']
        current_track_uris = [item['track']['uri'] for item in current_tracks]
        
        # Filter out duplicate tracks
        new_track_uris = [uri for uri in track_uris if uri not in current_track_uris]
        
        # Limit the number of new tracks to the maximum
        new_track_uris = new_track_uris[:max_tracks]
        
        self.sp.playlist_replace_items(self.playlist_id, new_track_uris)
        print(f"Playlist updated with {len(new_track_uris)} new tracks.")

    def get_matching_tracks(self, target_genres, target_danceability, target_energy, min_tracks=20):
        """
        Retrieves a list of Spotify track URIs that match the target genres, danceability, and energy.
        
        Args:
            target_genres (list): The target genres to search for.
            target_danceability (float): The target danceability range (0.0 to 1.0) for new tracks.
            target_energy (float): The target energy range (0.0 to 1.0) for new tracks.
            min_tracks (int): The minimum number of tracks to return.
        
        Returns:
            list: A list of Spotify track URIs.
        """
        print(f"Searching for tracks matching: genres={', '.join(target_genres)}, danceability={target_danceability:.2f}, energy={target_energy:.2f}")
        matching_tracks = []
        
        # Start with the target range and expand if needed to find at least min_tracks
        danceability_range = 0.1
        energy_range = 0.1
        
        while len(matching_tracks) < min_tracks:
            query = ' OR '.join([f'genre:"{genre}"' for genre in target_genres])
            results = self.sp.search(q=query, type='track', limit=50)
            
            for track in results['tracks']['items']:
                audio_features = self.sp.audio_features([track['id']])[0]
                if (target_danceability - danceability_range <= audio_features['danceability'] <= target_danceability + danceability_range and
                    target_energy - energy_range <= audio_features['energy'] <= target_energy + energy_range):
                    matching_tracks.append(track['uri'])
            
            if len(matching_tracks) < min_tracks:
                danceability_range += 0.1
                energy_range += 0.1
        
        print(f"Found {len(matching_tracks)} matching tracks.")
        return matching_tracks

def main():
    client_id = input("Enter your Spotify API Client ID: ")
    client_secret = input("Enter your Spotify API Client Secret: ")
    redirect_uri = input("Enter your Spotify API Redirect URI: ")
    playlist_id = input("Enter the Spotify Playlist ID: ")

    manager = SpotifyPlaylistManager(client_id, client_secret, redirect_uri, playlist_id)
    playlist_info = manager.get_average_playlist_info()

    print(f"The top 5 genres of the playlist are: {', '.join(playlist_info['top_genres'])}")
    print(f"The average danceability of the playlist is: {playlist_info['average_danceability']:.2f}")
    print(f"The average energy of the playlist is: {playlist_info['average_energy']:.2f}")

    update_playlist = input(f"Do you want to update the playlist with new tracks that match the current top 5 genres, danceability, and energy? (y/n) ")
    if update_playlist.lower() == 'y':
        manager.update_playlist(playlist_info['top_genres'],
                                playlist_info['average_danceability'],
                                playlist_info['average_energy'])
    else:
        print("Playlist update cancelled.")

if __name__ == "__main__":
    main()

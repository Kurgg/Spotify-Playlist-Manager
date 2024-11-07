# Spotify Playlist Manager

This is a Python script that allows you to manage and update your Spotify playlists based on the average genre, danceability, and energy of the tracks in the playlist.

## Features

- Retrieves information about the tracks in a Spotify playlist, including genres, danceability, and energy.
- Calculates the average genre, danceability, and energy of the tracks in the playlist.
- Updates the playlist with new tracks that match the target genre, danceability, and energy.

## Requirements

- Python 3.6 or later
- Spotipy library (`pip install spotipy`)
- Numpy library (`pip install numpy`)
- Ipywidgets library (`pip install ipywidgets`)

## Usage

1. Clone the repository and navigate to the project directory.
2. Run the script:

```
python spotify_playlist_manager.py
```

3. Enter your Spotify API Client ID, Client Secret, Redirect URI, and Playlist ID when prompted.
4. The script will analyze the playlist and display the average genre, danceability, and energy.
5. You'll be asked if you want to update the playlist with new tracks that match the current average values. Enter "y" to proceed or "n" to cancel.

## Functions

### `SpotifyPlaylistManager`

This is the main class that manages the Spotify playlist.

#### `__init__(self, client_id, client_secret, redirect_uri, playlist_id)`
- Initializes the class with the necessary Spotify API credentials and the playlist ID.

#### `get_playlist_info(self)`
- Retrieves information about the tracks in the Spotify playlist, including genres, danceability, and energy.
- Returns a dictionary containing the retrieved information.

#### `get_average_playlist_info(self)`
- Calculates the average genre, danceability, and energy of the tracks in the playlist.
- Returns a dictionary containing the average values.

#### `update_playlist(self, target_genre, target_danceability, target_energy)`
- Updates the Spotify playlist with new tracks that match the target genre, danceability, and energy.

#### `get_matching_tracks(self, target_genre, target_danceability, target_energy)`
- Retrieves a list of Spotify track URIs that match the target genre, danceability, and energy.

### `main()`
- Prompts the user for the necessary Spotify API credentials and the playlist ID.
- Creates a `SpotifyPlaylistManager` instance and retrieves the average playlist information.
- Displays the average genre, danceability, and energy.
- Asks the user if they want to update the playlist with new tracks that match the current average values.

## Contributing

If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

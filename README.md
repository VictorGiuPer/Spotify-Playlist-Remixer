## Spotify-Playlist-Remixer

**Description**
This Python project interfaces with the Spotify API to offer sophisticated tools for music playlist creation, analysis, and recommendation. It uniquely enables users to generate new Spotify playlists by analyzing the audio features of an existing playlist, ensuring the new playlist matches the mood, style, and characteristics of the original.

**Key Features**
0. Connect to Spotify API
init_spotify_api.py: Establishes the initial connection to Spotify's API by fetching and setting up the authentication token, which is crucial for making authorized requests to Spotify's endpoints. This file supports all other scripts in your repository by ensuring they have the necessary credentials to interact with the Spotify API

1. Audio Feature Analysis
analyze_playlist_audio_features.py: This file is central to analyzing audio features. It takes an existing playlist, calculates the range of audio features like energy, danceability, tempo, and more, and uses these insights to inform the creation of new playlists that share a similar audio profile.

2. Dynamic Playlist Creation
create_playlist_from_analysis.py: Utilizes the analysis provided by analyze_playlist_audio_features.py to create new playlists. This script directly interacts with Spotify's API to dynamically generate playlists that match the audio feature profile of a user-selected playlist and genre (+market).

3. Top Artists and Related Artists Discovery
fetch_artists.py: Fetches details about top artists from Spotify, focusing on a specific genre. It helps in discovering new artists by providing information on their popularity and genres.
search_tracks.py: This script includes functionality to fetch related artists based on the top artists discovered, thereby aiding in the exploration of musical connections and expanding the user's musical horizons.

4. Music Recommendations
generate_recommendations.py: Generates music recommendations based on user-selected genres, market preferences, and audio metrics derived from analyze_playlist_audio_features.py. This script represents the core logic behind curating personalized music recommendations

6. Mood-Based Search:
classify_moods.py: This file classifies searches for songs from different moods and creates mood-based playlists.


**Installation**
Prerequisites
- Python 3.6 or higher
- A Spotify Developer account and API credentials

------------

**Contributing**
- Contributions to improve the project are welcome. Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (git checkout -b feature/AmazingFeature).
- Commit your changes (git commit -m 'Add some AmazingFeature').
- Push to the branch (git push origin feature/AmazingFeature).
- Open a pull request.

Acknowledgments
Spotify Web API: https://developer.spotify.com/
Python Requests Library: https://pypi.org/project/requests/

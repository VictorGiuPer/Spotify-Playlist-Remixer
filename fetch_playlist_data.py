from init_spotify_api import headers, token
from search_tracks import multiple_audio_feat
from requests import post, get
import json
import pandas as pd
import csv

# Predefined Spotify playlist IDs for different genres
afrobeats = "4JJgffqENbOlwaeOcUzNbt"
portugues = "6r22I00vHMCxhneAGtiPNT"
drum_and_bass = "3djIt439HKrISGRydpmNWn"


# GET TRACKS FROM GIVEN PLAYLIST_ID
def get_playlist_tracks(id_p):
    """
    Fetches the tracks of a Spotify playlist and extracts their ID, popularity, and name.

    This function queries the Spotify Web API for the tracks in a specified playlist.
    For each track, it extracts the track's ID, popularity score, and name, storing
    these in a dictionary keyed by the track ID.

    Parameters:
    - playlist_id (str): The Spotify ID for the playlist.

    Returns:
    - dict: A dictionary where each key is a track ID, and the value is a list containing
            the track's popularity score and name, in that order.
    """
    song_id_pop = {}
    url = f"https://api.spotify.com/v1/playlists/{id_p}/tracks?market=BE"
    result = get(url, headers=headers)
    result = json.loads(result.content)["items"]
    for i in range(len(result)):
        song_id_pop[result[i]["track"]["id"]] = [
            result[i]["track"]["popularity"],
            result[i]["track"]["name"],
        ]
    print(song_id_pop)
    return song_id_pop


playlist_tracks = get_playlist_tracks(drum_and_bass)
# ____________________________


# FUNCTION CALL FROM SEARCH FILE
playlist_info = multiple_audio_feat(token=token, headers=headers, ids=playlist_tracks)
# ____________________________


def playlist_to_csv(playlist, song_names_pop, playlist_name):
    """
    Generates a CSV file from playlist tracks's data,
    enriched with song names and popularity scores.

    Parameters:
    - playlist (dict): Mapping of track IDs to their features.
    - song_names_pop (dict): Mapping of track IDs to their popularity score and name.
    - playlist_name (str): Base name for the output CSV file.

    Updates the playlist dictionary with song names and popularity from song_names_pop,
    then writes the complete track information to a CSV named `playlist_name.csv`,
    with predefined columns for track features including name, ID, and popularity.
    """
    print(playlist)
    head = [
        "name",
        "id",
        "popularity",
        "danceability",
        "energy",
        "loudness",
        "speechiness",
        "acousticness",
        "instrumentalness",
        "liveness",
        "valence",
        "tempo",
    ]

    for track_id, track_info in song_names_pop.items():
        popularity, song_name = track_info
        if track_id in playlist:
            playlist[track_id]["name"] = song_name
            playlist[track_id]["popularity"] = popularity
    # Determine the CSV header based on the keys of the first item in playlist (assuming all items have the same keys)
    with open(
        str(playlist_name + ".csv"), mode="w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=head)
        writer.writeheader()

        # Write each track's features, ensuring they follow the order in 'head'
        for track_id, features in playlist.items():
            # Create a row dictionary starting with the track ID, then update it with the rest of the features
            row = {"id": track_id}
            row.update(features)
            writer.writerow(row)


playlist_to_csv(playlist_info, playlist_tracks, "drum_and_bass")
# ____________________________

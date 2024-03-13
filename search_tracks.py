from requests import post, get
import json

from init_spotify_api import token, headers


# get song name given the ID
def single_song_info(token, headers, id):
    """
    Retrieves the name and primary artist of a single track given its Spotify ID.

    Parameters:
        token (str): Authentication token for Spotify API.
        headers (dict): Headers for the API request, including authorization.
        id (str): The Spotify ID of the track.

    Returns:
        tuple: A tuple containing the name of the song and the name of its primary artist.
    """

    # Construct the URL for the API request using the track ID
    url = f"https://api.spotify.com/v1/tracks/{id}?market=US"

    # Make the GET request to Spotify API
    result = get(url, headers=headers)

    # Parse the JSON response to extract song and artist names
    song_name = json.loads(result.content)["name"]
    artist_name = json.loads(result.content)["artists"][0]["name"]
    # artist_id = json.loads(result.content)["artists"][0]["id"]

    return song_name, artist_name  # , artist_id

    # song_n, song_a = single_song_info(
    token = token, headers = headers, id = "5wG3HvLhF6Y5KTGlK0IW3J"


def multiple_song_info(token, headers, ids):
    """
    Retrieves details for multiple tracks based on their Spotify IDs.

    Parameters:
        token (str): Authentication token for Spotify API.
        headers (dict): Headers for the API request, including authorization.
        ids (list): A list of Spotify track IDs.

    Returns:
        dict: A dictionary with track IDs as keys and a list containing the track's name and primary artist as values.
    """
    songs = {}
    print(ids)
    ids_string = ""
    # Concatenate track IDs into a comma-separated string for the API request
    for id in ids.keys():
        ids_string += str(id) + ","

    # Construct the URL for fetching details of multiple tracks
    url = f"https://api.spotify.com/v1/tracks?market=US&ids={ids_string}"

    # Make the GET request to Spotify API
    result = get(url, headers=headers)
    result = json.loads(result.content)

    # Iterate through the response to populate the songs dictionary
    for id in ids:
        for k in range(len(ids)):
            artist_name = result["tracks"][k]["artists"][0]["name"]
            song_name = result["tracks"][k]["name"]

            songs[id] = [
                song_name,
                artist_name,
            ]

    return songs

    # songs_list = multiple_song_info(
    token = (token,)
    headers = (headers,)
    ids = (
        ["5wG3HvLhF6Y5KTGlK0IW3J", "4Enk3Ss0Mp6L8eCgL2WbEv", "5iwz1NiezX7WWjnCgY5TH4"],
    )


def multiple_audio_feat(token, headers, ids):
    """
    Fetches audio features for multiple tracks from Spotify and organizes them into a dictionary.

    This function makes a single API call to Spotify's "Get Audio Features for Several Tracks"
    endpoint using a list of track IDs. It then parses the response to create a structured
    dictionary mapping each track ID to its audio features.

    Parameters:
    - token (str): Spotify API authentication token.
    - headers (dict): Request headers containing authorization information.
    - ids (dict): A dictionary where keys are Spotify track IDs.

    Returns:
    - dict: A dictionary mapping track IDs to their respective audio features.

    Each entry in the return dictionary contains a subset of predefined audio features
    (e.g., danceability, energy) for the corresponding track.
    """

    # Initialize a dictionary to hold the audio features for each track
    playlist_info = {id: {} for id in ids.keys()}

    # Define the audio features to be retrieved
    features = [
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
    # Create ID's string for API call
    ids_string = ""
    for id in ids.keys():
        ids_string += str(id) + ","
    # Construct the URL for the API request
    url = f"https://api.spotify.com/v1/audio-features?market=US&ids={ids_string}"

    # Make the GET request to Spotify API
    result = get(url, headers=headers)
    result = json.loads(result.content)["audio_features"]

    # Create ID's list
    ids_list = list(ids.keys())

    # loop over amount of songs
    for i, result_k in enumerate(result):
        # Check if result_k is not None
        if result_k:
            # Use index to get the corresponding track ID
            track_id = ids_list[i]
            for key in features:
                if key in result_k:
                    audio_value = result_k[key]
                    # Assign the value directly to the corresponding key
                    playlist_info[track_id][key] = audio_value

    return playlist_info

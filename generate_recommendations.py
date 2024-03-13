from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import pandas as pd
import matplotlib.pyplot as plt
import time

# Import required modules and variables from other scripts for
# Spotify API access and track searching
from init_spotify_api import token, headers
from search_tracks import single_song_info, multiple_song_info


def choose_genre_seed():
    """
    Prompts the user to choose a genre and a market from available Spotify genre seeds and markets.

    The function makes two separate API calls to Spotify to fetch the available genre seeds and markets,
    then prompts the user to make a selection from each list.

    Returns:
        tuple: A tuple containing the user's genre choice and market choice.
    """

    # Fetch available genre seeds from Spotify
    seeds_url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    genre_result = get(url=seeds_url, headers=headers)
    genre_seeds = json.loads(genre_result.content)
    print(genre_seeds["genres"])

    # Prompt the user to choose a genre from the fetched list
    genre_choice = ""
    while genre_choice not in genre_seeds["genres"]:
        genre_choice = input("Choose a genre: ")

    # Fetch available markets from Spotify
    seeds_url = "https://api.spotify.com/v1/markets"
    market_result = get(url=seeds_url, headers=headers)
    markets = json.loads(market_result.content)
    print(markets["markets"])

    # Prompt the user to choose a market from the fetched list
    market_choice = ""
    while market_choice not in markets["markets"]:
        market_choice = input("Choose a market: ")

    return genre_choice, market_choice


# genre_choice, market_choice = choose_genre_seed()

# Example of manually setting genre and market choice without user input
genre_choice = "soul"
market_choice = "BR"

# print(genre_choice, market_choice)


def genre_recommendations(genre_choice, market_choice, audio_metrics):
    """
    Generates music recommendations based on a specified genre, market, and set of audio metrics.

    Parameters:
        genre_choice (str): The chosen genre for recommendation.
        market_choice (str): The chosen market (country) for the recommendation.
        audio_metrics (DataFrame): A DataFrame containing audio metrics which will inform the recommendation.

    Returns:
        dict: A dictionary containing the recommended tracks and their details.
    """
    # Transpose the audio metrics DataFrame to access features easily
    audio_metrics = audio_metrics.T
    print(genre_choice, market_choice)

    # Initialize a dictionary to store the recommendation parameters
    params = {}

    # Populate the parameters dictionary with minimum, maximum,
    # and target values for each audio feature
    for feature in audio_metrics.index:
        min_value = audio_metrics.loc[feature, "min"]
        max_value = audio_metrics.loc[feature, "max"]
        median_value = audio_metrics.loc[feature, "Median"]
        target_value = median_value

        params[f"min_{feature}"] = min_value
        params[f"max_{feature}"] = max_value
        params[f"target_{feature}"] = target_value

    parameter_ranges = {
        "limit": (1, 100),
        "market": "ISO 3166-1 alpha-2 country code",
        "seed_artists": "Spotify IDs",
        "seed_genres": "Genres",
        "seed_tracks": "Spotify IDs",
        "min_acousticness": (0, 1),
        "max_acousticness": (0, 1),
        "target_acousticness": (0, 1),
        "min_danceability": (0, 1),
        "max_danceability": (0, 1),
        "target_danceability": (0, 1),
        "min_duration_ms": (0, None),  # None represents no upper limit
        "max_duration_ms": (0, None),
        "target_duration_ms": (0, None),
        "min_energy": (0, 1),
        "max_energy": (0, 1),
        "target_energy": (0, 1),
        "min_instrumentalness": (0, 1),
        "max_instrumentalness": (0, 1),
        "target_instrumentalness": (0, 1),
        "min_key": (0, 11),
        "max_key": (0, 11),
        "target_key": (0, 11),
        "min_liveness": (0, 1),
        "max_liveness": (0, 1),
        "target_liveness": (0, 1),
        "min_loudness": (None, 0),  # None represents no lower limit
        "max_loudness": (None, 0),
        "target_loudness": (None, 0),
        "min_mode": (0, 1),
        "max_mode": (0, 1),
        "target_mode": (0, 1),
        "min_popularity": (0, 100),
        "max_popularity": (0, 100),
        "target_popularity": (0, 100),
        "min_speechiness": (0, 1),
        "max_speechiness": (0, 1),
        "target_speechiness": (0, 1),
        "min_tempo": (0, None),
        "max_tempo": (0, None),
        "target_tempo": (0, None),
        "min_time_signature": (0, 11),
        "max_time_signature": (0, 11),
        "target_time_signature": (0, 11),
        "min_valence": (0, 1),
        "max_valence": (0, 1),
        "target_valence": (0, 1),
    }

    # Integer Parameters
    integer_parameters = [
        "limit",
        "min_duration_ms",
        "max_duration_ms",
        "target_duration_ms",
        "min_key",
        "max_key",
        "target_key",
        "min_mode",
        "max_mode",
        "target_mode",
        "min_time_signature",
        "max_time_signature",
        "target_time_signature",
        "min_popularity",
        "max_popularity",
        "target_popularity",
    ]

    # Number Parameters (Floating Point)
    number_parameters = [
        "min_acousticness",
        "max_acousticness",
        "target_acousticness",
        "min_danceability",
        "max_danceability",
        "target_danceability",
        "min_energy",
        "max_energy",
        "target_energy",
        "min_instrumentalness",
        "max_instrumentalness",
        "target_instrumentalness",
        "min_liveness",
        "max_liveness",
        "target_liveness",
        "min_loudness",
        "max_loudness",
        "target_loudness",
        "min_speechiness",
        "max_speechiness",
        "target_speechiness",
        "min_tempo",
        "max_tempo",
        "target_tempo",
        "min_valence",
        "max_valence",
        "target_valence",
    ]

    # Construct the URL string
    base_url = f"https://api.spotify.com/v1/recommendations?limit=100&market={str(market_choice)}&seed_genres={str(genre_choice)}"
    # Initialize an empty list to hold the formatted parameter strings
    formatted_params = []

    # Loop through each parameter and format it based on its type and range
    for key, value in params.items():
        # Skip the parameters you don't want to include in the URL
        if key in [
            "min_key",
            "max_key",
            "target_key",
            "min_mode",
            "max_mode",
            "target_mode",
            "min_time_signature",
            "max_time_signature",
            "target_time_signature",
            "min_popularity",
            "max_popularity",
            "target_popularity",
        ]:
            continue

        # Get the range for the current parameter
        range_info = parameter_ranges.get(key)

        if range_info is None:
            # Skip parameters without range information
            continue

        if isinstance(range_info, tuple):
            # If range info is a tuple, it represents a numeric range
            min_value, max_value = range_info
            try:
                # Convert value to the appropriate type and validate it against the range
                if key in integer_parameters:
                    formatted_value = int(value)
                elif key in number_parameters:
                    formatted_value = round(float(value), 1)
                else:
                    formatted_value = str(value)

                if min_value is not None and formatted_value < min_value:
                    formatted_value = min_value
                elif max_value is not None and formatted_value > max_value:
                    formatted_value = max_value

                # Append the formatted parameter string to the list
                formatted_params.append(f"{key}={formatted_value}")

            except (ValueError, TypeError):
                # Handle invalid values
                continue

        elif isinstance(range_info, str):
            # If range info is a string, it represents a textual range or format
            # You can handle these cases as per your specific requirements
            # For now, we'll just convert the value to string and append
            formatted_params.append(f"{key}={value}")

    # Join the formatted parameter strings with '&' to create the URL parameters string
    url_params = "&".join(formatted_params)

    # Construct the final URL
    url_rec = f"{base_url}&{url_params}"

    # Send the request and parse the response
    recommendation_result = get(url=url_rec, headers=headers)
    recommendation = json.loads(recommendation_result.content)
    print(recommendation)
    print(len(recommendation["tracks"]))
    return recommendation


# TO DO
# Find way to search for songs with keywords
# Code in advance the create playlist feature

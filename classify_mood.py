"""
This script aims to classify songs into predefined moods based on Spotify's 
track features and create mood-based playlists. It searches for tracks 
matching specific keywords associated with each mood, across different markets, 
to ensure a diverse selection. The script then organizes the found tracks into 
mood-based categories, facilitating the creation of playlists that cater to 
various emotional states or settings.
"""

from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import pandas as pd
import matplotlib.pyplot as plt
import time

# Import Spotify API token and headers for authentication
from init_spotify_api import token, headers
from search_tracks import single_song_info, multiple_song_info

# Define mood categories and associated search keywords
mood_search_terms = {
    "Sunset Serenade": [
        "calm",
        "serene",
        "acoustic",
        "soft rock",
        "easy listening",
    ],
    "Starry Night Whispers": [
        "ambient",
        "chill",
        "soft electronic",
        "introspective",
        "dream pop",
    ],
    "Urban Jungle Rhythms": [
        "upbeat",
        "electronic",
        "hip hop",
        "urban pop",
        "dance",
    ],
    "Bohemian Rhapsodies": [
        "eclectic",
        "alternative",
        "folk",
        "indie",
        "world music",
    ],
    "Retro Futurism": ["synthwave", "80s pop", "electronic", "vaporwave", "retro"],
    "Ethereal Echoes": ["ambient", "ethereal", "dreamy", "chillstep", "airy"],
    "Vintage Vibes": ["vintage", "retro", "jazz", "soul", "oldies"],
    "Cosmic Contemplations": [
        "space rock",
        "ambient",
        "chillstep",
        "electronic",
        "experimental",
    ],
    "Groovy Getaway": ["tropical house", "reggae", "samba", "beach", "summer hits"],
    "Rainy Day Reverie": ["melancholic", "piano", "soft jazz", "acoustic", "chill"],
    "Soulful Spirits": ["soul", "r&b", "gospel", "blues", "jazz"],
    "Electro Enigma": ["electronic", "edm", "house", "techno", "trance"],
}

# Define a list of markets to search in, aiming for a wide geographical diversity
market_list = ["US", "ES", "JP", "CN", "SA", "FR", "BR", "NL", "ZA"]


# Gets 5 songs for each mood
def get_mood_songs(headers=headers, mood_search_terms=mood_search_terms):
    """
    Fetches songs that match the mood search terms from various markets.

    :param headers: Authorization headers for Spotify API requests.
    :param mood_search_terms: Dictionary mapping moods to lists of search keywords.
    :return: Dictionary mapping moods to lists of track IDs.
    """
    url = "https://api.spotify.com/v1/search"
    mood_track_ids = {}
    # loop over moods
    for mood, search_t in mood_search_terms.items():
        print(search_t)
        mood_track_ids[mood] = []
        # loop over keyword in each mood
        for keyword in mood_search_terms[mood]:
            for market in market_list:
                # create query
                query_url = url + f"?q={keyword}&type=track&market={market}&limit=3"
                result = get(query_url, headers=headers)
                # dict -> dict -> list -> dict
                # get 5 ID's -> name and other info get later
                for nr in range(3):
                    track_id = json.loads(result.content)["tracks"]["items"][nr]["id"]
                    print(track_id)

                    # check for duplicates
                    if track_id not in mood_track_ids[mood]:
                        mood_track_ids[mood].append(track_id)
        time.sleep(2)  # Respectful pause to avoid rate limits

    # Check if ID's have been passed
    # print(mood_track_ids["Sunset Serenade"])
    return mood_track_ids


def to_pd(mood_track_ids):
    """
    Converts mood_track_ids to a Pandas DataFrame for further processing.

    :param mood_track_ids: Dictionary of mood categories to track IDs.
    :return: A dictionary of DataFrames for each mood and a combined DataFrame.
    """
    df_dict = {}
    for mood in mood_track_ids:
        print(f"Creating {mood} Data Dictionary...")
        data_dict = {"Section": [], "Song Name": [], "Artist Name": []}
        id_list = []

        print("Gathering ID's...")
        for id in mood_track_ids[mood]:
            id_list.append(str(id))

        print("Fetching Song Name & Artist Name...")
        song_name, artist_name = multiple_song_info(
            token=token, headers=headers, ids=id_list
        )
        data_dict["Section"].append(mood)
        data_dict["Song Name"].append(song_name)
        data_dict["Artist Name"].append(artist_name)

        dataframe = pd.DataFrame(data_dict)
        df_dict[mood] = dataframe
        time.sleep(3)

    return df_dict, dataframe


mood_songs = get_mood_songs()

# Convert track IDs to DataFrames for easier manipulation and visualization
df_dict, dataframe = to_pd(mood_songs)

# Specify the filepath for saving the mood-based playlists
filepath = "moods.csv"

# print(dataframe.head())


# Writes passed df's to passed filepath
def write_csv(df_dict, filepath=filepath):
    append_mode = "a"

    # loop over each mood df in dict
    for df_name, df in df_dict.items():
        # initialize last_section value
        last_section = None

        if not os.path.isfile(filepath):
            with open(filepath, mode="w", newline="") as csv_file:
                df.to_csv(csv_file, header=True, index=False)
        else:
            existing_data = pd.read_csv(filepath)

            section_positions = {}
            current_section = None

            for idx, row in existing_data.iterrows():
                if row["Section"] == "Section":
                    current_section = row["Section"]
                    section_positions[current_section] = idx

            if last_section != df_name:
                append_mode = "w"

            new_songs = df[~df["Song Name"].isin(existing_data["Song Name"])]

            existing_data = pd.concat(
                [existing_data, new_songs], ignore_index=True, sort=False
            )

            existing_data.to_csv(filepath, mode=append_mode, header=True, index=False)

        print(f"Appended {df_name} to CSV.")


write_csv(df_dict=df_dict)


# loads csv data into dataframes per mood
def load_csv(filepath, mood_search_terms):
    moods_raw = pd.read_csv(filepath, header=0)
    print(moods_raw.head())

    moods = {}
    for section in moods_raw["Section"].unique():
        moods[section] = moods_raw[moods_raw["Section"] == section].copy()

    print(moods)
    return moods


# load_csv(filepath=filepath, mood_search_terms=mood_search_terms)

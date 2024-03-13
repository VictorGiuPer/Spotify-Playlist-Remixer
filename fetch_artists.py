from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import pandas as pd
import matplotlib.pyplot as plt

# Import functions for Spotify API authentication
from init_spotify_api import token, headers


def top_artists(token=token, headers=headers):
    """
    Fetches top reggaeton artists from the Spotify API and returns their details.

    :param token: Spotify API token for authorization.
    :param headers: Request headers including the authorization token.
    :return: A DataFrame with artist details including name, Spotify ID, popularity, and genres.
    """
    url = "https://api.spotify.com/v1/search"
    query = "?q=genre=reggeaton&type=artist&limit=30&market=NL"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    artists_data = []
    for artist in json_result:
        artists_data.append(
            {
                "Artist Name": artist["name"],
                "Spotify ID": artist["id"],
                "Popularity": artist["popularity"],
                "Genres": ", ".join(artist["genres"]),
            }
        )
    artists_data = pd.DataFrame(artists_data)
    return artists_data


artists_df = top_artists()
print(artists_df.head())
print(len(artists_df))


def plot_popularity(artists_data=artists_df):
    """
    Plots a scatter graph of artist popularity scores based on their ranking.

    :param artists_data: DataFrame containing artists and their popularity scores.
    """
    plt.scatter(artists_data.index, artists_data["Popularity"], color="g")
    plt.xlabel("Position in the ranking")
    plt.ylabel("Popularity Score")
    plt.show()


plot_popularity()


# Retrieves related artists for each artist in the provided DataFrame using Spotify API.
# Returns: DataFrame with names of related artists.
def get_related_artists(artist_data=artists_df):
    """
    Fetches related artists for each artist in the provided DataFrame.

    :param artist_data: DataFrame with artist Spotify IDs.
    :return: A DataFrame with names of related artists for each main artist.
    """
    rel_artist = []
    # loop through ID's to get related artist url for each
    for id in artist_data["Spotify ID"]:
        url = f"https://api.spotify.com/v1/artists/{id}/related-artists"
        result = get(url, headers=headers)
        json_result = json.loads(result.content)["artists"]

        # 20 related artists per artists -> 600 (599)

        for rel in json_result:
            rel_artist.append(
                {
                    "Artist Name": rel["name"],
                }
            )
    rel_artist = pd.DataFrame(rel_artist)
    print(rel_artist.head())
    return rel_artist


related_artists = get_related_artists()


def order_rel_artists(related_artists=related_artists, artist_data=artists_df):
    """
    Associates related artists with the main artists in the original DataFrame.

    :param related_artists: DataFrame with names of related artists.
    :param artist_data: Original DataFrame of main artists.
    """
    artist_data["Related Artists"] = ""
    print(artist_data["Artist Name"][0])
    for idx, rel in enumerate(related_artists["Artist Name"]):
        connector = idx // 20
        if artist_data.loc[connector, "Related Artists"]:
            artist_data.loc[connector, "Related Artists"] += ", "
        artist_data.loc[connector, "Related Artists"] += rel

    print(artist_data.head())


order_rel_artists()

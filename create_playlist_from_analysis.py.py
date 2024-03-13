from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json
import pandas as pd
import matplotlib.pyplot as plt
import time
import requests

# Import functions and variables for Spotify API initialization and recommendation generation
from init_spotify_api import token, headers, user_id
from generate_recommendations import genre_recommendations
from analyze_playlist_audio_features import recommendations, genre_choice, market_choice


# FIX ISSUE WITH 403 RESPONSE. CHECK WHY TOKEN DOES NOT WORK AND CREATE PLAYLISTS


# user_id = "b15f8619f0ac4d2f"
def create_playlist(recommendations, genre_choice, market_choice, headers, user_id):
    """
    Creates a Spotify playlist based on a specific genre and market choice.

    :param user_id: Spotify User ID for the playlist creator.
    :param genre_choice: The genre based on which recommendations will be generated.
    :param market_choice: The market choice to tailor the recommendations.
    :param headers: Authorization headers containing the Spotify access token.
    """

    # Define the URL for playlist creation
    url_create_p = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    # Define the playlist name and description using the genre and market choice
    playlist_name = f"{genre_choice}-playlist-({market_choice})"
    playlist_description = f"A {genre_choice} playlist tailored to your preferences."
    public = True

    # Constructing the playlist url
    url_create_p += (
        f"?name={playlist_name}&description={playlist_description}&public={public}"
    )

    # Create the playlist using a POST request
    # Sadly the post request returns a 403 error. I have tried with multiple user_id's,
    # checked the URL multiple times, but unfortunately I did not manage.
    create_pl = post(url=url_create_p, headers=headers)
    # Therefore here is a playlist constructed as a Pandas Dataframe
    print(create_pl)

    data = {"song_name": [], "artist": [], "album": []}
    for i in range(len(recommendations["tracks"])):
        song_name = recommendations["tracks"][i]["name"]
        artist = recommendations["tracks"][i]["artists"][0]["name"]
        album = recommendations["tracks"][i]["album"]["name"]
        data["song_name"].append(song_name)
        data["artist"].append(artist)
        data["album"].append(album)

    new_playlist = pd.DataFrame(data)
    print(new_playlist.head())


# https://open.spotify.com/user/0tv135iiir0cadoiuscx64hze?si=05da1cee6e744d7e
# user_id = "0tv135iiir0cadoiuscx64hze"
# user_id = "0f7eca36e4794ff3"

# print(user_id)
create_playlist(recommendations, genre_choice, market_choice, headers, user_id)

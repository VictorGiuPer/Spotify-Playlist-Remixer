from dotenv import load_dotenv
import os
from requests import post, get
import base64
import json


def get_token():
    """
    Retrieves an access token from Spotify Web API using the client credentials flow.

    The client ID and client secret are obtained from environment variables,
    encoded, and used to authenticate. The function then requests an access
    token from Spotify's token endpoint.

    Returns:
        str: An access token for the Spotify Web API.
    """
    # Load environment variables
    load_dotenv()
    # Retrieve client ID and secret from .env file
    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")
    # Encode client credentials and prepare them for header
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    # Spotify URL for requesting an access token
    url = "https://accounts.spotify.com/api/token"

    # Headers including the encoded client credentials
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    # Data payload specifying the grant type
    data = {"grant_type": "client_credentials"}
    # POST request to get the token
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    # Extract the access token from response
    token = json_result["access_token"]
    print(json_result["token_type"])
    print(token)
    return token


def get_auth_headers(token):
    """
    Creates the authorization headers needed for subsequent requests to the Spotify API.

    Args:
        token (str): The access token for Spotify Web API.

    Returns:
        dict: Headers containing the authorization field.
    """
    return {"Authorization": "Bearer " + token}


def get_user_id():
    """
    Retrieves the Spotify user ID from an environment variable.

    The user ID is extracted from the profile link saved in the .env file.

    Returns:
        str: The Spotify user ID.
    """
    load_dotenv()
    # Retrieve user ID from environment variable
    user_link = os.getenv("PROFILE_LINK")
    user_id = user_link[-16:]
    print(user_id)
    return user_id


# Main script flow: Get the token, setup headers for authentication, and retrieve the user ID.
token = get_token()
headers = get_auth_headers(token=token)
user_id = get_user_id()

print(headers)

"""
This script analyzes a given Spotify playlist's audio features, calculates descriptive statistics, and uses these insights to generate a new playlist. It leverages audio features like danceability, energy, and tempo to find songs with similar characteristics across different genres or markets. This approach allows for the creation of curated playlists that match the mood or style of the original playlist data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Path to the CSV file containing the playlist's audio features
csv_playlist_data_path = "afrobeats.csv"


def audio_values_range(filepath):
    """
    Calculates the descriptive statistics and interquartile range for each audio feature in a playlist.

    Parameters:
    - filepath: The path to the CSV file containing the playlist's audio features.

    Returns:
    - DataFrame containing the descriptive statistics for each audio feature.
    """
    playlist_data = pd.read_csv(filepath)
    audio_metrics_stats = {}

    for column in playlist_data:
        try:
            descriptive = playlist_data[column].describe()
            descriptive.rename(
                index={"25%": "Q1", "50%": "Median", "75%": "Q3"}, inplace=True
            )
            iq_range = (
                descriptive.loc["Q3"] - descriptive.loc["Q1"]
            )  # Calculate the IQR
            descriptive.loc["IQR"] = iq_range

            column_stats = {
                statistic: value for statistic, value in descriptive.items()
            }
            audio_metrics_stats[column] = column_stats

        except Exception as e:
            print(f"Non-numeric data skipped: {column}")

    audio_metrics_df = pd.DataFrame(audio_metrics_stats)
    return audio_metrics_df


audio_metrics = audio_values_range(csv_playlist_data_path)

# Importing the genre_recommendations function from the generate_recommendations script.
# It's assumed that 'generate_recommendations.py' is correctly renamed and contains the required function.
from generate_recommendations import genre_recommendations, choose_genre_seed

# Example genre and market choice for generating recommendations
genre_choice = "salsa"
market_choice = "US"

# Generating recommendations based on the calculated audio metrics, genre, and market choice
recommendations = genre_recommendations(genre_choice, market_choice, audio_metrics)


def plot_descriptive(descriptive_stats, filepath):
    """
    Plots descriptive statistics for audio features in a playlist.

    Parameters:
    - descriptive_stats: Descriptive statistics for the playlist's audio features.
    - filepath: Path to the CSV file containing the playlist data.
    """
    playlist_data = pd.read_csv(filepath)
    for column in playlist_data:
        if column not in ["name", "id"]:
            plt.figure(figsize=(10, 6))
            sns.boxplot(y=playlist_data[column], color="lightblue", width=0.3)
            plt.scatter(
                x=0, y=descriptive_stats["50%"], color="red", zorder=5, label="Median"
            )
            plt.scatter(
                x=0, y=descriptive_stats["mean"], color="blue", zorder=5, label="Mean"
            )

            plt.text(
                x=0.4,
                y=descriptive_stats["25%"],
                s=f"Q1\n{descriptive_stats['25%']:.2f}",
                color="green",
                verticalalignment="center",
            )
            plt.text(
                x=0.4,
                y=descriptive_stats["75%"],
                s=f"Q3\n{descriptive_stats['75%']:.2f}",
                color="green",
                verticalalignment="center",
            )
            plt.xlim(-0.5, 1)
            plt.title(f"Box Plot and Statistics for {column}")
            plt.ylabel(column)
            plt.legend()
            plt.grid(True, which="both", linestyle="--", linewidth=0.5, axis="y")
            plt.show()


# Example call to plot_descriptive, assuming descriptive statistics for a specific column are provided in a dictionary format
# plot_descriptive(descriptive_stats={'mean': value, '50%': value, '25%': value, '75%': value}, filepath=csv_playlist_data_path)

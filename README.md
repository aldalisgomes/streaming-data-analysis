# Streaming Platforms Data Analysis

This project analyzes a dataset containing ratings for movies and TV shows available on major streaming platforms (Netflix, Prime Video, Hulu, and Disney+). The goal is to clean the data, normalize ratings from different sources (IMDb and Rotten Tomatoes), and identify the top-tier content across all platforms.

## Dataset
The raw data was sourced from Kaggle: [TV shows on Netflix, Prime Video, Hulu and Disney+](https://www.kaggle.com/datasets/ruchi798/tv-shows-on-netflix-prime-video-hulu-and-disney). 
* `streaming_movies.csv`: Contains movie data and ratings.
* `streaming_tv_shows.csv`: Contains TV show data and ratings.

## Methodology
1. **Data Cleaning & Concatenation:** Merged the movie and TV show datasets while filtering for relevant columns.
2. **String Manipulation & Casting:** Extracted numerical values from string-based rating columns (e.g., converting `'7.7/10'` to a float `7.7`).
3. **Descriptive Statistics:** Grouped data by content type to generate statistical summaries.
4. **Percentile Filtering:** Identified the "Best" movies and TV shows by filtering for titles that scored in the 95th percentile on both IMDb and Rotten Tomatoes.

## Repository Structure
* `data/raw/`: Contains the CSV datasets.
* `src/`: Contains the Python script for the analysis.

## How to Run
1. Clone this repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the analysis script from the root directory: `python src/streaming_analysis.py`
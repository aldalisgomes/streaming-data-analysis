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
* `resultados/`: Auto-generated folder for saving visualization plots (ignored by git).

## How to Run

Note for Windows Users: The Makefile commands are designed for Unix environments (Linux/macOS). If you are on Windows, please use Git Bash or WSL to run the pipeline. The script is fully configured to automatically open the generated visualization on your Windows screen even if running from WSL.

1. Clone the repository and access the folder
```bash
git clone https://github.com/aldalisgomes/streaming-data-analysis.git
cd streaming-data-analysis
```

2. Create and activate the virtual environment (Required on newer Debian/Ubuntu-based systems, such as WSL)
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies and run the pipeline
```bash
make install
make run
```
(Note: To clean the environment, cache, and the generated resultados folder, you can run `make clean`)

## Alternative for Windows (Or No Make Installed)
If you are using standard Git Bash, PowerShell, or Command Prompt without make installed, you can simply run the Python script directly after activating your virtual environment:

```bash
pip install -r requirements.txt
python src/streaming_analysis.py
```
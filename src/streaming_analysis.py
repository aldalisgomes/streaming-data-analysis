#%% Movies and TV Shows Datasets

# The datasets contain ratings for movies and TV shows available on streaming platforms
# Source: https://www.kaggle.com/datasets/ruchi798/tv-shows-on-netflix-prime-video-hulu-and-disney

#%% Loading the packages
import pandas as pd
import os
import platform
import subprocess
import plotly.express as px

#%% Loading the datasets

movies_data = pd.read_csv('data/raw/streaming_movies.csv', sep=',')
tv_shows_data = pd.read_csv('data/raw/streaming_tv_shows.csv', sep=',')

movies_data.info()
tv_shows_data.info()

#%% Selecting columns and merging datasets

# Both datasets have similar structures regarding variables
# However, the movies dataset has extra columns
# Let's organize the datasets quickly and merge them

# Selection of variables of interest:
movies_data = movies_data.iloc[:, 0:12]

# Merging data
full_data = pd.concat([movies_data, tv_shows_data], ignore_index=True)

# Removing unnecessary variable
full_data.drop(columns=['Unnamed: 0'], inplace=True)

#%% Extracting ratings
# Extract ratings [Example formats: ('IMDb': 7.7/10) ('Rotten Tomatoes': 99/100)]
full_data['IMDB_Adj'] = full_data['IMDb'].str.slice(0, 4) #'7.7/'
full_data['Rotten_Adj'] = full_data['Rotten Tomatoes'].str.slice(0, 3) #'99/'

# Now we must adjust these strings and transform them into floats
full_data['IMDB_Adj'] = full_data['IMDB_Adj'].str.rstrip('/').astype('float')
full_data['Rotten_Adj'] = full_data['Rotten_Adj'].str.rstrip('/').astype('float')

#%% Generating statistics about the ratings
# Assigning labels 
type_mapping = {0: 'movie', 1: 'tv_show'}
full_data = full_data.assign(type = full_data.Type.map(type_mapping))

# Grouping the dataset
descriptive_stats = full_data.groupby(['type'])

# Generating statistics per variable
print(descriptive_stats['IMDB_Adj'].describe().T)
print(descriptive_stats['Rotten_Adj'].describe().T)

#%% Creating an indicator for the "best" movies and TV shows 
# Separating the database (we separate into TV shows and movies, then we select the best)
best_tv_shows = full_data.query("type == 'tv_show'")
best_movies = full_data.query("type == 'movie'")

# Now we will select the best ones:
#%% TV Shows
# Let's identify those with the best ratings in both evaluations
# We will use the 95th percentile of the ratings as a reference
best_tv_shows[['IMDB_Adj', 'Rotten_Adj']].quantile(0.95)

# Generating the data
best_tv_shows = best_tv_shows.assign(IMDB_Categ = pd.qcut(best_tv_shows.IMDB_Adj, 
                                                          q=[0, 0.95, 1.0],
                                                          labels=['lower', 'higher']))

best_tv_shows = best_tv_shows.assign(Rotten_Categ = pd.qcut(best_tv_shows.Rotten_Adj, 
                                                            q=[0, 0.95, 1.0],
                                                            labels=['lower', 'higher']))

top_tv_shows = best_tv_shows[(best_tv_shows['IMDB_Categ'] == 'higher') & 
                             (best_tv_shows['Rotten_Categ'] == 'higher')].sort_values(['Rotten_Adj', 'IMDB_Adj'], ascending=False)

#%% Movies

# Let's identify those with the best ratings in both evaluations
# We will use the 95th percentile of the ratings as a reference
best_movies[['IMDB_Adj', 'Rotten_Adj']].quantile(0.95)

# Generating the data
best_movies = best_movies.assign(IMDB_Categ = pd.qcut(best_movies.IMDB_Adj,
                                                      q=[0, 0.95, 1.0],
                                                      labels=['lower', 'higher']))

best_movies = best_movies.assign(Rotten_Categ = pd.qcut(best_movies.Rotten_Adj,
                                                        q=[0, 0.95, 1.0],
                                                        labels=['lower', 'higher']))

top_movies = best_movies[(best_movies['IMDB_Categ'] == 'higher') & 
                         (best_movies['Rotten_Categ'] == 'higher')].sort_values(['IMDB_Adj', 'Rotten_Adj'], ascending=False)


#%% Generating and Exporting Plots-------------------------------------------------------

#%% Generating and Exporting Interactive Plot

# 1. Create the 'resultados' folder (if it doesn't exist)
results_folder = os.path.join(os.getcwd(), 'resultados')
os.makedirs(results_folder, exist_ok=True)

# 2. Create the interactive plot with Plotly
# The 'hover_name' property will show the movie title when hovering over the points
fig = px.scatter(
    top_movies,
    x='Rotten_Adj',
    y='IMDB_Adj',
    hover_name='Title',
    title='IMDb vs Rotten Tomatoes (Best Movies)',
    labels={'Rotten_Adj': 'Rotten Tomatoes', 'IMDB_Adj': 'IMDb'},
    opacity=0.7,
    color_discrete_sequence=['purple']
)

# 3. Save the plot as an HTML file
plot_path = os.path.join(results_folder, 'ratings_plot.html')
fig.write_html(plot_path)

# 4. Detect the environment to open the results
environment = platform.release().lower()

if 'microsoft' in environment or 'wsl' in environment:
    # WSL environment detected
    try:
        # Convert Linux paths to native Windows paths
        win_folder = subprocess.check_output(['wslpath', '-w', results_folder]).decode('utf-8').strip()
        win_plot = subprocess.check_output(['wslpath', '-w', plot_path]).decode('utf-8').strip()
        
        # Open the folder in Windows Explorer
        subprocess.run(['explorer.exe', win_folder])
        
        # Open the HTML file in the default Windows browser (Edge, Chrome, etc.)
        subprocess.run(['powershell.exe', '-Command', f"Invoke-Item -LiteralPath '{win_plot}'"])
    except Exception as e:
        print(f"Error interacting with Windows via WSL: {e}")
        
elif platform.system() == 'Windows':
    # Native Windows support
    os.startfile(results_folder)
    os.startfile(plot_path)
    
elif platform.system() == 'Darwin':
    # Native macOS support
    subprocess.run(['open', results_folder])
    subprocess.run(['open', plot_path])
    
else:
    # Generic / Native Linux support
    subprocess.run(['xdg-open', results_folder])
    subprocess.run(['xdg-open', plot_path])
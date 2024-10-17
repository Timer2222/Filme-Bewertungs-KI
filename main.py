import requests
import csv

# TMDb API-Schlüssel
tmdb_api_key = '7518bd0631bc7b8ae0a74da2b982cbb1'

# OMDb API-Schlüssel
omdb_api_key = '375d37b'

# Funktion zum Abrufen der Top-Filme von TMDb
def get_top_movies():
    url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={tmdb_api_key}&language=de-DE&page=1'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['results']
    else:
        return None

# Funktion zum Abrufen der externen IDs (inklusive IMDb-ID) von TMDb
def get_imdb_id(tmdb_id):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}/external_ids?api_key={tmdb_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('imdb_id')
    else:
        return None

# Funktion zum Abrufen von OMDb-Infos
def get_movie_info_by_id(imdb_id):
    url = f'http://www.omdbapi.com/?i={imdb_id}&apikey={omdb_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funktion zum Abrufen des Budgets von TMDb
def get_movie_budget(tmdb_id):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('budget', 'N/A')  # 'N/A', falls nicht verfügbar
    else:
        return None

# CSV-Datei mit Semikolons schreiben
with open('Daten/Daten.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=';')  # Semikolon als Trennzeichen
    
    # Header der CSV-Datei
    writer.writerow(['Title', 'Budget', 'Box Office', 'IMDB Rating'])

    # Top-Filme abrufen
    top_movies = get_top_movies()

    # Für jeden Film die IMDb-ID, Budget und OMDb-Details abrufen
    if top_movies:
        for movie in top_movies[:20]:  # Abrufen der ersten 20 Filme
            tmdb_id = movie.get('id')  # TMDb-ID
            imdb_id = get_imdb_id(tmdb_id)  # Abrufen der IMDb-ID über die externe IDs Anfrage
            
            if imdb_id:
                movie_info = get_movie_info_by_id(imdb_id)
                if movie_info:
                    # Titel, Box Office und Bewertung aus OMDb abrufen
                    title = movie_info.get('Title')
                    imdb_rating = movie_info.get('imdbRating', 'N/A')
                    box_office = movie_info.get('BoxOffice', 'N/A')
                    
                    # Budget von TMDb abrufen
                    budget = get_movie_budget(tmdb_id)
                    if budget != 'N/A':
                        budget = f"${budget:,}"  # Budget formatieren
                    else:
                        budget = 'N/A'
                    
                    # Daten in die CSV-Datei schreiben
                    writer.writerow([title, budget, box_office, imdb_rating])
    else:
        print("Error retrieving top movies")

print("CSV-Datei erfolgreich erstellt: movies_data_semicolon.csv")

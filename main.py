import requests
import csv
import pandas
import sklearn.tree
import matplotlib

# TMDb API-Schlüssel
tmdb_api_key = '7518bd0631bc7b8ae0a74da2b982cbb1'

# OMDb API-Schlüssel
omdb_api_key = '375d37b'

# Funktion zum Abrufen der beliebtesten Filme von TMDb
def get_schlechteste_Filme():
    movies = []
    for page in range(450, 501):  # Ruft die Filme von Seite 490 bis 500 ab (20 Filme pro Seite)
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=us-US&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            movies.extend(response.json()['results'])
        else:
            return None
    return movies

def get_beste_Filme():
    movies = []
    for page in range(1, 50):  # Ruft die Filme von Seite 490 bis 500 ab (20 Filme pro Seite)
        url = f'https://api.themoviedb.org/3/movie/popular?api_key={tmdb_api_key}&language=us-US&page={page}'
        response = requests.get(url)
        if response.status_code == 200:
            movies.extend(response.json()['results'])
        else:
            return None
    return movies

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

# Funktion zum Abrufen des Budgets und des Box Office von TMDb
def get_movie_budget_and_box_office(tmdb_id):
    url = f'https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={tmdb_api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        movie_data = response.json()
        budget = movie_data.get('budget', 'N/A')
        box_office = movie_data.get('revenue', 'N/A')  # 'revenue' ist das Box Office
        return budget, box_office
    else:
        return None, None


def SchlechteFilme():
    # CSV-Datei mit Semikolons schreiben
    with open('Daten/schlecht.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')  # Semikolon als Trennzeichen
    
        # Header der CSV-Datei
        writer.writerow(['Title', 'Budget', 'Box Office', 'guter Film'])

        # Beliebte Filme abrufen
        least_popular_movies = get_schlechteste_Filme()
    
        i = 0
        schlechteFilmeListe = []
        schonDrinn = False
        # Für jeden Film die IMDb-ID, Budget und OMDb-Details abrufen
        if least_popular_movies:
            for movie in least_popular_movies[:len(least_popular_movies)]:  # Abrufen der ersten 100 Filme
                tmdb_id = movie.get('id')  # TMDb-ID
                imdb_id = get_imdb_id(tmdb_id)  # Abrufen der IMDb-ID über die externe IDs Anfrage

                if imdb_id:
                    movie_info = get_movie_info_by_id(imdb_id)
                    if movie_info:
                        # Titel, IMDb-Rating und Box Office abrufen
                        title = movie_info.get('Title')
                        imdb_rating = movie_info.get('imdbRating', 'N/A')

                        # Budget und Box Office von TMDb abrufen
                        budget, box_office = get_movie_budget_and_box_office(tmdb_id)

                        # Nur Filme hinzufügen, bei denen sowohl Budget als auch Box Office bekannt sind
                        if (budget != 0 and box_office != 0):
                            # Budget und Box Office formatieren
                            budget = f"${budget:,}" if budget else 'N/A'
                            box_office = f"${box_office:,}" if box_office else 'N/A'

                            # Daten in die CSV-Datei schreiben
                            # manchmal kommen Filme aus irgendeinem Grund doppelt vor, also wird geschaut, dass dies nicht passiert
                            if i == 0:
                                schlechteFilmeListe.append([title, budget, box_office, "0"])
                                writer.writerow([title, budget, box_office, "0"])
                                i = i+1
                            for ii in range(len(schlechteFilmeListe)):
                                if schlechteFilmeListe[ii][0] == title:
                                    schonDrinn = True
                                    break
                            if(schonDrinn == False):
                                schlechteFilmeListe.append([title, budget, box_office, "0"])
                                writer.writerow([title, budget, box_office, "0"])
                                i = i+1
                            schonDrinn = False

                        if (i == 100):
                            break
        else:
            print("Error retrieving popular movies")

    print("CSV-Datei erfolgreich erstellt: Daten/schlecht.csv")


def GuteFilme():
    # CSV-Datei mit Semikolons schreiben
    with open('Daten/gut.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')  # Semikolon als Trennzeichen

        # Header der CSV-Datei
        writer.writerow(['Title', 'Budget', 'Box Office', 'guter Film'])

        # Beliebte Filme abrufen
        most_popular_movies = get_beste_Filme()

        i = 0
        guteFilmeListe = []
        schonDrinn = False
        # Für jeden Film die IMDb-ID, Budget und OMDb-Details abrufen
        if most_popular_movies:
            for movie in most_popular_movies[:len(most_popular_movies)]:  # Abrufen der ersten 100 Filme
                tmdb_id = movie.get('id')  # TMDb-ID
                imdb_id = get_imdb_id(tmdb_id)  # Abrufen der IMDb-ID über die externe IDs Anfrage

                if imdb_id:
                    movie_info = get_movie_info_by_id(imdb_id)
                    if movie_info:
                        # Titel, IMDb-Rating und Box Office abrufen
                        title = movie_info.get('Title')
                        imdb_rating = movie_info.get('imdbRating', 'N/A')

                        # Budget und Box Office von TMDb abrufen
                        budget, box_office = get_movie_budget_and_box_office(tmdb_id)

                        # Nur Filme hinzufügen, bei denen sowohl Budget als auch Box Office bekannt sind
                        if (budget != 0 and box_office != 0):
                            # Budget und Box Office formatieren
                            budget = f"${budget:,}" if budget else 'N/A'
                            box_office = f"${box_office:,}" if box_office else 'N/A'

                            # Daten in die CSV-Datei schreiben
                            # manchmal kommen Filme aus irgendeinem Grund doppelt vor, also wird geschaut, dass dies nicht passiert
                            if i == 0:
                                guteFilmeListe.append([title, budget, box_office, "1"])
                                writer.writerow([title, budget, box_office, "1"])
                                i = i+1
                            for ii in range(len(guteFilmeListe)):
                                if guteFilmeListe[ii][0] == title:
                                    schonDrinn = True
                                    break
                            if(schonDrinn == False):
                                guteFilmeListe.append([title, budget, box_office, "1"])
                                writer.writerow([title, budget, box_office, "1"])
                                i = i+1
                            schonDrinn = False

                        if (i == 100):
                            break
        else:
            print("Error retrieving popular movies")

    print("CSV-Datei erfolgreich erstellt: Daten/gut.csv")


def vorbereiten():
    guteFilmeDaten = pandas.read_csv('c:/Users/acer/Documents/Schule/12.1/Info/Python/Filme-Bewertungs-KI/Daten/gut.csv', sep=';')
    schlechteFilmeDaten = pandas.read_csv('c:/Users/acer/Documents/Schule/12.1/Info/Python/Filme-Bewertungs-KI/Daten/schlecht.csv', sep=';')
    datengesamt = pandas.concat([guteFilmeDaten, schlechteFilmeDaten], ignore_index=True)
    attribute  = ["Budget","Box Office"]
    zielkriterium = "guter Film"
    datengesamt['Budget'] = datengesamt['Budget'].replace('[\$,]', '', regex=True).astype(float)
    datengesamt['Box Office'] = datengesamt['Box Office'].replace('[\$,]', '', regex=True).astype(float)

    lernen(datengesamt, attribute, zielkriterium)

def lernen(daten, attribute, ziel):
    model = sklearn.linear_model.LinearRegression()
    model.fit(daten[attribute], daten['guter Film'])
    model.score(daten[attribute], daten['guter Film'])
    for datensatz in daten.index:
        print(daten.loc[datensatz]['Title'],model.predict(daten.loc[[datensatz]][attribute]))


vorbereiten()
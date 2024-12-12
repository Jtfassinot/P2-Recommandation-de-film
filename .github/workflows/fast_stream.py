import streamlit as st
import requests
import pandas as pd

# URL de l'API FastAPI
API_URL = "http://127.0.0.1:8000/find_similar_film/"

# Charger les données de films
df_recherche_film = pd.read_csv('/Users/julien-thomasfassinot/Documents/WCS/PROJET 2/Data final/Fonctionnel/df_recherche_film.csv')  # Remplacez par le chemin correct

# Titre de l'application Streamlit
st.title('Recherche de films similaires')

# Entrée de l'utilisateur pour le nom du film (minimum 3 lettres)
film_name = st.text_input('Entrez le nom du film (minimum 3 lettres)', '')

# Vérifier si l'entrée fait au moins 3 lettres
if len(film_name) >= 3:
    # Filtrer les films qui contiennent les lettres entrées
    matching_movies = df_recherche_film[df_recherche_film["title"].str.contains(film_name, case=False, na=False)]

    if not matching_movies.empty:
        # Liste déroulante avec les films correspondants
        selected_movie_title = st.selectbox('Sélectionnez un film', matching_movies['title'])

        if selected_movie_title:
            # Si un film est sélectionné, récupérer les informations du film
            selected_movie = matching_movies[matching_movies['title'] == selected_movie_title].iloc[0]

            # Afficher le film sélectionné (optionnel)
            st.subheader(f"Film sélectionné: {selected_movie['title']} ({selected_movie['startYear']})")

            # Appeler l'API pour obtenir les films similaires
            response = requests.post(API_URL, json={"film_name": selected_movie_title, "k": 5})

            if response.status_code == 200:
                data = response.json()
                films = data["films"]

                if films:
                    # Convertir les films en DataFrame pour les afficher sous forme de tableau
                    films_df = pd.DataFrame(films)

                    # Affichage du tableau avec les films recommandés
                    st.subheader("Films recommandés similaires")
                    st.dataframe(films_df[['title', 'startYear', 'similarity_score', 'overview_fr', 'poster_path']])

                    # Affichage des images des films recommandés
                    for film in films:
                        # Si le chemin de l'image existe, afficher l'image
                        if film['poster_path']:
                            st.image(film['poster_path'], width=150)

                else:
                    st.write("Aucun film similaire trouvé.")
            else:
                st.write("Erreur lors de la récupération des films.")
    else:
        st.write("Aucun film ne correspond à votre recherche.")
else:
    st.write("Veuillez entrer au moins 3 lettres pour rechercher un film.")





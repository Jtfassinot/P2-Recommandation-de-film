import streamlit as st
import requests
import pandas as pd
import urllib.parse  # Pour encoder correctement les titres dans les URL

# URL de l'API FastAPI (assurez-vous que le backend FastAPI fonctionne sur ce port)
API_URL = "http://127.0.0.1:8000/rechercher"

# Charger les données de films
@st.cache_data
def load_movie_data():
    try:
        df = pd.read_csv(r"C:\Users\laeti\Desktop\Wild_code_school\Projet2\tout refait au propre\df_avec_overview.csv")
        return df
    except FileNotFoundError:
        st.error("Le fichier des films est introuvable. Vérifiez le chemin du fichier.")
        return pd.DataFrame()

df_recherche_film = load_movie_data()

# Fonction pour générer un lien de recherche YouTube
def get_youtube_search_link(movie_title):
    query = f"{movie_title} trailer"
    query_encoded = urllib.parse.quote(query)
    return f"https://www.youtube.com/results?search_query={query_encoded}"

# Ajouter une image de fond en bannière et des petites images liées au cinéma
st.markdown("""
    <style>
        .stApp {
            background-image: url("C:/Users/laeti/Desktop/Wild_code_school/Projet2/image_streamlit_background.jpg");
            background-size: cover;
            background-position: center;
        }
        .movie-title {
            font-size: 28px;
            color: #FF6347;
            font-weight: bold;
            margin-bottom: 5px; /* Ajout d'une petite marge après le titre */
        }
        .realisateurs {
             font-size: 16px;
            color: #008080; /* Couleur turquoise pour les réalisateurs */
            margin-bottom: 5px; /* Marge plus petite après les réalisateurs */
        }
        .synopsis {
            font-size: 14px;
            color: #555; /* Couleur gris pour les synopsis */
        }
        .recommended-movie {
            margin-bottom: 50px; /* Ajouter un espace plus grand entre chaque film recommandé */
        }
        .center-image {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%; /* Centrer verticalement l'image */
        }
        /* Centrer le titre de l'application */
        .center-title {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# Afficher l'image de la bannière
st.image(r"C:\Users\laeti\Desktop\Wild_code_school\Projet2\image streamlit.jpg", use_container_width=True)

# Titre de l'application Streamlit centré
st.markdown("<h1 class='center-title'>Cin'Ehpad 🎬</h1>", unsafe_allow_html=True)

# Entrée utilisateur pour rechercher un film ou un mot du titre
film_name = st.text_input("🔍 Entrez le nom du film ou un mot du titre et appuyez sur la touche entrée", '')

# Logique de recherche locale des films avec un mot-clé dans le titre
if len(film_name.strip()) >= 1:
    matching_movies = df_recherche_film[
        df_recherche_film["title"].str.contains(film_name, case=False, na=False)
    ].head(10)

    if not matching_movies.empty:
        # Ajouter une colonne pour afficher "Titre (Année)"
        matching_movies['title_with_year'] = matching_movies['title'] + " (" + matching_movies['startYear'].astype(str) + ")"
        
        # Sélection du film via liste déroulante
        selected_movie_title_with_year = st.selectbox("🎥 Sélectionnez un film :", matching_movies['title_with_year'])

        if selected_movie_title_with_year:
            # Extraire les détails du film sélectionné
            selected_movie = matching_movies[matching_movies['title_with_year'] == selected_movie_title_with_year].iloc[0]

            col1, col2 = st.columns([2, 3])

            with col1:
                st.subheader(f"🎞️ Film sélectionné : {selected_movie['title']} ({selected_movie['startYear']})")

            with col2:
                if pd.notna(selected_movie.get('poster_path')):
                    poster_url = f"https://image.tmdb.org/t/p/w500{selected_movie['poster_path']}"
                    st.image(poster_url, width=150)
                else:
                    st.write("🖼️ Aucune affiche disponible pour ce film.")

            # Appel de l'API pour obtenir des recommandations
            with st.spinner("🔄 Chargement des recommandations..."):
                response = requests.post(API_URL, json={"film_name": selected_movie['title']})

            # Vérification de la réponse API
            if response.status_code == 200:
                data = response.json()
                recommended_films = data.get("recommended_films", [])

                if recommended_films:
                    st.subheader("✨ Films recommandés similaires")
                    for film in recommended_films:
                        # Utilisation de la disposition en colonnes pour afficher les affiches et synopsis côte à côte
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            # Utilisation de la classe CSS pour centrer l'affiche du film
                            with st.container():
                                st.markdown('<div class="center-image">', unsafe_allow_html=True)
                                # Afficher l'affiche du film si elle existe
                                if film.get('poster_path'):
                                    poster_url = f"https://image.tmdb.org/t/p/w500{film['poster_path']}"
                                    st.image(poster_url, width=150)
                                else:
                                    st.write("🖼️ Aucune image disponible.")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            # Appliquer la classe CSS pour le titre du film et l'agrandir
                            st.markdown(f"<p class='movie-title'>🎬 {film['title']} ({film['startYear']})</p>", unsafe_allow_html=True)
                            
                            # Afficher les réalisateurs juste en dessous du titre
                            if film.get('realisateurs'):
                                st.markdown(f"<p class='realisateurs'>👤 Réalisateurs : {film['realisateurs']}</p>", unsafe_allow_html=True)
                            
                            # Afficher le synopsis
                            if film.get('overview_fr'):
                                st.markdown(f"📖 **Synopsis :** {film['overview_fr']}", unsafe_allow_html=True)

                            # Ajouter un lien YouTube pour le trailer
                            youtube_link = get_youtube_search_link(film['title'])
                            st.markdown(f"[🎥 Rechercher la bande d'annonce sur YouTube]({youtube_link})", unsafe_allow_html=True)
                        
                        # Ajouter un peu d'espace entre les films recommandés
                        st.markdown("<br>", unsafe_allow_html=True)
                else:
                    st.warning("Aucune recommandation disponible pour ce film.")
            else:
                st.error("❌ Erreur lors de la récupération des films similaires. Vérifiez le serveur API.")
    else:
        st.warning("🔎 Aucun film trouvé. Essayez un autre nom.")
else:
    st.info("Veuillez entrer au moins une lettre pour rechercher un film.")

    
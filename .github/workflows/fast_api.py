from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.neural_network import MLPRegressor
from typing import List, Dict

# Charger les DataFrames
df_recherche_film = pd.read_csv('/Users/julien-thomasfassinot/Documents/WCS/PROJET 2/Data final/Fonctionnel/df_recherche_film.csv')  # Remplacez le chemin
df_entrainement = pd.read_csv('/Users/julien-thomasfassinot/Documents/WCS/PROJET 2/Data final/Fonctionnel/df_entrainement.csv')  # Remplacez le chemin

# Créer l'instance de l'API
app = FastAPI()

# Classe Pydantic pour valider les entrées de l'API
class FilmRequest(BaseModel):
    film_name: str
    k: int = 5

# Fonction pour trouver les films similaires
def find_similar_film_genre(film_name: str, k: int = 5) -> List[Dict]:
    def search_and_select_movie(df, query):
        matches = df_recherche_film[df_recherche_film["title"].str.contains(query, case=False, na=False)]
        if matches.empty:
            return None
        selected_movie = matches.iloc[0]
        return selected_movie

    # Recherche du film
    selected_movie = search_and_select_movie(df_entrainement, film_name)
    if selected_movie is None:
        return [{"error": "Aucun film trouvé"}]

    # Exclure le film recherché des candidats
    df_candidates = df_entrainement[df_entrainement['title'] != selected_movie['title']]

    # Caractéristiques pour la similarité
    features = [
        'popularity', 'vote_count',
        'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary',
        'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery',
        'Romance', 'Science Fiction', 'TV Movie', 'Thriller', 'War', 'Western'
    ]

    # Standardisation des données
    scaler = StandardScaler()
    X = scaler.fit_transform(df_candidates[features])

    # k-NN : Identification des voisins proches
    knn = NearestNeighbors(n_neighbors=2 * k, metric='euclidean')
    knn.fit(X)

    # Caractéristiques du film recherché
    film_features = scaler.transform(selected_movie[features].values.reshape(1, -1))

    # Trouver les voisins proches
    distances, indices = knn.kneighbors(film_features)
    candidate_indices = indices[0]
    candidates = df_candidates.iloc[candidate_indices]

    # Préparation des données pour le réseau neuronal
    X_candidates = scaler.transform(candidates[features])
    y_similarities = 1 / (1 + distances[0])

    # Entraînement d'un modèle NN pour ajuster les scores de similarité
    nn = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    nn.fit(X_candidates, y_similarities)

    # Prédiction des scores pour les voisins
    predicted_scores = nn.predict(X_candidates)

    # Ajouter les scores de similarité et trier les résultats
    candidates['similarity_score'] = predicted_scores
    recommended_films = candidates.sort_values(by='similarity_score', ascending=False).head(k)

    # Retourner les films recommandés sous forme de dictionnaire
    return recommended_films[['title', 'startYear', 'similarity_score', 'poster_path', 'overview_fr']].to_dict(orient="records")

# Définir l'endpoint de l'API
@app.post("/find_similar_film/")
async def find_similar_film(request: FilmRequest):
    results = find_similar_film_genre(request.film_name, request.k)
    return {"films": results}




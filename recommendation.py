from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.neural_network import MLPRegressor
import pandas as pd
import numpy as np

# Charger les DataFrames pour la recherche des films et l'entraînement du modèle
df_recherche_film = pd.read_csv(r"C:\Users\laeti\Desktop\Wild_code_school\Projet2\tout refait au propre\df_avec_overview.csv")
df_entrainement = pd.read_csv(r'C:\Users\laeti\Desktop\Wild_code_school\Projet2\presque final\df_entrainement_trailer.csv')

def search_movie(df, film_name):
    """
    Recherche un film dans le DataFrame en fonction du nom.
    
    Parameters:
    df (DataFrame): Le DataFrame contenant les films.
    film_name (str): Le nom du film à rechercher.
    
    Returns:
    dict: Le film trouvé, ou None si pas trouvé.
    """
    result = df[df['title'].str.contains(film_name, case=False, na=False)]
    return result.iloc[0] if not result.empty else None

def recommend_similar_movies(film_name, df_recherche_film, df_entrainement, k=5):
    """
    Recommande des films similaires basés sur les caractéristiques, avec un entraînement effectué sur df_entrainement.
    
    Parameters:
    film_name (str): Le nom du film à rechercher.
    df_recherche_film (DataFrame): DataFrame des films à rechercher.
    df_entrainement (DataFrame): DataFrame des caractéristiques pour l'entraînement du modèle.
    k (int): Nombre de films similaires à recommander.
    
    Returns:
    DataFrame: DataFrame contenant les films recommandés.
    """
    # Rechercher le film à recommander
    selected_movie = search_movie(df_recherche_film, film_name)
    if selected_movie is None:
        return "Aucun film trouvé."
    
    # Exclure le film sélectionné des candidats
    df_candidates = df_entrainement[df_entrainement['title'] != selected_movie['title']]
    
    features = ['popularity', 'vote_count', 'Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 
                'Drama', 'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 
                'TV Movie', 'Thriller', 'War', 'Western']
    
    # Normalisation des données
    scaler = StandardScaler()
    X = scaler.fit_transform(df_candidates[features])
    
    popularity = 1
    vote_count = 1
    genre = 30
    weights = np.array([popularity,
                        vote_count,
                        genre, genre, genre, genre, genre,
                        genre, genre, genre, genre, genre,
                        genre, genre, genre, genre, genre,
                        genre, genre, genre, genre])
    knn = NearestNeighbors(n_neighbors=2 * k, metric='minkowski', metric_params={'w': weights})
    
    # Identification des voisins proches
    # knn = NearestNeighbors(n_neighbors=2 * k, metric='minkowski', metrics_params = {"w": weights})
    # knn = NearestNeighbors(n_neighbors=2 * k, metric='euclidean')
    knn.fit(X)
    
    # Caractéristiques du film recherché
    film_features = scaler.transform(selected_movie[features].values.reshape(1, -1))
    distances, indices = knn.kneighbors(film_features)
    
    # Obtenir les films candidats les plus proches
    candidate_indices = indices[0]
    candidates = df_candidates.iloc[candidate_indices]
    
    # Préparer les données pour le réseau neuronal
    X_candidates = scaler.transform(candidates[features])
    y_similarities = 1 / (1 + distances[0])  # Calcul de la similarité
        
    # Entraînement du réseau neuronal
    nn = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
    nn.fit(X_candidates, y_similarities)
    
    # Prédiction des scores de similarité
    predicted_scores = nn.predict(X_candidates)
    
    # Ajouter les scores et trier les résultats
    candidates['similarity_score'] = predicted_scores
    recommended_films = candidates.sort_values(by='similarity_score', ascending=False).head(k)
    
    return recommended_films[['title', 'startYear', 'poster_path', 'overview_fr', 'realisateurs']]


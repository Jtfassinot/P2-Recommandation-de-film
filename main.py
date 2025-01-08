from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from recommendation import recommend_similar_movies

app = FastAPI()

# Charger les données
try:
    df_recherche_film = pd.read_csv(
        r"C:\Users\laeti\Desktop\Wild_code_school\Projet2\tout refait au propre\df_avec_overview.csv"
    )
    df_entrainement = pd.read_csv(
        r"C:\Users\laeti\Desktop\Wild_code_school\Projet2\presque final\df_entrainement_trailer.csv"
    )
except FileNotFoundError as e:
    print(f"Erreur de chargement des fichiers : {str(e)}")
    raise

# Modèle pour la requête
class MovieRequest(BaseModel):
    film_name: str


@app.get("/")
def read_root():
    """Message d'accueil."""
    return {"message": "Bienvenue sur l'API de recommandation de films"}


@app.post("/rechercher")
def search_movie(request: MovieRequest):
    """
    Recherche un film dans le DataFrame par son titre et recommande des films similaires.
    """
    film_name = request.film_name.strip()  # Nettoyage de l'input utilisateur
    
    if not film_name:
        raise HTTPException(status_code=400, detail="Le nom du film est requis.")

    try:
        # Log pour vérifier l'input utilisateur
        print(f"Recherche en cours pour : {film_name}")

        # Recherche des films correspondants avec un titre similaire
        matched_films = df_recherche_film[
            df_recherche_film['title'].str.strip().str.lower() == film_name.lower()
        ]
        
        if matched_films.empty:
            raise HTTPException(status_code=404, detail=f"Aucun film trouvé pour le titre '{film_name}'.")

        # Log pour vérifier les films trouvés
        print(f"Films trouvés : {matched_films['title'].tolist()}")

        # Appeler la fonction de recommandation
        recommended_films = recommend_similar_movies(film_name, df_recherche_film, df_entrainement)
        
        if not isinstance(recommended_films, pd.DataFrame) or recommended_films.empty:
            raise HTTPException(status_code=404, detail="Aucun film similaire trouvé.")
        
        # Convertir les recommandations en JSON
        recommended_films_json = recommended_films.to_dict(orient='records')
        return {"recommended_films": recommended_films_json}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erreur lors de la recherche : {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur interne du serveur : {str(e)}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



def search_movie(df_recherche_film, film_name):
    """
    Recherche un film dans le DataFrame des films par titre, en limitant les résultats à 10 films.

    Parameters:
    df_recherche_film (DataFrame): DataFrame contenant les informations des films.
    film_name (str): Le nom du film à rechercher.

    Returns:
    list[dict] | None: Liste des films correspondants sous forme de dictionnaires ou None si aucun film n'est trouvé.
    """
    # Rechercher les titres de films contenant le texte saisi (insensible à la casse)
    matches = df_recherche_film[df_recherche_film["title"].str.contains(film_name, case=False, na=False)]

    if matches.empty:
        return None  # Aucun résultat trouvé
    
    # Limiter les résultats à 10 films maximum
    matches = matches.head(10)
    
    # Conversion des résultats en liste de dictionnaires
    results = matches[['tconst', 'title', 'startYear']].to_dict(orient="records")
    
    return results




Film Recommendation by CIN'EHPAd

Description:

Ce projet est un site de recommandation de films, élaboré suite à une étude de marché du cinéma dans la Creuse. L'objectif est de fournir des recommandations personnalisées basées sur les données collectées et les KPIs identifiés lors de notre analyse.
L'outil est conçu pour recommander exclusivement des films du 20ème siècle, même si l'utilisateur entre un film récent comme point de départ pour la recherche.
Le projet inclut des éléments de machine learning pour créer un modèle prédictif, une API pour gérer les interactions backend, ainsi qu'une interface utilisateur développée avec Streamlit.



Structure du projet

Voici la liste des principaux fichiers et dossiers du projet :

- streamlit_app.py : L'interface utilisateur développée avec Streamlit pour permettre à l'utilisateur de rechercher et obtenir des recommandations de films.

- main.py : L'API backend pour gérer les requêtes et les réponses entre l'interface utilisateur et les outils de recommandation.

- recommandation.py : Contient le moteur de recommandation, y compris les algorithmes de filtrage collaboratif ou basé sur le contenu.

- search.py : Gère les fonctionnalités de recherche de films dans la base de données.

- df_entrainement.csv : Base de données d'entraînement utilisée pour former le modèle de machine learning.

- power_bi_kpi.pbix : Fichier Power BI contenant les KPIs utilisés pour orienter le développement de l'outil de recommandation.
- 


Fonctionnalités:

-Recommandation de films personnalisée, limitée aux films du 20ème siècle.
-Recherche avancée de films.
-Visualisation des KPIs clés dans Power BI pour comprendre les préférences et les tendances du marché.

Installation

Clonez le dépôt sur votre machine locale :      git clone https://github.com/votre-utilisateur/film-recommendation.git

Accédez au répertoire du projet :    cd film-recommendation

Installez les dépendances requises :    pip install -r requirements.txt

Lancez l'application Streamlit :    streamlit run streamlit_app.py



Utilisation

Accédez à l'interface utilisateur via l'URL locale affichée dans votre terminal.

Saisissez un film ou une préférence pour obtenir des recommandations.

Notez que les recommandations seront limitées aux films du 20ème siècle.

Consultez le fichier Power BI pour visualiser les KPIs qui guident les recommandations.



Contributeurs

Corentin COCHARD
Laetitia TRIOLA
Julien FASSINOT




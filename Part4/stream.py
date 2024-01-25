import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import plotly.express as px

df = pd.read_csv("C:/Users/aurel/OneDrive - De Vinci/ONE DRIVE PC/A5/Webscrapping/Part4/llmcomm.csv")
df_tripadvisor = pd.read_csv('C:/Users/aurel/OneDrive - De Vinci/ONE DRIVE PC/A5/Webscrapping/tripadvisor_with_id.csv')
# Sélectionner les commentaires positifs
positive_reviews = df[df['TrueSentiment'] == 'positif'][['id', 'comment']].reset_index(drop=True)

# Création du vectoriseur TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
review_vectors = vectorizer.fit_transform(positive_reviews['comment'])

def recommend_restaurants(user_query, top_n=3):
    # Vectorisation de la requête utilisateur
    query_vector = vectorizer.transform([user_query])

    # Calcul de la similarité cosinus
    similarities = cosine_similarity(query_vector, review_vectors)

    # Trouver les indices des avis les plus similaires
    recommended_indices = np.argsort(similarities[0])[-top_n:][::-1]

    # Récupérer les recommandations
    recommendations = positive_reviews.iloc[recommended_indices][['id', 'comment']]

    return recommendations


# Streamlit app
st.title("WebScrapping Project : Restaurant Recommender 😋​🥙​🍲​🥗​")
st.subheader("By Maud Tissot, Arthur Scelles, Aurélien Pouxviel")

# Menu cliquable pour le sommaire
menu = st.sidebar.radio("Menu", ["Home", "Recommendations"])
if menu == "Home":
    st.write("Welcome to Restaurant Recommender! Enter your restaurant preferences in the search box on the left.")
else:
    st.write("Enter your preferences : ")
    user_query = st.text_input('Enter your restaurant preferences:')
    if st.button('Find Recommendations'):
        recommended_reviews = recommend_restaurants(user_query, top_n=3)
        
        st.header('Top 3 Recommendations 🏆')
        for index, row in recommended_reviews.iterrows():
            st.write(f"ID: {row['id']}")
            nom = df_tripadvisor.loc[df_tripadvisor['id'] == int(row['id']), 'name']
            feature = df_tripadvisor.loc[df_tripadvisor['id'] == int(row['id']), 'FEATURES_detail']
            st.write(f"Name : {nom.values[0]}")
            st.write(f"Informations : {feature.values[0]}")
            st.write(f"LLM sumarize comment of the restaurant 👀 \n: {row['comment']}")
            st.write('---')


            # Extraire les IDs pour le fichier TripAdvisor
        top3_ids = recommended_reviews['id'].tolist()

        # Filtrer le dataframe TripAdvisor pour les restaurants recommandés
        top3_details = df_tripadvisor[df_tripadvisor['id'].isin(top3_ids)]
        top3_details["global_rating"] = top3_details["global_rating"].fillna(4)

        # Afficher les informations des restaurants recommandés
        st.header('Details of Recommended Restaurants:')
        fig = px.bar(top3_details, x='name', y='global_rating', color='global_rating', title='Global Ratings of Recommended Restaurants')
        st.plotly_chart(fig)

# Afficher la carte des restaurants recommandés
        st.header('Map of Recommended Restaurants 🗺️')
        fig_map = px.scatter_mapbox(top3_details, lat='latitude', lon='longitude', color='global_rating',
                                size='global_rating', text='name',
                                mapbox_style='carto-darkmatter', zoom=10,
                                color_continuous_scale=px.colors.sequential.YlOrRd)
        fig_map.update_layout(
            mapbox=dict(
                center=dict(lat=top3_details['latitude'].mean(), lon=top3_details['longitude'].mean()),
            ),
            coloraxis=dict(colorbar=dict(title='Global Rating')),
        )
        st.plotly_chart(fig_map)

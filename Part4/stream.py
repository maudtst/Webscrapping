import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

trydta = ['<pad> the chef is an artist and his paintings were displayed, tastefully throughout. the ambiance was a perfect blend of timeless charm and modern luxury. the restaurant is aiming for a Michelin star - with amuse bouches followed by highly skilled cooking.</s>',
 '<pad> the restaurant is run by a husband and wife team and they are very friendly. the stairs to the restroom are narrow and very steep...something to keep in mind for this with limited youth. the food was excellent, beautifully presented and my fish was perfectly cooked.</s>',
 '<pad> the food was excellent with a tasty amuse Bouche to start the meal. the Langoustines and Crab appetisers were zingy and full of flavour. the Pork main was delightful and the Hake was melt in mouth delicious.</s>',
 '<pad> le Thika is a friendly cafe in the middle of Vannes. the food was really nice - freshly made in front of us. the bathroom is spotlessly clean.</s>',
 "<pad> la tête en l'air is a 'blind tasting menu' with a seven course wine pairing. the concept was really novel and unlike anything we have eaten before. the staff were friendly and patient even with our stilted french. the restaurant is closed on Tuesday and Wednesday.</s>",
 '<pad> the food was very good value for money, and the service was professional. the interior is modern and clean. the service is efficient and clean. the presentation of the dishes is sterile and clean.</s>',
 "<pad> the waitress Ivy was a delight! She was smiley, attentive and friendly with excellent English skills. the pizzas were delicious. my sons like deep crust whereas me and my husband prefer thin. it didn't matter.</s>",
 '<pad> the food is outstanding, inventively put together, carefully constructed and beautifully cooked and presented. the service is excellent and the cutlery is specially made and monogrammed for la gourmandiere. the wine is expensive but disappointing for the price.</s>',
 '<pad> the complete with mushrooms was amazing and the Complete with andouille sausage was also good. Nice ambience and excellent service.</s>',
 '<pad> the food was mouth watering and extremely well presented. the aubergine starter was very light and very tasty. the dessert was a little disappointing.</s>',
 '<pad> the creperie in Quiberon is a favourite of ours. we had the Genereuse and Pistache Fruits crepes. they were fantastic and we would return for dinner.</s>',
 '<pad>lovely restaurant near to Hotel de Ville in vannes. good quality food and wine',
 '<pad> le Roscanvec is the only place to stay in old-town vannes. it completely exceeded our expectations. the food is beautiful, local, imaginative, and tasty.</s>',
 '<pad> small restaurant operating in cramped quarters in the heart of the old city of vannes. Empreinte was an absolute joy to eat here. each dish is wonderfully thought through but not over worked.</s>',
 '<pad> buckwheat crepes are a great way to start a day in vannes. despite the pandemic, we had not visited our favourite creperie for over three years.</s>',
 '<pad> i was turned away 1.5 hours before closing time with a claim that they were ‘fully booked’ although only one table was seated. i had the rabbit Rilettes with a beetroot coulis and <unk> Fleischschnacka of veal with a beautiful citrus zingy sauce which complimented it magnificently.</s>',
 '<pad> the andouille de Guémène is made using pork cauldrons (large intestines), about 30 wrapped over each other after brining that are stuffed into a natural casing. the andouille sausage is smoked over a wood fire (beech or oak) and then left to dry for several weeks. it is then pricked so that the fat can drain away and cooked in a simmering broth for three or four hours.</s>',
 '<pad> le Rive Gauche is a small, quiet, and classy restaurant. the food is superbly cooked, beautifully presented,...stimulates the tastebuds, and branches outside of French tradition. the menu at lunchtime is only 30 euros for food that is superbly cooked.</s>',
 "<pad> 'assez bien' is a popular restaurant in the old town of vannes. it serves lobster, frites and oysters at a reasonable price. but the service is a bit pushy at times. 'excellent' food and service.</s>",
 '<pad> service was excellent with a good pace and attention to detail. highlights were steaks, samosas and trio of desserts.</s>',
 '<pad> the food was beautifully presented, plentiful and delicious. a dietary requirement was seamlessly catered for with an alternative dish. service was attentive, friendly and welcoming.</s>',
 '<pad> a GemFriendly, welcoming small restaurant / bistro just outside the walls. service was good, in fact attentive. we were asked if we wanted to speak english. food was excellent and spices were well balanced.</s>',
 '<pad>a lovely restaurant with a woman',
 '<pad> the service was fantastic and the lady serving us was lovely and very friendly. we had the mushroom ravioli which was stunning the flavours were fantastic and i could of eaten it again as a main meal.</s>',
 '<pad> the Sushiya in Vannes is a young hipster staffed restaurant. the food is delicious and the service is friendly and english speaking. the owners love Japanese culture and food more than some "real" Japanese people.</s>',
 '<pad> the best crepes in the cityI enjoyed the chicken galette & my mum had one with scallops. the service was ok, waitresses were not really smiling and not really showing you count as a customer.</s>',
 '<pad> the setting is traditional but not twee, with the kitchen wide open to...view. service was friendly and, once ordered, very quick. atypical due to its interior decor and our very traditional cuisine.</s>',
 "<pad> despite many recommendations from shop owners, we decided to take on la p'tite souris...situated by the port, slightly out of the busy areas. the food is something they should be proud of, the kitchen has got it spot on in terms of portions, quality, presentation, flavours, diversity of choice. value for money is simply unbeatable.</s>",
 '<pad>must try!!A',
 "<pad> a small outside place in summer but no circulation very disturbing I have Liked the large choice of galettes / tradiotonal eat in région / somme suggar Salt to taste very average, wouldn't go back.</s>",
 '<pad> the fish was succulent & presented scampi style in a mini chip basket accompanied by a pot of nicely cooked chips & tartare sauce. service was quick and efficient. the chips were great...- a little soggy from being in a plastic dish, but probably delicious served fresh.</s>',
 '<pad>the restaurant is a little away from the center, real creative cuisine, with fresh market products. pleurotes persillade with egg',
 "<pad> a lovely little restaurant in the old town of vannes with very good food and wine. the menu isn't that diverse apart from bread, butter, jelly, eggs and bacon. the service was excellent and the food was good value for money. a mojito was the best cocktail i have tried before.</s>",
 "<pad> the restaurant is located on the quayside near the swinging bridge. the menu changes daily and is prepared with fresh produce. the food and service couldn't be faulted.</s>",
 '<pad> brie pane, salmon tartare and salmon rissoto were great value for money. the staff were equally as lovely and spoke some English. enfant was just as good - great value at €12.20 for 2 courses.</s>',
 "<pad>mone laos-thai restaurant in vannes has 12 reviews in about a month. it's now ranked 11th best in the french capital. the restaurant has a big, refrigerated counter with all the food on",
 "<pad> hidden away in the corrner of the Place des Lices it isn't obvious as you walk down towards the port. excellent crepes and generous with the fillings -...i had a lot of roquefort on mine.</s>",
 '<pad> the pizza was amazing! Great toppings super fresh and friendly service. a game of two halves (world cup time)We had pizza, pasta and panini - all delicious.</s>',
 "<pad> 'fait maison' is a small cafe/restaurant tucked away in the shopping area of vanes. it serves a variety of quiches and beautiful desserts, plus an entrée du jour and a plat du jour. the menu is inexpensive, good helpings, fresh and very tasty.</s>",
 '<pad> a small bistro next to the local fish market, this is a quieter place a step away from the busy port. the food is extremely fresh and tasty. You may need to reserve or wait for a table outside if you are more than two...or three.</s>',
 '<pad> food was delicious and staff were friendly and helpful. food was spot on and service was great. food was spot on and service was spot on.</s>',
 '<pad>this restaurant is definitely worth a',
 '<pad> a rabbit terrine- superb, veal fillet and a fabulous mash all was grand and my husband ended it with a coffee and warm chocolate pudding with raspberry sauce!! The service was not obtrusive, the food exceptional and actually simple and the lunch was really good. the food was excellent whilst my wife had "ordinary food" - that is with gluten and she was more than satisfied with her food.</s>',
 '<pad> creperie du Vieux Vannes is a charming little creperie. the service was friendly and efficient, but calm at the same time. the food was excellent as well. Authentic buckwheat galettes with some traditional and some more creative fillings.</s>',
 "<pad> Le District is a family run restaurant in the old town of vannes. the food was excellent and the owners made us feel welcome. the owners' young son made an appearance.</s>",
 '<pad> a great place for a light lunch on the heart of vannes. the food is incredible, the galettes and the crepes. the service was very good and friendly.</s>',
 '<pad>food quality very good but kids left a bit',
 '<pad> the service was friendly and as my son said “it does not deserve to be no. 84 in Vannes”... it’s much better.</s>',
 '<pad> the title says it all. the food was well prepared and the size of the dishes were simply enormous. the service was good but without being overhelpfull or friendly.</s>',
 "<pad> a charming indoor/ outdoor cafe restaurant in the centre of beautiful vannes. it's not expensive, just great wine, food, people watching and just chilling out.</s>",
 "<pad> 'café gourmand' is worth a mention and the 'pichet'...of house red wine is excellent so don't go to the expense of a bottle. the pizzas are thin and crispy with loads of filling.</s>",
 '<pad>we ordered coffee and were also',
 '<pad> manu makes this look like one of the Parisan tourist sushi places. set menu, lots of brochettes, not really great fish, but we were pleasantly suprised.</s>',
 '<pad> the food was always well presented, authentic French cooking at its best. the staff are welcoming, polite and...will assist with a little english if help required.</s>',
 '<pad> the vegetarian biryani is flavourful, the Dahl is not the right lentil so it taste quite grainy. overall, good service, decent Indian food, but wish it...was more authentic.</s>',
 '<pad>the waitress was very helpful and quick',
 '<pad> a typical busy, cheerful french bar/brasserie in the city centre. food was good but not great, I asked for mussels but no creme. service was friendly and...nothing was too much trouble.</s>',
 "<pad> aigle celeste, vannes, britany, is a popular 'chinese buffet' restaurant. there are a wide selection of dishes from french style charcouterie to sushi, seafood, whole crabs, oysters, mussels and all the ususal chinese favorites. aigle celeste is located just off the motorway.</s>",
 "<pad> the restaurant Madame is definitly the'Hostess with the mostess. breakfast had to be pre ordered, this too was rather substantial.</s>",
 '<pad>the restaurant is run mostly by ladies of the 3 generations (one cooking, one managing and one serving',
 "<pad> a lovely spot to watch the world go by on a busy market day in vannes. table de jeanne was recommended to us by our hotel but we couldn't get a table. staff were very efficient, very nice. note menus are in french, the manager had some english but...generally the staff did not.</s>",
 "<pad> i'm currently exploring the town of vannes. ordered a drink and asked the server for their wi-fi code. the server returned and paid my bill and left.</s>",
 "<pad> a 13 yr old ordered a'veggie burger' which came enclosed in grease filled potato hash browns. the patty was reportedly worse than frozen and had to give all napkins to wipe from hand. Across from that same old is an incredible crêperie.</s>",
 "<pad> the restaurant is in a wonderful location, but the food is sort of 'expensive chic'. the menus are unnecessarily complicated, especially as you can mix and match them, some with supplements. the staff are helpful and efficient and the food is excellent.</s>",
 '<pad>the last time we visited it was for lunch this time we were in Vannes. the service was as good as last',
 "<pad>cozyL'ardoise was a breath of fresh air. service was quick & wonderful",
 '<pad> the pizzeria grill capri was a life saver for us as we passed through Vannes. we were starving and ordered four plate-sized pizzas with various toppings. the pizzas were wonderful, thin, crispy crusts and fresh, flavorful ingredients.</s>',
 '<pad> great spot for very good wine, a tasty cheese board and good service. the wine was 3euros a glass and very good.</s>',
 "<pad> the waiter slammed a ham and goat's cheese salad in front of us without a word of apology. he then slammed the plates in front of us with such a force that some of the boiling hot water cascaded from the teapot, narrowly missing my leg. he is the rudest man that i have ever had the misfortune to encounter.</s>",
 '<pad>artisan/specialty coffee, knowledgeable baristas and excellent latte art. the taste was very close to the traditional italian cappuccino. the cha',
 '<pad> Opposite the fish market but not serving the freshest of fish. we chose to visit this atmospheric restaurant because we expected the fish to be the freshest of the fresh. but when our fish arrived it was tough, chewy, grey looking. Definitely not the freshest.</s>',
 '<pad>a very good',
 '<pad> the restaurant is one of very few open for dinner on a major holiday. it is located in the heart of the bustling centre of vannes. the food is delicious and the staff are friendly and helpful.</s>',
 '<pad> une honte is a restaurant in the Mercure Vannes Le Port hotel. it is located in a very convenient location. the service was good and the food was very tasty. the waiter refused to take wine orders.</s>',
 '<pad>the food was perfectly cooked and yummy as. the food was perfectly cooked and delicious as.',
 '<pad> the atmosphere is great; plants, books and the floor of moza<unk> ek. a bit different from the usual french with a modern twist.</s>',
 '<pad> the steak was delicious and the menu had a lot of choices. the price is quite good and i am very satisfied with the service.</s>',
 '<pad>Magnifique!!!An amazing restaurant run by lovely people. They made us feel very welcome and relaxed. Massive selection of wines and the nicest',
 '<pad> the cafe de conleau is within the Hotel Le Roof building, but separate menu, although served by the same kitchen as the Hotel. the meal we had here was delightful, slightly less expensive than the main Hotel but the same nice surroundings.</s>',
 "<pad> the service was very friendly and the food was reasonable value for money. it's the first time we had poor service in our holiday in britany.</s>",
 '<pad> the staff was very friendly and patient with my inadequate French. the prices were reasonable and the atmosphere in the café was quite welcoming.</s>',
 '<pad>a SATISFIED VACATIONMagda the chef is a professional.',
 '<pad> despite being busy, the service was very good and the food was excellent. despite being busy, the staff looked extremely stressed and rushing around like they were chasing time. despite being half empty and full of staff, the place still appeared to be very disorganised.</s>',
 '<pad>Le Yeti is a lovely family run restaurant located just on the edge of the old town. the menu is varied though has',
 '<pad>chocolate excellent and a cherry sorbet which although it tasted good was',
 '<pad>FriendlyPopped in for breakfast as the breakfast served at out hotel was overpriced. service is OK,',
 "<pad> the creperie de la Tour Trompette is hidden in the city ramparts in the basement of a tower. it has a cavernous, fairytale ambience, but that's evidently its selling point, rather than the food. the food is average and the price is almost twice as much as elsewhere.</s>",
 '<pad>fast food of good quality, seating in',
 '<pad>sardine and salmon gal',
 '<pad>the reraurant is',
 '<pad>a really good craft beer menu and',
 '<pad>burgers were nice',
 '<pad> opposite the train station, great staff who were polite, cheerful and efficient. fish & chips (13.50€) were extremely...tasty as was my cheesecake.</s>',
 '<pad>the Campanile Restaurant at Vannes is not a Michelin Guide restaurant. the restaurant offers a buffet style',
 '<pad>a disaster trying to get something to eat for the family across the square in jeanne',
 '<pad>quick, cheap eatBy the entrance',
 '<pad>this is one of the best places to enjoy a coffee and pastry',
 '<pad>nice clean comfortable seating area and prompt service. fish was beautifully cooked and very well presented',
 '<pad> service was friendly and relatively quick for our large group of 15. food is excellent and the quality of the boards is excellent. one suggestion is the sardines dish which are just to die for.</s>',
 '<pad>the buffolo and doner were the best kebab in brittany. the',
 '<pad>the view of the cafe is better than the view from it, but it is a nice setting on the',
 '<pad>Outside of Vannes Centre',
 '<pad>la Boucherie is a restaurant of the chain "la boucherie" in vannes',
 '<pad>pizzahubby and hubby decided to have a takeaway pizza for dinner. he ordered a box of mixed pizza slices',
 "<pad> the restaurant is a classic provincial french restaurant. it's in a quiet setting by the river and there is outside seating. the food was enjoyable and the service was slick.</s>"]
# Exemple de DataFrame

def reco(trydta):
    trydta = [text[5:] for text in trydta]
    from transformers import pipeline

    # Chargement du modèle d'analyse de sentiment
    sentiment_analyzer = pipeline("sentiment-analysis")

    recommendations = []

    # Utilisez le modèle de prédiction de sentiment pour chaque phrase
    for sentence in trydta:
        sentiment_result = sentiment_analyzer(sentence)
        sentiment_label = sentiment_result[0]['label']
        recommendations.append(sentiment_label)
    data = {'input': trydta, 'output': recommendations}
    df = pd.DataFrame({
        'id': range(len(trydta)),
        'input': trydta,
        'output': recommendations  # Les sentiments prédits que vous avez calculés précédemment
    })
    reviews = df['input'].tolist()
    from sklearn.feature_extraction.text import TfidfVectorizer

    # Création du vectoriseur TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    review_vectors = vectorizer.fit_transform(reviews)
    return review_vectors,vectorizer,df



def get_top_recommendations(df,user_query, review_vectors, top_n=3):
    query_vector = vectorizer.transform([user_query])
    similarities = cosine_similarity(query_vector, review_vectors)
    top_indices = np.argsort(similarities[0])[::-1][:top_n]
    top_reviews = df.iloc[top_indices]
    return top_reviews



# Streamlit app
st.title("WebScrapping Project : Restaurant Recommender 😋​🥙​🍲​🥗​")
st.subheader("By Maud Tissot, Arthur Scelles, Aurélien Pouxviel")

# Menu cliquable pour le sommaire
menu = st.sidebar.radio("Menu", ["Home", "Recommendations"])
if menu == "Home":
    st.write("Welcome to Restaurant Recommender! Enter your restaurant preferences in the search box on the left.")
else:
    review_vectors,vectorizer,df = reco(trydta)
    user_query = st.text_input("🔎 Enter your restaurant preferences 🔎 (I'm looking for a cozy cafe with a great view)", "")


    # Plus loin dans le code Streamlit
    if user_query:
        top_reviews = get_top_recommendations(df,user_query, review_vectors)
        for index, row in top_reviews.iterrows():
            st.write(f"Restaurant ID 🔥: {row['id']}")
            st.write(f"Similar Review 👉: {row['input']}")
            st.write("-----")

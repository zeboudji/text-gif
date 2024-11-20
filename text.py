import streamlit as st
import random
import re
import time
from collections import defaultdict
import matplotlib.pyplot as plt

# 1. Configurer la page (doit être le premier appel Streamlit)
st.set_page_config(page_title="Simulation IA : Choix Pondéré", layout="wide")

# 2. Appliquer des styles CSS en ligne pour une apparence moderne et responsive
st.markdown("""
    <style>
    /* Conteneur principal */
    .container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }

    /* Phrase animée avec effet de fondu */
    .animated-text {
        font-size: 2em;
        color: #ffffff;
        transition: all 0.5s ease-in-out;
        text-align: center;
        word-wrap: break-word;
        animation: fadeIn 0.5s ease-in-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Options et probabilités */
    .probabilities {
        font-size: 1.2em;
        color: #87CEFA;
        margin-top: 20px;
    }

    /* Texte final */
    .final-text {
        font-size: 2.5em;
        color: #32CD32;
        margin-top: 30px;
        text-align: center;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .animated-text {
            font-size: 1.5em;
        }
        .probabilities {
            font-size: 1em;
        }
        .final-text {
            font-size: 2em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Fonction pour afficher les probabilités sous forme de graphique
def display_probabilities(options):
    labels = [opt['word'] for opt in options]
    sizes = [opt['probability'] for opt in options]
    colors = ['#FFA500', '#87CEFA', '#32CD32', '#FF6347', '#FFD700', '#9370DB', '#40E0D0', '#FF69B4', '#CD5C5C', '#F08080']
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, colors=colors[:len(labels)], autopct='%1.1f%%', startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

# 4. Fonction pour simuler l'animation dans Streamlit
def simulate_animation(sentence, options, selected_word, scale_factor=1):
    prob_weights = [opt["probability"] for opt in options]
    prob_texts = [f"{opt['word']} : {opt['probability']}%" for opt in options]
    
    # Créer des placeholders pour l'animation
    sentence_placeholder = st.empty()
    probs_placeholder = st.empty()
    final_placeholder = st.empty()
    
    # Animation aléatoire
    for _ in range(20):
        chosen_option = random.choices(options, weights=prob_weights, k=1)[0]
        random_word = chosen_option["word"]
        random_prob = chosen_option["probability"]
        
        # Créer la phrase animée avec des styles HTML
        animated_sentence = sentence.replace(
            selected_word, f"<span style='color:#FFA500;'>[{random_word} ({random_prob}%)]</span>"
        )
        
        # Afficher la phrase animée avec une taille de police agrandie et centrée
        sentence_html = f"<div class='animated-text'>{animated_sentence}</div>"
        sentence_placeholder.markdown(sentence_html, unsafe_allow_html=True)
        
        # Afficher les probabilités des options sous forme de graphique
        probs_html = "<div class='probabilities'>Options et Probabilités :</div>"
        display_probabilities(options)
        
        time.sleep(0.3)  # Pause de 300 ms entre les frames
    
    # Afficher le résultat final
    final_option = max(options, key=lambda x: x["probability"])
    final_word = final_option["word"]
    final_prob = final_option["probability"]
    final_sentence = sentence.replace(
        selected_word, f"<span style='color:#32CD32;'>[{final_word} ({final_prob}%)]</span>"
    )
    final_text = f"Le mot choisi est : <strong>{final_word} ({final_prob}%)</strong> ! 🎉"
    
    # Afficher la phrase finale
    final_sentence_html = f"<div class='animated-text'>{final_sentence}</div>"
    sentence_placeholder.markdown(final_sentence_html, unsafe_allow_html=True)
    
    # Afficher le texte final
    final_text_html = f"<div class='final-text'>{final_text}</div>"
    final_placeholder.markdown(final_text_html, unsafe_allow_html=True)

# 5. Fonction pour exécuter des simulations multiples et afficher les résultats
def run_simulations(sentence, options, selected_word, num_simulations=100):
    results = defaultdict(int)
    prob_weights = [opt["probability"] for opt in options]
    
    for _ in range(num_simulations):
        chosen_option = random.choices(options, weights=prob_weights, k=1)[0]
        results[chosen_option['word']] += 1
    
    # Afficher les résultats sous forme de graphique à barres
    labels = list(results.keys())
    sizes = list(results.values())
    colors = ['#FFA500', '#87CEFA', '#32CD32', '#FF6347', '#FFD700', '#9370DB', '#40E0D0', '#FF69B4', '#CD5C5C', '#F08080']
    
    fig, ax = plt.subplots()
    ax.bar(labels, sizes, color=colors[:len(labels)])
    ax.set_xlabel('Options')
    ax.set_ylabel('Nombre de Sélections')
    ax.set_title(f'Resultats des Simulations ({num_simulations} Choix)')
    st.pyplot(fig)

# 6. Interface utilisateur Streamlit
st.title("🧠 Simulation IA : Choix Pondéré avec Contexte")
st.markdown("""
### 📚 Introduction à l'IA et aux Probabilités Pondérées

L'intelligence artificielle (IA) prend souvent des décisions basées sur des **probabilités pondérées**. Cela signifie que chaque option possible se voit attribuer une probabilité, et l'IA choisit parmi ces options en fonction de ces probabilités.

**Exemple Simplifié :**
Imaginez que vous avez trois choix pour le dîner : Pizza (50%), Sushi (30%), et Salade (20%). Une IA utilisant des probabilités pondérées choisirait la Pizza 50% du temps, le Sushi 30% du temps, et la Salade 20% du temps.

Cette application interactive vous permet de visualiser comment une IA peut faire de tels choix basés sur des probabilités définies.
""")

# Étape 1 : Entrée de la phrase
sentence = st.text_area(
    "📄 Entrez une phrase :",
    placeholder="Exemple : Toulouse est la ville rose."
)

if sentence:
    # Étape 2 : Sélection d'un mot à animer
    words = re.findall(r'\b\w+\b', sentence)  # Extraction des mots sans ponctuation
    selected_word = st.selectbox("🔍 Choisissez un mot à animer :", words)
    
    if selected_word:
        st.markdown(f"**Vous avez choisi :** `<span style='color:#1E90FF;'>{selected_word}</span>`", unsafe_allow_html=True)
        
        # Étape 3 : Ajouter des options avec leurs probabilités
        st.subheader("📝 Définir les options et leurs probabilités")
        num_options = st.number_input("Nombre de choix possibles :", min_value=2, max_value=10, value=3, step=1)
        options = []
        for i in range(int(num_options)):
            st.markdown(f"**Option {i + 1}**")
            col1, col2 = st.columns([3, 1])
            with col1:
                word = st.text_input(f"Option {i + 1} :", key=f"word_{i}")
            with col2:
                prob = st.number_input(f"Probabilité {i + 1} (%) :", min_value=1, max_value=100, value=50, key=f"prob_{i}")
            
            if word:
                options.append({"word": word, "probability": prob})
        
        # Étape 4 : Validation des probabilités et génération
        if len(options) == int(num_options):
            total_prob = sum([opt["probability"] for opt in options])
            if total_prob > 100:
                st.error(f"La somme des probabilités est de **{total_prob}%**, ce qui dépasse 100%. Veuillez ajuster les valeurs.")
            elif total_prob < 100:
                st.warning(f"La somme des probabilités est de **{total_prob}%**, ce qui est inférieur à 100%. Assurez-vous que la somme est correcte.")
            else:
                if st.button("🚀 Générer l'animation"):
                    with st.spinner("Génération de l'animation en cours..."):
                        try:
                            simulate_animation(sentence, options, selected_word, scale_factor=1)
                            st.success("🎉 Animation terminée !")
                            
                            # Optionnel : Lancer des simulations multiples pour démontrer les résultats statistiques
                            if st.checkbox("📊 Voir les résultats des simulations multiples (100 choix)"):
                                run_simulations(sentence, options, selected_word, num_simulations=100)
                        except Exception as e:
                            st.error(f"⚠️ Une erreur s'est produite lors de l'animation : {e}")
        else:
            st.error("❗ Veuillez remplir toutes les options avec leurs probabilités.")

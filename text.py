import streamlit as st
import random
import re
import time

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

    /* Phrase animée */
    .animated-text {
        font-size: 2em;
        color: #ffffff;
        transition: all 0.5s ease-in-out;
        text-align: center;
        word-wrap: break-word;
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

# 3. Fonction pour simuler l'animation dans Streamlit
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
        
        # Afficher les probabilités des options
        probs_html = "<div class='probabilities'>Options et Probabilités :</div>"
        probs_html += "<ul style='list-style-type: none; padding: 0; text-align: center;'>"
        for prob in prob_texts:
            probs_html += f"<li>{prob}</li>"
        probs_html += "</ul>"
        probs_placeholder.markdown(probs_html, unsafe_allow_html=True)
        
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

# 4. Interface utilisateur Streamlit
st.title("🧠 Simulation IA : Choix Pondéré avec Contexte")
st.write("""
Saisissez une phrase, sélectionnez un mot à animer, et attribuez des probabilités pour voir comment l'IA fait son choix !
""")

# Étape 1 : Entrée de la phrase
sentence = st.text_area(
    "Entrez une phrase :",
    placeholder="Exemple : Toulouse est la ville rose."
)

if sentence:
    # Étape 2 : Sélection d'un mot à animer
    words = re.findall(r'\b\w+\b', sentence)  # Extraction des mots sans ponctuation
    selected_word = st.selectbox("Choisissez un mot à animer :", words)
    
    if selected_word:
        st.markdown(f"**Vous avez choisi :** `<span style='color:#1E90FF;'>{selected_word}</span>`", unsafe_allow_html=True)
        
        # Étape 3 : Ajouter des options avec leurs probabilités
        st.subheader("Définir les options et leurs probabilités")
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
                if st.button("Générer l'animation"):
                    with st.spinner("Génération de l'animation en cours..."):
                        try:
                            simulate_animation(sentence, options, selected_word, scale_factor=1)
                            st.success("L'IA a fait son choix en fonction du mot le plus probable dans sa base de données, plus la base de données est conséquente plus la reponse sera robuste !")
                        except Exception as e:
                            st.error(f"Une erreur s'est produite lors de l'animation : {e}")
        else:
            st.error("Veuillez remplir toutes les options avec leurs probabilités.")

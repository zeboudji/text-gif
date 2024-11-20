import streamlit as st
import random
import re
import time

# Fonction pour simuler l'animation dans Streamlit
def simulate_animation(sentence, options, selected_word, scale_factor=2):
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
        
        # Créer la phrase animée
        animated_sentence = sentence.replace(selected_word, f"<span style='color:orange;'>[{random_word} ({random_prob}%)]</span>")
        
        # Afficher la phrase animée avec une taille de police agrandie
        sentence_html = f"<h2 style='font-size:{30 * scale_factor}px;'>{animated_sentence}</h2>"
        sentence_placeholder.markdown(sentence_html, unsafe_allow_html=True)
        
        # Afficher les probabilités des options
        probs_html = "<h3 style='font-size:{0}px;'>Options et Probabilités :</h3>".format(20 * scale_factor)
        probs_html += "<ul style='font-size:{0}px;'>".format(18 * scale_factor)
        for prob in prob_texts:
            probs_html += f"<li style='color:lightblue;'>{prob}</li>"
        probs_html += "</ul>"
        probs_placeholder.markdown(probs_html, unsafe_allow_html=True)
        
        time.sleep(0.3)  # Pause de 300 ms entre les frames
    
    # Afficher le résultat final
    final_option = max(options, key=lambda x: x["probability"])
    final_word = final_option["word"]
    final_prob = final_option["probability"]
    final_sentence = sentence.replace(selected_word, f"<span style='color:green;'>[{final_word} ({final_prob}%)]</span>")
    final_text = f"<h2 style='font-size:{35 * scale_factor}px; color:green;'>Le mot choisi est : <strong>{final_word} ({final_prob}%)</strong> ! 🎉</h2>"
    
    # Afficher la phrase finale
    sentence_placeholder.markdown(final_sentence.replace("\n", "<br>"), unsafe_allow_html=True)
    
    # Afficher le texte final
    final_placeholder.markdown(final_text, unsafe_allow_html=True)
    
    # Optionnel : Afficher les probabilités une dernière fois
    # probs_placeholder.markdown(probs_html, unsafe_allow_html=True)

# Application Streamlit
st.set_page_config(page_title="Simulation IA : Choix Pondéré", layout="wide")
st.title("🧠 Simulation IA : Choix Pondéré avec Contexte")
st.write("Saisissez une phrase, sélectionnez un mot à animer, et attribuez des probabilités pour voir comment l'IA fait son choix !")

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
        st.markdown(f"**Vous avez choisi :** `<span style='color:blue;'>{selected_word}</span>`", unsafe_allow_html=True)
        
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
                            simulate_animation(sentence, options, selected_word, scale_factor=3)
                            st.success("Animation terminée !")
                        except Exception as e:
                            st.error(f"Une erreur s'est produite lors de l'animation : {e}")
        else:
            st.error("Veuillez remplir toutes les options avec leurs probabilités.")

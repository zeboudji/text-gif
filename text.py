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

    /* Étapes de réflexion */
    .step {
        font-size: 1.5em;
        color: #ffffff;
        background-color: #2F4F4F;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
        width: 80%;
        transition: all 0.5s ease-in-out;
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
        .step {
            font-size: 1.2em;
            width: 95%;
        }
        .final-text {
            font-size: 2em;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Fonction pour simuler l'animation des étapes de réflexion de l'IA
def simulate_reflection(sentence, options, selected_word):
    prob_weights = [opt["probability"] for opt in options]
    prob_texts = [f"{opt['word']} : {opt['probability']}%" for opt in options]
    
    # Créer des placeholders pour les étapes
    step1_placeholder = st.empty()
    step2_placeholder = st.empty()
    step3_placeholder = st.empty()
    step4_placeholder = st.empty()
    final_placeholder = st.empty()
    
    # Étape 1 : Analyse des options
    step1_html = f"""
    <div class='step'>
        <strong>Étape 1 : Analyse des Options</strong><br>
        L'IA analyse les options disponibles pour remplacer le mot <em><strong>{selected_word}</strong></em> dans la phrase.
    </div>
    """
    step1_placeholder.markdown(step1_html, unsafe_allow_html=True)
    time.sleep(2)  # Pause de 2 secondes

    # Étape 2 : Évaluation des Probabilités
    step2_html = f"""
    <div class='step'>
        <strong>Étape 2 : Évaluation des Probabilités</strong><br>
        Chaque option se voit attribuer une probabilité de sélection basée sur son importance ou sa pertinence.
    </div>
    """
    step2_placeholder.markdown(step2_html, unsafe_allow_html=True)
    time.sleep(2)  # Pause de 2 secondes

    # Étape 3 : Comparaison des Options
    step3_html = f"""
    <div class='step'>
        <strong>Étape 3 : Comparaison des Options</strong><br>
        L'IA compare les probabilités attribuées à chaque option pour déterminer laquelle a le plus de chances d'être sélectionnée.
    </div>
    """
    step3_placeholder.markdown(step3_html, unsafe_allow_html=True)
    time.sleep(2)  # Pause de 2 secondes

    # Étape 4 : Prise de Décision
    chosen_option = random.choices(options, weights=prob_weights, k=1)[0]
    step4_html = f"""
    <div class='step'>
        <strong>Étape 4 : Prise de Décision</strong><br>
        Basé sur les probabilités, l'IA sélectionne l'option <em><strong>{chosen_option['word']}</strong></em> avec une probabilité de <strong>{chosen_option['probability']}%</strong>.
    </div>
    """
    step4_placeholder.markdown(step4_html, unsafe_allow_html=True)
    time.sleep(2)  # Pause de 2 secondes

    # Résultat Final
    final_sentence = sentence.replace(selected_word, f"<strong>{chosen_option['word']}</strong>")
    final_text_html = f"""
    <div class='final-text'>
        🎉 **Résultat Final :**<br>
        La phrase finale est : <br>
        <em>{final_sentence}</em>
    </div>
    """
    final_placeholder.markdown(final_text_html, unsafe_allow_html=True)

# 4. Interface utilisateur Streamlit
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
                            simulate_reflection(sentence, options, selected_word)
                            st.success("🎉 Animation terminée !")
                        except Exception as e:
                            st.error(f"⚠️ Une erreur s'est produite lors de l'animation : {e}")
        else:
            st.error("❗ Veuillez remplir toutes les options avec leurs probabilités.")

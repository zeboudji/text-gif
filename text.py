import streamlit as st
import random
import re
import time

# 1. Configurer la page (doit être le premier appel Streamlit)
st.set_page_config(page_title="🧠 Simulation IA : Choix Pondéré Réaliste", layout="wide")

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

# 3. Fonction pour simuler les étapes de réflexion de l'IA
def simulate_reflection(sentence, options, selected_word):
    prob_weights = [opt["probability"] for opt in options]
    
    # Créer des placeholders pour les étapes
    step1_placeholder = st.empty()
    step2_placeholder = st.empty()
    step3_placeholder = st.empty()
    step4_placeholder = st.empty()
    final_placeholder = st.empty()
    
    # Étape 1 : Encodage du Contexte
    step1_html = f"""
    <div class='step'>
        <strong>Étape 1 : Encodage du Contexte</strong><br>
        L'IA analyse la phrase : <em>{sentence}</em><br>
        Elle identifie le mot cible à remplacer : <strong>{selected_word}</strong>.<br>
        Grâce aux embeddings et au mécanisme d'attention, l'IA comprend le contexte global de la phrase.
    </div>
    """
    step1_placeholder.markdown(step1_html, unsafe_allow_html=True)
    time.sleep(3)  # Pause de 3 secondes
    
    # Étape 2 : Calcul des Probabilités
    step2_html = f"""
    <div class='step'>
        <strong>Étape 2 : Calcul des Probabilités</strong><br>
        Pour chaque option, l'IA calcule la probabilité qu'elle soit le prochain mot, basée sur les données d'entraînement.<br>
        Ces probabilités reflètent la pertinence de chaque mot dans le contexte donné.
    </div>
    """
    step2_placeholder.markdown(step2_html, unsafe_allow_html=True)
    
    # Affichage des probabilités
    prob_html = "<ul style='list-style-type: none; padding: 0;'>"
    for opt in options:
        prob_html += f"<li>{opt['word']} : {opt['probability']}%</li>"
    prob_html += "</ul>"
    step2_placeholder.markdown(prob_html, unsafe_allow_html=True)
    time.sleep(3)  # Pause de 3 secondes
    
    # Étape 3 : Sélection Basée sur les Probabilités
    step3_html = f"""
    <div class='step'>
        <strong>Étape 3 : Sélection Basée sur les Probabilités</strong><br>
        L'IA utilise un algorithme de sélection pondérée pour choisir le prochain mot.<br>
        Cela peut être fait en sélectionnant le mot avec la plus haute probabilité ou en échantillonnant selon la distribution des probabilités pour introduire de la diversité.
    </div>
    """
    step3_placeholder.markdown(step3_html, unsafe_allow_html=True)
    time.sleep(3)  # Pause de 3 secondes
    
    # Étape 4 : Prise de Décision
    chosen_option = random.choices(options, weights=prob_weights, k=1)[0]
    step4_html = f"""
    <div class='step'>
        <strong>Étape 4 : Prise de Décision</strong><br>
        L'IA sélectionne l'option <strong>{chosen_option['word']}</strong> avec une probabilité de <strong>{chosen_option['probability']}%</strong>.
    </div>
    """
    step4_placeholder.markdown(step4_html, unsafe_allow_html=True)
    time.sleep(3)  # Pause de 3 secondes
    
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
st.title("🧠 Simulation IA : Choix Pondéré Réaliste")

st.markdown("""
### 📚 Comprendre le Fonctionnement d'une IA Générative

Les IA génératives, comme GPT, sont conçues pour prédire le prochain mot dans une phrase en se basant sur les mots précédents. Elles utilisent des **probabilités** pour déterminer quel mot est le plus approprié à ajouter à la suite.

**Comment cela fonctionne-t-il ?**

1. **Encodage du Contexte :** L'IA examine les mots déjà présents dans la phrase en utilisant des embeddings et des mécanismes d'attention pour comprendre le contexte global.
2. **Calcul des Probabilités :** Pour chaque mot possible, l'IA calcule une probabilité basée sur les données d'entraînement. Ces probabilités reflètent la pertinence et la cohérence du mot dans le contexte donné.
3. **Sélection du Mot :** L'IA choisit le mot avec la probabilité la plus élevée ou sélectionne un mot de manière aléatoire en fonction de ces probabilités pour introduire de la diversité.
4. **Prise de Décision :** Le mot sélectionné est ajouté à la phrase, et le processus peut se répéter pour les mots suivants.

Cette application interactive vous permet de visualiser comment une IA générative peut faire de tels choix basés sur des probabilités définies.
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
        
        # Validation des probabilités
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

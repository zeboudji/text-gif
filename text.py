import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import re
import os

# Fonction pour charger une police TTF personnalisée
def load_font(font_size):
    try:
        # Téléchargez une police plus esthétique ou utilisez une police système
        # Ici, j'utilise une police standard pour la simplicité
        return ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback à la police par défaut si la police personnalisée n'est pas trouvée
        return ImageFont.load_default()

# Fonction pour créer une animation GIF
def create_probability_animation(sentence, options, selected_word, output_path="animated_choice.gif"):
    font_sentence = load_font(24)  # Taille de police pour la phrase
    font_probs = load_font(18)     # Taille de police pour les probabilités
    font_final = load_font(28)     # Taille de police pour le texte final

    frames = []

    # Calculer la somme des probabilités pour validation
    total_prob = sum([opt["probability"] for opt in options])

    # Étape 1 : Animation aléatoire
    for _ in range(20):  # Nombre de frames pour simuler le défilement rapide
        # Sélectionner un mot basé sur les probabilités
        chosen_option = random.choices(
            options, weights=[opt["probability"] for opt in options], k=1
        )[0]
        random_word = chosen_option["word"]
        random_prob = chosen_option["probability"]

        # Remplacer le mot sélectionné par le mot animé avec son pourcentage entre crochets
        animated_sentence = sentence.replace(
            selected_word, f"[{random_word} ({random_prob}%)]"
        )

        # Créer une image pour chaque frame
        img = Image.new("RGB", (1000, 300), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Afficher la phrase animée
        draw.text((50, 50), animated_sentence, fill=(0, 0, 0), font=font_sentence)

        # Afficher les probabilités des options en bas de l'image
        draw.text((50, 150), "Options et Probabilités :", fill=(0, 0, 0), font=font_probs)
        for i, opt in enumerate(options):
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((70, 180 + i * 30), prob_text, fill=(0, 0, 0), font=font_probs)

        frames.append(img)

    # Étape 2 : Afficher la phrase finale avec le mot ayant la plus grande probabilité
    final_option = max(options, key=lambda x: x["probability"])
    final_word = final_option["word"]
    final_prob = final_option["probability"]
    final_sentence = sentence.replace(
        selected_word, f"[{final_word} ({final_prob}%)]"
    )

    # Ajouter un texte supplémentaire pour indiquer le mot choisi
    final_text = f"Le mot choisi est : {final_word} ({final_prob}%) !"

    for _ in range(15):  # 15 frames pour insister sur le résultat final
        img = Image.new("RGB", (1000, 350), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Afficher la phrase finale
        draw.text((50, 50), final_sentence, fill=(0, 0, 0), font=font_sentence)
        # Afficher le texte final
        draw.text((50, 200), final_text, fill=(0, 100, 0), font=font_final)

        # Afficher les probabilités des options en bas de l'image
        draw.text((50, 250), "Options et Probabilités :", fill=(0, 0, 0), font=font_probs)
        for i, opt in enumerate(options):
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((70, 280 + i * 30), prob_text, fill=(0, 0, 0), font=font_probs)

        frames.append(img)

    # Sauvegarder l'animation avec une durée de 500 ms par frame pour une vitesse modérée
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=500,  # 500 ms par frame
        loop=0
    )
    return output_path

# Application Streamlit
st.set_page_config(page_title="Simulation IA : Choix Pondéré", layout="wide")
st.title("Simulation IA : Choix Pondéré avec Contexte 🧠")
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
        st.markdown(f"**Vous avez choisi :** `{selected_word}`")

        # Étape 3 : Ajouter des options avec leurs probabilités
        st.subheader("Définir les options et leurs probabilités")
        num_options = st.number_input("Nombre de choix possibles :", min_value=2, max_value=10, value=3)
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
                        gif_path = create_probability_animation(sentence, options, selected_word)
                    st.success("Animation générée avec succès !")

                    # Afficher l'animation
                    st.image(gif_path, caption="Simulation IA : Processus de choix", use_column_width=True)

                    # Afficher le mot choisi
                    final_option = max(options, key=lambda x: x["probability"])
                    st.markdown(f"### Résultat Final : **{final_option['word']} ({final_option['probability']}%)** a été choisi ! 🎉")

        else:
            st.error("Veuillez remplir toutes les options avec leurs probabilités.")


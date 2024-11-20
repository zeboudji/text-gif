import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random

# Fonction pour créer une animation GIF
def create_probability_animation(sentence, options, selected_word, output_path="animated_choice.gif"):
    font = ImageFont.load_default()
    frames = []

    # Étape 1 : Animation aléatoire
    for _ in range(20):  # Nombre de frames pour simuler le défilement rapide
        random_word = random.choices(
            [opt["word"] for opt in options], weights=[opt["probability"] for opt in options]
        )[0]
        animated_sentence = sentence.replace(selected_word, random_word)

        # Créer une image
        img = Image.new("RGB", (800, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 80), animated_sentence, fill=(0, 0, 0), font=font)

        # Ajouter les probabilités visibles
        for i, opt in enumerate(options):
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((10, 140 + i * 20), prob_text, fill=(0, 0, 0), font=font)

        frames.append(img)

    # Étape 2 : Afficher la phrase finale
    final_word = max(options, key=lambda x: x["probability"])["word"]
    final_sentence = sentence.replace(selected_word, f"{final_word} ({max(options, key=lambda x: x['probability'])['probability']}%)")
    for _ in range(10):  # 10 frames pour insister sur le résultat final
        img = Image.new("RGB", (800, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 80), final_sentence, fill=(0, 0, 0), font=font)

        # Ajouter les probabilités visibles
        for i, opt in enumerate(options):
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((10, 140 + i * 20), prob_text, fill=(0, 0, 0), font=font)

        frames.append(img)

    # Sauvegarder l'animation
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=200, loop=0)
    return output_path

# Streamlit Application
st.title("Simulation IA : Choix pondéré avec contexte 🧠")
st.write("Saisissez une phrase, sélectionnez un mot et attribuez des probabilités pour voir comment l'IA fait son choix !")

# Étape 1 : Entrée de la phrase
sentence = st.text_area("Entrez une phrase :", placeholder="Exemple : Toulouse est la ville rose.")

if sentence:
    # Étape 2 : Sélection d'un mot à animer
    words = sentence.split()
    selected_word = st.selectbox("Choisissez un mot à animer :", words)

    if selected_word:
        st.write(f"Vous avez choisi : {selected_word}")

        # Étape 3 : Ajouter des options avec leurs probabilités
        num_options = st.number_input("Nombre de choix possibles :", min_value=2, max_value=10, value=3)
        options = []
        for i in range(num_options):
            col1, col2 = st.columns([2, 1])
            with col1:
                word = st.text_input(f"Option {i + 1} :", placeholder=f"Mot {i + 1}")
            with col2:
                prob = st.number_input(f"Probabilité {i + 1} (%) :", min_value=1, max_value=100, value=50)

            if word:
                options.append({"word": word, "probability": prob})

        # Étape 4 : Validation des probabilités et génération
        if len(options) > 1 and sum([opt["probability"] for opt in options]) == 100:
            if st.button("Générer l'animation"):
                with st.spinner("Génération en cours..."):
                    gif_path = create_probability_animation(sentence, options, selected_word)
                st.success("Animation générée avec succès !")

                # Afficher l'animation
                st.image(gif_path, caption="Simulation IA : Processus de choix", use_column_width=True)
        else:
            st.error("Assurez-vous que les probabilités totalisent exactement 100%.")


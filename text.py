import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random

# Fonction pour créer une animation GIF
def create_probability_animation(sentence, options, selected_word, output_path="animated_choice.gif"):
    font = ImageFont.load_default()
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
        img = Image.new("RGB", (800, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 50), animated_sentence, fill=(0, 0, 0), font=font)

        # Afficher les probabilités des options en bas de l'image
        for i, opt in enumerate(options):
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((10, 150 + i * 20), prob_text, fill=(0, 0, 0), font=font)

        frames.append(img)

    # Étape 2 : Afficher la phrase finale avec le mot ayant la plus grande probabilité
    final_option = max(options, key=lambda x: x["probability"])
    final_word = final_option["word"]
    final_prob = final_option["probability"]
    final_sentence = sentence.replace(
        selected_word, f"[{final_word} ({final_prob}%)]"
    )

    for _ in range(10):  # 10 frames pour insister sur le résultat final
        img = Image.new("RGB", (800, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 50), final_sentence, fill=(0, 0, 0), font=font)

        # Afficher les probabilités des options en bas de l'image
        for i, opt in enumerate(options):
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((10, 150 + i * 20), prob_text, fill=(0, 0, 0), font=font)

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
st.title("Simulation IA : Choix pondéré avec contexte 🧠")
st.write("Saisissez une phrase, sélectionnez un mot à animer, et attribuez des probabilités pour voir comment l'IA fait son choix !")

# Étape 1 : Entrée de la phrase
sentence = st.text_area(
    "Entrez une phrase :",
    placeholder="Exemple : Toulouse est la ville rose."
)

if sentence:
    # Étape 2 : Sélection d'un mot à animer
    words = sentence.split()
    selected_word = st.selectbox("Choisissez un mot à animer :", words)

    if selected_word:
        st.write(f"Vous avez choisi : **{selected_word}**")

        # Étape 3 : Ajouter des options avec leurs probabilités
        st.subheader("Définir les options et leurs probabilités")
        num_options = st.number_input("Nombre de choix possibles :", min_value=2, max_value=10, value=3)
        options = []
        for i in range(num_options):
            st.markdown(f"**Option {i + 1}**")
            col1, col2 = st.columns([2, 1])
            with col1:
                word = st.text_input(f"Option {i + 1} :", key=f"word_{i}")
            with col2:
                prob = st.number_input(f"Probabilité {i + 1} (%) :", min_value=1, max_value=100, value=50, key=f"prob_{i}")

            if word:
                options.append({"word": word, "probability": prob})

        # Étape 4 : Validation des probabilités et génération
        if len(options) == num_options:
            total_prob = sum([opt["probability"] for opt in options])
            if total_prob > 100:
                st.error("La somme des probabilités dépasse 100%. Veuillez ajuster les valeurs.")
            elif total_prob < 100:
                st.warning("La somme des probabilités est inférieure à 100%. Assurez-vous que la somme est correcte.")
            else:
                if st.button("Générer l'animation"):
                    with st.spinner("Génération en cours..."):
                        gif_path = create_probability_animation(sentence, options, selected_word)
                    st.success("Animation générée avec succès !")

                    # Afficher l'animation
                    st.image(gif_path, caption="Simulation IA : Processus de choix", use_column_width=True)
        else:
            st.error("Veuillez remplir toutes les options avec leurs probabilités.")

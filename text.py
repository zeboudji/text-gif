import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random

# Fonction pour créer un GIF animé
def create_animated_gif(selected_word, percentage, output_path="animated_word.gif"):
    # Configuration
    font = ImageFont.load_default()
    frames = []

    # Étape 1 : Animer rapidement avec des mots aléatoires
    for _ in range(20):  # Nombre de frames pour le défilement
        text = f"Votre mot sélectionné est [{selected_word if random.randint(1, 100) <= percentage else '...'}]"
        img = Image.new("RGB", (600, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 80), text, fill=(0, 0, 0), font=font)
        frames.append(img)

    # Étape 2 : Focus sur le mot final
    final_text = f"Votre mot sélectionné est [{selected_word}] !"
    for _ in range(10):
        img = Image.new("RGB", (600, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 80), final_text, fill=(0, 0, 0), font=font)
        frames.append(img)

    # Sauvegarder le GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
    return output_path

# Streamlit Application
st.title("Animation de mots avec Streamlit 🎥")
st.write("Saisissez un texte, choisissez un mot, attribuez un pourcentage, et voyez le résultat !")

# Étape 1 : Saisie du texte
user_text = st.text_area("Entrez un texte :", placeholder="Exemple : Marseille Paris Lyon Bordeaux Nice")
if user_text:
    words = user_text.split()
    # Étape 2 : Sélection d'un mot
    selected_word = st.selectbox("Choisissez un mot à animer :", words)

    # Étape 3 : Choix du pourcentage
    percentage = st.slider("Pourcentage d'apparition du mot :", min_value=1, max_value=100, value=50)

    # Étape 4 : Bouton pour générer l'animation
    if st.button("Générer l'animation"):
        with st.spinner("Génération en cours..."):
            gif_path = create_animated_gif(selected_word, percentage)
        st.success("GIF généré avec succès !")
        st.image(gif_path, caption="Animation de votre mot", use_column_width=True)


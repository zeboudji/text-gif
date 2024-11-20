import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random

# Fonction pour créer une animation GIF montrant le processus de choix
def create_probability_animation(words_with_probabilities, output_path="animated_choice.gif"):
    font = ImageFont.load_default()
    frames = []
    all_words = [item["word"] for item in words_with_probabilities]

    # Étape 1 : Animation aléatoire pour simuler le choix
    for _ in range(20):  # 20 frames pour simuler le défilement rapide
        random_word = random.choices(
            all_words, weights=[item["probability"] for item in words_with_probabilities]
        )[0]
        text = f"Choix actuel : [{random_word}]"
        
        # Créer une image pour chaque étape
        img = Image.new("RGB", (600, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 50), text, fill=(0, 0, 0), font=font)

        # Afficher les probabilités des autres mots
        for i, item in enumerate(words_with_probabilities):
            draw.text((10, 100 + i * 20), f"{item['word']} : {item['probability']}%", fill=(0, 0, 0), font=font)
        frames.append(img)

    # Étape 2 : Afficher le mot final (le mot avec la plus grande probabilité)
    final_word = max(words_with_probabilities, key=lambda x: x["probability"])["word"]
    final_text = f"Mot final choisi : [{final_word}]"
    for _ in range(10):  # 10 frames pour insister sur le résultat final
        img = Image.new("RGB", (600, 200), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        draw.text((10, 50), final_text, fill=(0, 0, 0), font=font)
        for i, item in enumerate(words_with_probabilities):
            draw.text((10, 100 + i * 20), f"{item['word']} : {item['probability']}%", fill=(0, 0, 0), font=font)
        frames.append(img)

    # Sauvegarder l'animation GIF
    frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=100, loop=0)
    return output_path

# Streamlit Application
st.title("Animation du processus de choix par l'IA 🎥")
st.write("Saisissez des mots avec leurs probabilités pour voir comment l'IA fait son choix.")

# Étape 1 : Saisie des mots et probabilités
st.write("Ajoutez vos mots avec leurs probabilités (entre 1 et 100).")
words = st.text_area("Entrez des mots séparés par des virgules :", placeholder="Exemple : Marseille, Paris, Lyon")
probabilities = st.text_area(
    "Entrez les probabilités correspondantes séparées par des virgules :", placeholder="Exemple : 20, 50, 30"
)

if st.button("Générer l'animation"):
    if words and probabilities:
        # Convertir les entrées utilisateur en listes
        word_list = words.split(",")
        probability_list = probabilities.split(",")

        try:
            # Vérification et conversion des probabilités
            probability_list = [int(p.strip()) for p in probability_list]
            if len(word_list) != len(probability_list):
                st.error("Le nombre de mots et de probabilités doit être identique.")
            elif sum(probability_list) > 100:
                st.error("La somme des probabilités ne doit pas dépasser 100.")
            else:
                # Créer une liste de dictionnaires pour les mots et probabilités
                words_with_probabilities = [
                    {"word": word.strip(), "probability": prob}
                    for word, prob in zip(word_list, probability_list)
                ]

                # Générer l'animation
                with st.spinner("Génération en cours..."):
                    gif_path = create_probability_animation(words_with_probabilities)
                st.success("Animation générée avec succès !")
                st.image(gif_path, caption="Processus de choix par l'IA", use_column_width=True)

        except ValueError:
            st.error("Veuillez entrer des probabilités valides (nombres entiers).")
    else:
        st.error("Veuillez remplir les champs pour générer l'animation.")

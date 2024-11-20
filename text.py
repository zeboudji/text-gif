import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import re
import random

# Fonction pour extraire les options et probabilités d'une phrase
def extract_options(sentence):
    matches = re.findall(r"\[(.*?)\((\d+)%\)\]", sentence)
    options = [{"word": match[0].strip(), "probability": int(match[1])} for match in matches]
    return options

# Fonction pour créer une animation GIF
def create_probability_animation(sentence, options, output_path="animated_choice.gif"):
    font = ImageFont.load_default()
    frames = []

    # Étape 1 : Animation aléatoire
    for _ in range(20):  # Nombre de frames pour simuler le défilement rapide
        random_word = random.choices(
            [opt["word"] for opt in options], weights=[opt["probability"] for opt in options]
        )[0]
        animated_sentence = re.sub(r"\[.*?\]", f"[{random_word}]", sentence)

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
    final_sentence = re.sub(r"\[.*?\]", f"[{final_word} ({max(options, key=lambda x: x['probability'])['probability']}%)]", sentence)
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
st.write("Saisissez une phrase avec des options entre crochets, associées à des probabilités, et voyez comment l'IA sélectionne !")

# Entrée utilisateur
sentence = st.text_area(
    "Entrez votre phrase (format : [option (probabilité%)]):",
    placeholder="Exemple : Toulouse est la ville [rose (50%)][jaune (20%)][chaude (20%)]",
)

# Bouton pour générer l'animation
if st.button("Générer l'animation"):
    if sentence:
        # Extraire les options et probabilités
        options = extract_options(sentence)

        if options:
            # Générer l'animation
            with st.spinner("Génération en cours..."):
                gif_path = create_probability_animation(sentence, options)
            st.success("Animation générée avec succès !")

            # Afficher l'animation et le résultat final
            st.image(gif_path, caption="Simulation IA : Processus de choix", use_column_width=True)
        else:
            st.error("Aucune option valide trouvée dans la phrase.")
    else:
        st.error("Veuillez entrer une phrase valide.")

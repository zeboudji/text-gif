import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import re
import os
from io import BytesIO
import textwrap

# Fonction pour charger une police par défaut avec une taille spécifique
def load_default_font(font_size):
    try:
        # Utiliser une police truetype intégrée si disponible
        return ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        # Fallback à la police par défaut bitmap
        st.warning("Police Arial non trouvée. Utilisation de la police par défaut de Pillow.")
        return ImageFont.load_default()

# Fonction pour ajuster la taille de la police en fonction de la largeur maximale
def get_font_and_wrapped_text(text, font_path, max_width, initial_size=60):
    font_size = initial_size
    font = load_default_font(font_size)
    wrapped_lines = textwrap.wrap(text, width=40)  # Nombre de caractères par ligne
    
    while True:
        # Calculer la largeur de chaque ligne
        line_widths = []
        for line in wrapped_lines:
            if isinstance(font, ImageFont.FreeTypeFont):
                bbox = font.getbbox(line)
                line_width = bbox[2] - bbox[0]
            else:
                # Pour les polices bitmap, utiliser getsize
                line_width = font.getsize(line)[0]
            line_widths.append(line_width)
        
        if max(line_widths) <= max_width or font_size <= 20:
            break
        font_size -= 2
        font = load_default_font(font_size)
    
    return font, wrapped_lines

# Fonction pour créer une animation GIF avec texte wrapped
def create_probability_animation(sentence, options, selected_word, output_path="animated_choice.gif"):
    # Charger les polices avec des tailles dynamiques
    initial_font_size_sentence = 60
    initial_font_size_probs = 40
    initial_font_size_final = 50

    # Couleurs
    background_color = (40, 40, 40)      # Fond sombre
    text_color = (255, 255, 255)         # Texte blanc
    prob_title_color = (255, 215, 0)     # Or pour le titre des probabilités
    prob_text_color = (135, 206, 250)    # Bleu clair pour les probabilités
    final_text_color = (0, 255, 0)       # Vert vif pour le texte final

    # Dimensions de l'image pour mieux accueillir le texte agrandi
    img_width = 1920
    img_height = 1080

    frames = []

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

        # Ajuster la taille de la police pour la phrase et envelopper le texte
        font_sentence, wrapped_sentence = get_font_and_wrapped_text(
            animated_sentence, "arial.ttf", img_width - 200, initial_size=60
        )

        # Créer une image pour chaque frame
        img = Image.new("RGB", (img_width, img_height), color=background_color)
        draw = ImageDraw.Draw(img)

        # Afficher la phrase animée
        y_text = 100
        for line in wrapped_sentence:
            draw.text((100, y_text), line, fill=text_color, font=font_sentence)
            y_text += font_sentence.getsize(line)[1] + 10  # Espacement entre les lignes

        # Afficher les probabilités des options en bas de l'image
        draw.text((100, 600), "Options et Probabilités :", fill=prob_title_color, font=load_default_font(initial_font_size_probs))
        y_prob = 700
        for opt in options:
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((150, y_prob), prob_text, fill=prob_text_color, font=load_default_font(initial_font_size_probs))
            y_prob += load_default_font(initial_font_size_probs).getsize(prob_text)[1] + 10

        frames.append(img)

    # Étape 2 : Afficher la phrase finale avec le mot ayant la plus grande probabilité
    final_option = max(options, key=lambda x: x["probability"])
    final_word = final_option["word"]
    final_prob = final_option["probability"]
    final_sentence = sentence.replace(
        selected_word, f"[{final_word} ({final_prob}%)]"
    )

    final_text = f"Le mot choisi est : {final_word} ({final_prob}%) !"

    # Ajuster la taille de la police pour la phrase finale et envelopper le texte
    font_sentence_final, wrapped_final_sentence = get_font_and_wrapped_text(
        final_sentence, "arial.ttf", img_width - 200, initial_size=60
    )
    font_final_text = load_default_font(initial_font_size_final)

    for _ in range(30):  # Augmenter le nombre de frames pour une pause plus longue
        img = Image.new("RGB", (img_width, img_height + 100), color=background_color)
        draw = ImageDraw.Draw(img)

        # Afficher la phrase finale
        y_text = 100
        for line in wrapped_final_sentence:
            draw.text((100, y_text), line, fill=text_color, font=font_sentence_final)
            y_text += font_sentence_final.getsize(line)[1] + 10  # Espacement entre les lignes

        # Afficher le texte final
        draw.text((100, 600), final_text, fill=final_text_color, font=font_final_text)

        # Afficher les probabilités des options en bas de l'image
        draw.text((100, 700), "Options et Probabilités :", fill=prob_title_color, font=load_default_font(initial_font_size_probs))
        y_prob = 800
        for opt in options:
            prob_text = f"{opt['word']} : {opt['probability']}%"
            draw.text((150, y_prob), prob_text, fill=prob_text_color, font=load_default_font(initial_font_size_probs))
            y_prob += load_default_font(initial_font_size_probs).getsize(prob_text)[1] + 10

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

# Fonction pour convertir le GIF en bytes pour le téléchargement
def get_gif_bytes(file_path):
    with open(file_path, "rb") as f:
        return f.read()

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
        st.markdown(f"**Vous avez choisi :** `{selected_word}`")

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
                            gif_path = create_probability_animation(sentence, options, selected_word)
                            st.success("Animation générée avec succès !")

                            # Afficher l'animation
                            st.image(gif_path, caption="📈 Simulation IA : Processus de choix", use_column_width=True)

                            # Afficher le mot choisi
                            final_option = max(options, key=lambda x: x["probability"])
                            st.markdown(f"### 🎉 Résultat Final : **{final_option['word']} ({final_option['probability']}%)** a été choisi !")

                            # Permettre le téléchargement du GIF
                            gif_bytes = get_gif_bytes(gif_path)
                            st.download_button(
                                label="📥 Télécharger le GIF",
                                data=gif_bytes,
                                file_name="animated_choice.gif",
                                mime="image/gif"
                            )
                        except Exception as e:
                            st.error(f"Une erreur s'est produite lors de la génération du GIF : {e}")
        else:
            st.error("Veuillez remplir toutes les options avec leurs probabilités.")

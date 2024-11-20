import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import re
from io import BytesIO
import textwrap
import time

# Fonction pour charger la police par défaut
def load_font():
    return ImageFont.load_default()

# Fonction pour dessiner le texte sur une image
def draw_text(image, text, position, font, color):
    draw = ImageDraw.Draw(image)
    draw.text(position, text, font=font, fill=color)

# Fonction pour créer une image avec le texte
def create_image(animated_sentence, prob_texts, final=False, final_text="", img_width=600, img_height=400, scale_factor=2):
    # Créer une image avec fond sombre
    img = Image.new("RGB", (img_width, img_height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Charger les polices avec des tailles agrandies
    font_sentence = load_font()
    font_probs = load_font()
    font_final = load_font()
    
    # Dessiner la phrase animée avec des espacements fixes
    y_text = 20
    draw_text(img, animated_sentence, (20, y_text), font_sentence, (255, 255, 255))
    y_text += 20  # Espacement fixe entre les lignes

    if not final:
        # Dessiner les probabilités des options
        draw_text(img, "Options et Probabilités :", (20, y_text), font_probs, (255, 215, 0))
        y_text += 20  # Espacement fixe
        for prob_text in prob_texts:
            draw_text(img, prob_text, (40, y_text), font_probs, (135, 206, 250))
            y_text += 15  # Espacement fixe entre les probabilités
    else:
        # Dessiner le texte final
        draw_text(img, final_text, (20, y_text), font_final, (0, 255, 0))
        y_text += 20  # Espacement fixe

        # Dessiner les probabilités des options
        draw_text(img, "Options et Probabilités :", (20, y_text), font_probs, (255, 215, 0))
        y_text += 20  # Espacement fixe
        for prob_text in prob_texts:
            draw_text(img, prob_text, (40, y_text), font_probs, (135, 206, 250))
            y_text += 15  # Espacement fixe entre les probabilités

    # Redimensionner l'image pour agrandir le texte
    img = img.resize((img_width * scale_factor, img_height * scale_factor), Image.NEAREST)
    return img

# Fonction pour créer une animation GIF avec texte agrandi via redimensionnement
def create_probability_animation(sentence, options, selected_word, output_path="animated_choice.gif"):
    frames = []

    # Couleurs
    background_color = (30, 30, 30)      # Fond sombre
    text_color = (255, 255, 255)         # Texte blanc
    prob_title_color = (255, 215, 0)     # Or pour le titre des probabilités
    prob_text_color = (135, 206, 250)    # Bleu clair pour les probabilités
    final_text_color = (0, 255, 0)       # Vert vif pour le texte final

    # Dimensions de base (plus petite)
    base_width = 600
    base_height = 400

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

        # Préparer les textes des probabilités
        prob_texts = [f"{opt['word']} : {opt['probability']}%" for opt in options]

        # Créer et ajouter le frame
        frame = create_image(animated_sentence, prob_texts, final=False, img_width=base_width, img_height=base_height)
        frames.append(frame)

    # Étape 2 : Afficher la phrase finale avec le mot ayant la plus grande probabilité
    final_option = max(options, key=lambda x: x["probability"])
    final_word = final_option["word"]
    final_prob = final_option["probability"]
    final_sentence = sentence.replace(
        selected_word, f"[{final_word} ({final_prob}%)]"
    )

    # Ajouter un texte supplémentaire pour indiquer le mot choisi
    final_text = f"Le mot choisi est : {final_word} ({final_prob}%) !"

    # Préparer les textes des probabilités
    prob_texts = [f"{opt['word']} : {opt['probability']}%" for opt in options]

    for _ in range(30):  # Augmenter le nombre de frames pour une pause plus longue
        frame = create_image(final_sentence, prob_texts, final=True, final_text=final_text, img_width=base_width, img_height=base_height)
        frames.append(frame)

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

import streamlit as st
import numpy as np
import pickle
from PIL import Image
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import cosine_similarity


@st.cache_resource
def load_my_model():
    return load_model("mobilenetv2_food.keras", compile=False)

@st.cache_resource
def load_encoders_and_vectors():
    # Load label encoders
    with open("label_encoders.pkl", "rb") as f:
        label_encoders = pickle.load(f)

    # Load encoded vectors
    ingredients_encoded = np.load("ingredients_encoded.npy")
    description_encoded = np.load("description_encoded.npy")

    # Load original texts
    with open("text_data.pkl", "rb") as f:
        text_data = pickle.load(f)

    return label_encoders, ingredients_encoded, description_encoded, text_data

model = load_my_model()
label_encoders, ingredients_encoded, description_encoded, text_data = load_encoders_and_vectors()


def closest_description(vector, encoded_matrix, original_texts):
    sims = cosine_similarity([vector], encoded_matrix)[0]
    return original_texts[np.argmax(sims)]


st.title("🍲 Food Classifier (MobileNetV2)")

uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display input image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # Preprocess
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict
    food_pred, region_pred, health_pred, ingr_pred, desc_pred = model.predict(img_array)

    # Decode categorical predictions
    food_class = label_encoders["Food_Name"].inverse_transform([np.argmax(food_pred)])[0]
    region_class = label_encoders["Region"].inverse_transform([np.argmax(region_pred)])[0]
    health_class = label_encoders["Food_Health"].inverse_transform([np.argmax(health_pred)])[0]

    # Map vectors to closest text
    ingredient_text = closest_description(ingr_pred[0], ingredients_encoded, text_data["ingredients"])
    description_text = closest_description(desc_pred[0], description_encoded, text_data["description"])

    # Display results
    st.subheader("🔎 Prediction Results")
    st.write(f"**Food Name:** {food_class}")
    st.write(f"**Region:** {region_class}")
    st.write(f"**Health:** {health_class}")
    st.write(f"**Main Ingredients:** {ingredient_text}")
    st.write(f"**Procedure/Description:** {description_text}")


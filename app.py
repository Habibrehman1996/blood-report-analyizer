import os
import pytesseract
from PIL import Image
from transformers import pipeline
import streamlit as st

# Install Tesseract on Streamlit Cloud during runtime
os.system("apt-get update && apt-get install -y tesseract-ocr")

# Set Tesseract executable path for pytesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load Hugging Face Model for Text Classification
@st.cache_resource
def load_model():
    return pipeline('text-classification', model="distilbert-base-uncased", return_all_scores=True)

classifier = load_model()

# Streamlit UI
st.title("AI Blood Report Analyzer")
st.write("Upload an image of your blood report. The app will extract text using OCR and analyze the extracted text for potential conditions.")

# File Uploader
uploaded_image = st.file_uploader("Upload a Blood Report Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Blood Report", use_column_width=True)

        # Extract text using Tesseract OCR
        st.subheader("Step 1: Extracting Text from Image...")
        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            st.error("No text found in the uploaded image. Please try again with a clearer image.")
        else:
            # Display extracted text
            st.text_area("Extracted Text", extracted_text, height=200)

            # Analyze text using Hugging Face pipeline
            st.subheader("Step 2: Analyzing Extracted Text...")
            truncated_text = extracted_text[:512]  # Hugging Face models have a 512-character limit
            classification_results = classifier(truncated_text)

            # Display Classification Results
            st.write("### Potential Conditions and Confidence Levels:")
            for result in classification_results[0]:
                st.write(f"- **{result['label']}**: {round(result['score'] * 100, 2)}% confidence")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

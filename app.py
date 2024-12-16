import os
import streamlit as st
from transformers import pipeline
from PIL import Image
import pytesseract

# Install Tesseract at runtime for Streamlit Cloud
os.system("apt-get update && apt-get install -y tesseract-ocr")

# Load Hugging Face Model
@st.cache_resource
def load_model():
    return pipeline('text-classification', model="distilbert-base-uncased", return_all_scores=True)

classifier = load_model()

# Title and Description
st.title("AI Blood Report Analyzer")
st.write(
    "Upload an image of your blood report, and the app will extract the text using OCR and analyze it for potential conditions."
)

# File Uploader
uploaded_image = st.file_uploader("Upload Blood Report Image (JPEG/PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Blood Report", use_column_width=True)

        # Step 1: Extract text using Tesseract OCR
        st.subheader("Extracting Text from Image...")
        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            st.error("No readable text found in the image. Please upload a clearer image.")
        else:
            st.text_area("Extracted Text", extracted_text, height=200)

            # Step 2: Analyze text using Hugging Face model
            st.subheader("Analyzing Extracted Text...")
            truncated_text = extracted_text[:512]  # Limit to 512 characters for compatibility
            classification_results = classifier(truncated_text)

            # Display Classification Results
            st.write("### Potential Conditions and Confidence Levels:")
            for entry in classification_results[0]:
                st.write(f"- **{entry['label']}**: {round(entry['score'] * 100, 2)}% confidence")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

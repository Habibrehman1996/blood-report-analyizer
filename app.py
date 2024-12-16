import easyocr
from PIL import Image
import streamlit as st

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Streamlit UI
st.title("AI Blood Report Analyzer")
st.write("Upload an image of your blood report. The app will extract text using OCR.")

# File Uploader
uploaded_image = st.file_uploader("Upload a Blood Report Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Blood Report", use_column_width=True)

        # Extract text using EasyOCR
        st.subheader("Extracting Text from Image...")
        extracted_text = reader.readtext(image, detail=0)

        if not extracted_text:
            st.error("No text found in the uploaded image. Please try again with a clearer image.")
        else:
            # Display extracted text
            extracted_text_combined = "\n".join(extracted_text)
            st.text_area("Extracted Text", extracted_text_combined, height=200)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

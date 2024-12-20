import easyocr
from PIL import Image
import streamlit as st
import numpy as np
import re

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Define normal ranges with full and short forms
NORMAL_RANGES = {
    "Hemoglobin": (13.5, 17.5),  # g/dL for males
    "Hb": (13.5, 17.5),          # Alternate name for Hemoglobin
    "Red Blood Cell": (4.7, 6.1),  # million/μL for males
    "RBC": (4.7, 6.1),             # Alternate name for Red Blood Cell
    "White Blood Cell": (4.5, 11.0),  # thousand/μL
    "WBC": (4.5, 11.0),               # Alternate name for White Blood Cell
    "Platelets": (150, 450),          # thousand/μL
    "Plt": (150, 450),                # Alternate name for Platelets
}

# Function to analyze extracted text
def analyze_blood_report(extracted_text):
    report = []
    for parameter, (low, high) in NORMAL_RANGES.items():
        # Search for both full and short forms in the text using regex
        match = re.search(rf"{parameter}.*?(\d+\.?\d*)", extracted_text, re.IGNORECASE)
        if match:
            value = float(match.group(1))
            if low <= value <= high:
                report.append(f"{parameter}: {value} (Normal)")
            else:
                report.append(f"{parameter}: {value} (Out of Range: Normal {low}-{high})")
        else:
            report.append(f"{parameter}: Not Found in Report")
    return "\n".join(report)

# Streamlit UI
st.title("AI Blood Report Analyzer")
st.write("Upload an image of your blood report. The app will extract text and analyze the results.")

# File Uploader
uploaded_image = st.file_uploader("Upload a Blood Report Image (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    try:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Blood Report", use_column_width=True)

        # Convert image to NumPy array
        image_np = np.array(image)

        # Extract text using EasyOCR
        st.subheader("Extracting Text from Image...")
        extracted_text_list = reader.readtext(image_np, detail=0, paragraph=True)
        extracted_text_combined = " ".join(extracted_text_list).lower()

        # Display raw extracted text for debugging
        st.subheader("Extracted Text (Debugging)")
        st.text_area("Raw Extracted Text", extracted_text_combined, height=200)

        if not extracted_text_combined.strip():
            st.error("No text found in the uploaded image. Please try again with a clearer image.")
        else:
            # Analyze blood report
            st.subheader("Analysis of Blood Report")
            analysis = analyze_blood_report(extracted_text_combined)
            st.text_area("Analysis Results", analysis, height=200)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

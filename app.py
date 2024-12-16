import easyocr
from PIL import Image
import streamlit as st
import re

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'], gpu=False)

# Define normal ranges for common blood parameters
NORMAL_RANGES = {
    "Hemoglobin": (13.5, 17.5),  # g/dL for males
    "RBC": (4.7, 6.1),           # million/μL for males
    "WBC": (4.5, 11.0),          # thousand/μL
    "Platelets": (150, 450),     # thousand/μL
}

# Function to analyze extracted text
def analyze_blood_report(extracted_text):
    report = []
    for parameter, (low, high) in NORMAL_RANGES.items():
        # Search for parameter in the text using regex
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
st.write("Upload an image of your blood report. The app will analyze the results.")

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
        extracted_text_combined = " ".join(extracted_text)

        if not extracted_text_combined.strip():
            st.error("No text found in the uploaded image. Please try again with a clearer image.")
        else:
            # Display extracted text
            st.text_area("Extracted Text", extracted_text_combined, height=200)

            # Analyze blood report
            st.subheader("Analysis of Blood Report")
            analysis = analyze_blood_report(extracted_text_combined)
            st.text_area("Analysis Results", analysis, height=200)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

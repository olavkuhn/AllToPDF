import os
from PIL import Image
import streamlit as st

st.title("Mom's File-to-PDF Converter")
st.write("Easily turn your images or files into a clean PDF.")

# File uploader widget
uploaded_file = st.file_uploader(
    "Choose an image file", type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
  # Open image using Pillow
  image = Image.open(uploaded_file)
  rgb_image = image.convert("RGB")

  # Save to a temporary path or bytes buffer
  output_pdf_path = "converted_document.pdf"
  rgb_image.save(output_pdf_path, "PDF", resolution=100.0)

  st.success("Successfully converted!")

  # Provide a download button for your mom
  with open(output_pdf_path, "rb") as pdf_file:
    st.download_button(
        label="Download PDF",
        data=pdf_file,
        file_name="converted_output.pdf",
        mime="application/pdf",
    )
import os
from PIL import Image
import streamlit as st

# 1. Page Configuration (Sets the browser tab title and layout)
st.set_page_config(page_title="Mom's PDF Converter", page_icon="📄", layout="centered")

# 2. Custom Styling (A little bit of CSS to make text larger and friendlier)
st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Header Section
st.markdown('<p class="main-title">📄 Mom\'s PDF Maker</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Turn your photos into a clean PDF with one click!</p>',
    unsafe_allow_html=True,
)

# Add a visual separator line
st.divider()

# 4. File Upload Section
st.markdown("### Step 1: Choose your image")
uploaded_file = st.file_uploader(
    "Upload a picture (PNG, JPG, JPEG)", type=["png", "jpg", "jpeg"]
)

# 5. Conversion Logic & Preview
if uploaded_file is not None:
  # Show a preview so she knows she uploaded the right picture
  st.image(
      uploaded_file, caption="Here is your uploaded picture:", use_container_width=True
  )

  st.markdown("### Step 2: Download your PDF")

  # Process image to PDF
  image = Image.open(uploaded_file)
  rgb_image = image.convert("RGB")

  output_pdf_path = "converted_document.pdf"
  rgb_image.save(output_pdf_path, "PDF", resolution=100.0)

  # Big, prominent download button
  with open(output_pdf_path, "rb") as pdf_file:
    st.download_button(
        label="📥 Click Here to Download PDF",
        data=pdf_file,
        file_name="mom_document.pdf",
        mime="application/pdf",
        type="primary",  # Makes the button stand out with color
    )

# 6. Helpful footer for mom
st.divider()
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.9rem;'>Made with ❤️ just for you.</p>",
    unsafe_allow_html=True,
)
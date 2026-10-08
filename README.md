# 📄 PDF Maker
 
A simple, minimalistic [Streamlit](https://streamlit.io/) app to convert files to PDF locally.
 
Made to easily convert files on your own machine, mainly for personal use.
 
![Made with Claude](https://img.shields.io/badge/Made%20with-Claude-D97757?style=for-the-badge&logo=claude&logoColor=white)
![Made with Gemini](https://img.shields.io/badge/Made%20with-Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)
 
> 🤖 100% made by **Gemini** and **Claude**.
 
## ✨ Features
 
- Clean interface with big buttons and clear steps: upload → convert → download
- Automatic file type detection based on the file extension
- Preview before downloading (images and text)
- Everything runs locally, nothing is uploaded to a third party
- Supported formats:
  - Images: `JPG`, `JPEG`, `PNG`, `WEBP` (via Pillow)
  - Text: `TXT` (via fpdf2)
  - Word: `DOCX` (basic: text and headings only, via python-docx)
## 🚀 Getting started
 
This project uses [uv](https://docs.astral.sh/uv/).
 
```bash
# Install dependencies
uv add streamlit pillow fpdf2 python-docx
 
# Run the app
uv run streamlit run main.py
```
 
Then open the URL shown in the terminal (usually http://localhost:8501).
 
## 🔤 Fonts (optional)
 
For special characters (é, ë, €, ...) in `TXT` and `DOCX` conversions, the app looks for the `DejaVuSans.ttf` font:
 
1. `fonts/DejaVuSans.ttf` next to `main.py`
2. Common system font locations on Linux
If it isn't found, the app falls back to Helvetica and unsupported characters are replaced by `?`.
 
## ⚠️ Limitations
 
- `DOCX` conversion is basic: images, tables and formatting are not preserved.
- Only one file is converted at a time.
## 📝 Notes
 
Built for personal use, so expect no guarantees or support. Feel free to fork and adapt it.

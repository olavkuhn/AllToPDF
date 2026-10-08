"""PDF-maker: zet afbeeldingen, tekstbestanden en Word-bestanden om naar PDF.

Starten:  uv run streamlit run main.py
"""

from io import BytesIO
from pathlib import Path

import streamlit as st
from fpdf import FPDF
from PIL import Image, ImageOps

# ---------------------------------------------------------------------------
# Instellingen
# ---------------------------------------------------------------------------
IMAGE_TYPES = ["jpg", "jpeg", "png", "webp"]
TEXT_TYPES = ["txt"]
WORD_TYPES = ["docx"]
ALL_TYPES = IMAGE_TYPES + TEXT_TYPES + WORD_TYPES

# Een lettertype met Unicode-ondersteuning (voor é, ë, €, enz.).
# Leg bij voorkeur DejaVuSans.ttf in een map "fonts" naast dit bestand.
FONT_CANDIDATES = [
    Path(__file__).parent / "fonts" / "DejaVuSans.ttf",
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/TTF/DejaVuSans.ttf"),
]

st.set_page_config(page_title="PDF Maker", page_icon="📄", layout="centered")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.6rem; color: #2c3e50; text-align: center; margin-bottom: 0;
    }
    .subtitle {
        font-size: 1.25rem; color: #7f8c8d; text-align: center; margin-bottom: 1.5rem;
    }
    h3 { font-size: 1.7rem !important; }
    /* Grote, duidelijke knoppen */
    .stDownloadButton button, .stButton button {
        font-size: 1.5rem; padding: 1rem 1.5rem; width: 100%;
    }
    [data-testid="stFileUploaderDropzone"] { padding: 2rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Conversiefuncties: elk geeft de PDF terug als bytes
# ---------------------------------------------------------------------------
def image_to_pdf(data: bytes) -> bytes:
    image = Image.open(BytesIO(data))
    image = ImageOps.exif_transpose(image)  # telefoonfoto's goed draaien

    # Transparantie (PNG/WEBP) vervangen door een witte achtergrond
    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        image = image.convert("RGBA")
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.getchannel("A"))
        image = background
    else:
        image = image.convert("RGB")

    buffer = BytesIO()
    image.save(buffer, "PDF", resolution=100.0)
    return buffer.getvalue()


def _new_text_pdf() -> tuple[FPDF, bool]:
    """Maakt een lege PDF en geeft terug of Unicode-lettertype beschikbaar is."""
    pdf = FPDF(format="A4")
    pdf.set_margins(20, 20, 20)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    for font_path in FONT_CANDIDATES:
        if font_path.exists():
            pdf.add_font("DejaVu", "", str(font_path))
            pdf.set_font("DejaVu", size=12)
            return pdf, True

    pdf.set_font("Helvetica", size=12)  # alleen Latin-1 tekens
    return pdf, False


def _write_lines(pdf: FPDF, lines: list[tuple[str, int]], unicode_ok: bool) -> bytes:
    """Schrijft (tekst, lettergrootte)-regels naar de PDF."""
    font_name = "DejaVu" if unicode_ok else "Helvetica"
    for text, size in lines:
        if not unicode_ok:
            text = text.encode("latin-1", "replace").decode("latin-1")
        pdf.set_font(font_name, size=size)
        if text.strip() == "":
            pdf.ln(size * 0.5)
        else:
            pdf.multi_cell(0, size * 0.5, text, new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())


def decode_text(data: bytes) -> str:
    for encoding in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def text_to_pdf(data: bytes) -> bytes:
    text = decode_text(data).replace("\t", "    ")
    pdf, unicode_ok = _new_text_pdf()
    lines = [(line, 12) for line in text.splitlines()]
    return _write_lines(pdf, lines, unicode_ok)


def docx_to_pdf(data: bytes) -> bytes:
    """Eenvoudige conversie: tekst en koppen. Afbeeldingen/opmaak gaan verloren."""
    from docx import Document  # pas hier importeren; alleen nodig voor DOCX

    document = Document(BytesIO(data))
    pdf, unicode_ok = _new_text_pdf()

    lines: list[tuple[str, int]] = []
    for paragraph in document.paragraphs:
        style = paragraph.style.name if paragraph.style is not None else ""
        if style == "Title":
            size = 20
        elif style.startswith("Heading"):
            size = 16
        else:
            size = 12
        lines.append((paragraph.text, size))
    return _write_lines(pdf, lines, unicode_ok)


def convert(extension: str, data: bytes) -> bytes:
    """Kiest automatisch de juiste conversie op basis van de extensie."""
    if extension in IMAGE_TYPES:
        return image_to_pdf(data)
    if extension in TEXT_TYPES:
        return text_to_pdf(data)
    if extension in WORD_TYPES:
        return docx_to_pdf(data)
    raise ValueError(f"Bestandstype .{extension} wordt niet ondersteund.")


# ---------------------------------------------------------------------------
# Interface
# ---------------------------------------------------------------------------
st.markdown('<p class="main-title">📄 PDF Maker</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Zet je foto of document met één klik om naar een PDF</p>',
    unsafe_allow_html=True,
)
st.divider()

# Stap 1 -----------------------------------------------------------------
st.markdown("### Stap 1: Kies je bestand")
uploaded_file = st.file_uploader(
    "Foto (JPG, PNG, WEBP), tekstbestand (TXT) of Word-bestand (DOCX)",
    type=ALL_TYPES,
)

if uploaded_file is not None:
    file_bytes = uploaded_file.getvalue()
    extension = Path(uploaded_file.name).suffix.lower().lstrip(".")

    # Voorbeeld ---------------------------------------------------------
    if extension in IMAGE_TYPES:
        st.image(uploaded_file, caption="Dit is je foto", use_container_width=True)
    elif extension in TEXT_TYPES:
        with st.expander("Bekijk het begin van je tekst", expanded=True):
            st.text(decode_text(file_bytes)[:1500])
    else:
        st.info(f"📎 Word-bestand gekozen: {uploaded_file.name}")

    # Stap 2 -------------------------------------------------------------
    st.markdown("### Stap 2: Omzetten naar PDF")
    try:
        with st.spinner("Even geduld, je PDF wordt gemaakt..."):
            pdf_bytes = convert(extension, file_bytes)
    except Exception:
        st.error(
            "😕 Dit bestand kon niet worden omgezet. "
            "Probeer een ander bestand, of vraag Olav om hulp."
        )
        st.stop()

    st.success("✅ Klaar! Je PDF is gemaakt.")

    # Stap 3 -------------------------------------------------------------
    st.markdown("### Stap 3: Download je PDF")
    st.download_button(
        label="📥 Klik hier om de PDF te downloaden",
        data=pdf_bytes,
        file_name=f"{Path(uploaded_file.name).stem}.pdf",
        mime="application/pdf",
        type="primary",
    )

st.divider()
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 0.9rem;'>"
    "Met ❤️ gemaakt speciaal voor jou.</p>",
    unsafe_allow_html=True,
)
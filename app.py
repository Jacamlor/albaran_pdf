
import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd

st.set_page_config(page_title="Visualizador de Albaranes", layout="wide")
st.title("📦 Visualizador de Albaranes FRIKING")

uploaded_file = st.file_uploader("🔼 Sube un albarán PDF generado por PowerShop", type="pdf")

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    raw_text = ""
    for page in doc:
        raw_text += page.get_text()

    # Patrón para extraer datos del artículo
    pattern = r"(H\.CTAM\.[A-Z0-9]+CTAMC\d+)\s+([^\n]+)\s+S\s+M\s+L\s+XL\s+2XL\s+3XL\s*((?:\d+\s*){1,6})\s+([^\n]+)\s+[\d,]+\s+[\d,]+\s+[\d,]+"

    matches = re.findall(pattern, raw_text)

    if matches:
        filtro = st.text_input("🔍 Filtra por código o nombre del producto")

        for cod_full, nombre, tallas_str, color in matches:
            if filtro.lower() not in cod_full.lower() and filtro.lower() not in nombre.lower():
                continue

            tallas = re.findall(r"\d+", tallas_str)
            tallas += ['0'] * (6 - len(tallas))  # Rellenar si faltan tallas

            tallas_dict = dict(zip(["S", "M", "L", "XL", "2XL", "3XL"], tallas))

            with st.expander(f"{cod_full} - {nombre.strip()}", expanded=True):
                st.markdown(f"**🎨 Color:** {color.strip()}")
                st.markdown(f"**🆔 Código completo:** `{cod_full}`")
                st.markdown("**📏 Cantidades por talla:**")
                st.table(pd.DataFrame([tallas_dict]))
    else:
        st.warning("No se encontraron artículos en el PDF. Asegúrate de que el formato es correcto.")
else:
    st.info("Por favor, sube un archivo PDF para comenzar.")

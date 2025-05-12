
import streamlit as st
import fitz  # PyMuPDF
import pandas as pd
import re

st.set_page_config(page_title="Visualizador de Albaranes FRIKING", layout="wide")
st.title("📦 Visualizador de Albaranes FRIKING")

uploaded_file = st.file_uploader("🔼 Sube un albarán PDF generado por PowerShop", type="pdf")

def extraer_articulos(texto):
    lineas = texto.split("\n")
    articulos = []
    i = 0
    while i < len(lineas):
        if lineas[i].startswith("H.CTAM."):
            codigo1 = lineas[i].strip()
            codigo2 = lineas[i+1].strip()
            codigo = f"{codigo1}{codigo2}"
            nombre = lineas[i+2].strip()
            tallas = ["S", "M", "L", "XL", "2XL", "3XL"]
            cantidades = []
            j = i + 3
            while len(cantidades) < 6 and j < len(lineas):
                if re.match(r"^\d+$", lineas[j].strip()):
                    cantidades.append(int(lineas[j].strip()))
                    j += 1
                else:
                    break
            # Rellenar con ceros si faltan tallas
            cantidades += [0] * (6 - len(cantidades))
            color = lineas[j].strip() if j < len(lineas) else ""
            articulos.append({
                "codigo": codigo,
                "nombre": nombre,
                "color": color,
                "cantidades": dict(zip(tallas, cantidades))
            })
            i = j
        i += 1
    return articulos

if uploaded_file:
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    raw_text = ""
    for page in doc:
        raw_text += page.get_text()

    articulos = extraer_articulos(raw_text)

    if articulos:
        filtro = st.text_input("🔍 Filtra por código o nombre del producto")

        for articulo in articulos:
            if filtro.lower() not in articulo["codigo"].lower() and filtro.lower() not in articulo["nombre"].lower():
                continue
            with st.expander(f"{articulo['codigo']} - {articulo['nombre']}", expanded=True):
                st.markdown(f"**🎨 Color:** {articulo['color']}")
                st.markdown("**📏 Cantidades por talla:**")
                st.table(pd.DataFrame([articulo["cantidades"]]))
    else:
        st.warning("No se encontraron artículos en el PDF. Asegúrate de que el formato es correcto.")
else:
    st.info("Por favor, sube un archivo PDF para comenzar.")

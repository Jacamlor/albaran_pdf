
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
            try:
                codigo1 = lineas[i].strip()
                codigo2 = lineas[i+1].strip()
                codigo = f"{codigo1}{codigo2}"
                nombre = lineas[i+2].strip()

                # Ir avanzando para buscar cantidades por talla
                j = i + 3
                cantidades = []
                while j < len(lineas) and len(cantidades) < 6:
                    linea = lineas[j].strip()
                    if re.match(r"^\d+$", linea):
                        cantidades.append(int(linea))
                        j += 1
                    else:
                        break
                # Rellenar si faltan tallas
                cantidades += [0] * (6 - len(cantidades))

                # Buscar la siguiente línea no numérica como color
                while j < len(lineas) and re.match(r"^[\d,.]+$", lineas[j].strip()):
                    j += 1
                color = lineas[j].strip() if j < len(lineas) else ""

                articulos.append({
                    "codigo": codigo,
                    "nombre": nombre,
                    "color": color,
                    "cantidades": dict(zip(["S", "M", "L", "XL", "2XL", "3XL"], cantidades))
                })
                i = j
            except Exception as e:
                print(f"Error procesando línea {i}: {e}")
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

        total_por_talla = {"S": 0, "M": 0, "L": 0, "XL": 0, "2XL": 0, "3XL": 0}
        total_por_color = {}

        for articulo in articulos:
            for talla, cantidad in articulo["cantidades"].items():
                total_por_talla[talla] += cantidad
            if articulo["color"] not in total_por_color:
                total_por_color[articulo["color"]] = sum(articulo["cantidades"].values())
            else:
                total_por_color[articulo["color"]] += sum(articulo["cantidades"].values())

            if filtro.lower() not in articulo["codigo"].lower() and filtro.lower() not in articulo["nombre"].lower():
                continue
            with st.expander(f"{articulo['codigo']} - {articulo['nombre']}", expanded=True):
                st.markdown(f"**🎨 Color:** {articulo['color']}")
                st.markdown("**📏 Cantidades por talla:**")
                st.table(pd.DataFrame([articulo["cantidades"]]))

        st.markdown("## 📊 Resumen final")
        st.markdown("### 📏 Total por talla:")
        st.table(pd.DataFrame([total_por_talla]))

        st.markdown("### 🎨 Total por color:")
        st.table(pd.DataFrame(list(total_por_color.items()), columns=["Color", "Total unidades"]))
    else:
        st.warning("No se encontraron artículos en el PDF. Asegúrate de que el formato es correcto.")
else:
    st.info("Por favor, sube un archivo PDF para comenzar.")

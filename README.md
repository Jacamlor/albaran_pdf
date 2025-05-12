# Visualizador de Albaranes FRIKING

Esta aplicación desarrollada en Streamlit permite subir archivos PDF de albaranes generados desde el ERP PowerShop y visualizar los datos de cada artículo (código, nombre, color y cantidades por talla) en un formato estructurado y filtrable.

## 📦 Funcionalidades

- Subida de PDFs de albaranes.
- Extracción automática de:
  - Código de artículo
  - Descripción del producto
  - Color
  - Cantidades por talla (S, M, L, XL, 2XL, 3XL)
- Filtro por nombre o código del producto.

## ▶️ Cómo usar

1. Sube el archivo PDF desde la interfaz.
2. Visualiza y filtra los productos extraídos.

## 🚀 Despliegue en Streamlit Cloud

1. Sube los archivos `app.py` y `requirements.txt` a un repositorio de GitHub.
2. Ve a https://streamlit.io/cloud y crea una nueva app desde ese repositorio.
3. Selecciona `app.py` como archivo principal.


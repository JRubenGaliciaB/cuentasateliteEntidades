import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial del título
st.set_page_config(page_title="Cuesta Satélite de Cultura SHCP", layout="wide")
st.title("Cuesta Satélite de Cultura SHCP - Entidades Federativas")

# Carga del archivo CSV desde la misma ubicación del programa
csv_file = "conjunto_de_datos_cscm_csc_efacr_s2023_p.csv"
df = pd.read_csv(csv_file)

# Mostrar los encabezados del CSV
st.write("Encabezados del CSV:", data.columns.tolist())

# Seleccionar un descriptor
descriptores = data.iloc[:, 0].unique()
descriptor_seleccionado = st.selectbox("Selecciona un descriptor:", descriptores)

# Filtrar los datos por el descriptor seleccionado
data_filtrada = data[data.iloc[:, 0] == descriptor_seleccionado]

# Seleccionar un año
anios = data.columns[1:]  # Asumiendo que la primera columna es el descriptor
anio_seleccionado = st.selectbox("Selecciona un año:", anios)

# Filtrar los datos por el año seleccionado
data_anio = data_filtrada[['Descriptor', anio_seleccionado]]  # Cambia 'Descriptor' por el nombre real de la columna

# Graficar los datos
st.write(f"Datos para el descriptor '{descriptor_seleccionado}' en el año '{anio_seleccionado}':")
fig, ax = plt.subplots()
ax.bar(data_anio['Descriptor'], data_anio[anio_seleccionado], color='skyblue')
ax.set_xlabel('Descriptor')
ax.set_ylabel('Valor')
ax.set_title(f'Visualización de datos para {descriptor_seleccionado} en {anio_seleccionado}')
plt.xticks(rotation=45)
st.pyplot(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial del título
st.set_page_config(page_title="Cuesta Satélite de Cultura SHCP", layout="wide")
st.title("Cuenta Satélite de Cultura SHCP - Entidades Federativas")

# Carga del archivo CSV desde la misma ubicación del programa
csv_file = "conjunto_de_datos_cscm_csc_efacr_s2023_p.csv"
df = pd.read_csv(csv_file)

# Asumir que la primera fila tiene encabezados y se cargan correctamente
# Renombrar la primera columna a "Descriptor"
df = df.rename(columns={df.columns[0]: "Descriptor"})

# Opciones disponibles
descriptors = df["Descriptor"].dropna().unique()
years = list(df.columns[1:])  # Ignorar la columna Descriptor

# Selección de filtros en la barra lateral
st.sidebar.header("Configuración de visualización")
selected_descriptors = st.sidebar.multiselect("Selecciona uno o más descriptores", descriptors, default=descriptors[:1])
selected_years = st.sidebar.multiselect("Selecciona uno o más años", years, default=years)
graph_type = st.sidebar.selectbox("Selecciona el tipo de gráfica", ["Barras", "Series de tiempo"])

# Filtrar datos
filtered_data = df[df["Descriptor"].isin(selected_descriptors)]
filtered_data = filtered_data[["Descriptor"] + selected_years]

# Transformar datos para visualización
melted_data = filtered_data.melt(id_vars="Descriptor", var_name="Año", value_name="Valor")

# Visualización
st.subheader("Visualización de datos")
if graph_type == "Barras":
    fig = px.bar(
        melted_data,
        x="Año",
        y="Valor",
        color="Descriptor",
        barmode="group",
        title="Comparativa de datos",
        hover_data={"Valor": True, "Año": True, "Descriptor": True},
    )
else:
    fig = px.line(
        melted_data,
        x="Año",
        y="Valor",
        color="Descriptor",
        title="Evolución de datos",
        markers=True,
        hover_data={"Valor": True, "Año": True, "Descriptor": True},
    )

# Configuración del diseño de la gráfica
fig.update_layout(
    xaxis_title="Año",
    yaxis_title="Valor",
    legend_title="Descriptor",
    template="plotly_white",
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.3,  # Mover la leyenda debajo de la gráfica
        xanchor="center",
        x=0.5
    )
)

# Mostrar la gráfica en Streamlit
st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial del título
st.set_page_config(page_title="Cuesta Satélite de Cultura SHCP", layout="wide")
st.title("Cuenta Satélite de Cultura SHCP")

# Carga del archivo CSV desde la misma ubicación del programa
csv_file = "conjunto_de_datos_cscm_csc_efacr_s2023_p.csv"
df = pd.read_csv(csv_file)

# Renombrar la primera columna a "Descriptor"
df = df.rename(columns={df.columns[0]: "Descriptor"})

# Opciones disponibles
descriptors = df["Descriptor"].dropna().unique()
years = list(df.columns[1:])  # Ignorar la columna Descriptor

# Inicializar el estado de sesión para los filtros
if 'selected_descriptors' not in st.session_state:
    st.session_state.selected_descriptors = descriptors[:1]
if 'selected_years' not in st.session_state:
    st.session_state.selected_years = years

# Selección de filtros en la barra lateral
st.sidebar.header("Configuración de visualización")
selected_descriptors = st.sidebar.multiselect("Selecciona uno o más descriptores", descriptors, default=st.session_state.selected_descriptors)
selected_years = st.sidebar.multiselect("Selecciona uno o más años", years, default=st.session_state.selected_years)
graph_type = st.sidebar.selectbox("Selecciona el tipo de gráfica", ["Barras", "Series de tiempo"])

# Botón para limpiar filtros
if st.sidebar.button("Limpiar Filtros"):
    st.session_state.selected_descriptors = descriptors[:1]
    st.session_state.selected_years = years
    selected_descriptors = st.session_state.selected_descriptors
    selected_years = st.session_state.selected_years

# Botón para agrupar por años y subsectores
if st.sidebar.button("Agrupar por Años y Subsectores"):
    # Aquí puedes implementar la lógica para agrupar los datos
    # Por ejemplo, podrías crear un nuevo DataFrame agrupado
    grouped_data = df.groupby(['Descriptor'] + selected_years).sum().reset_index()
    st.write("Datos agrupados:", grouped_data)

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

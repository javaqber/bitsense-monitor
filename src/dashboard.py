import streamlit as st
import pandas as pd
import time
from config import DATABASE_URL
from sqlalchemy import create_engine

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="Crypto Monitor",
    page_icon="💸",
    layout="wide"
)

# --- [NIVEL 3] INYECCIÓN DE CSS PERSONALIZADO ---
# Así es como cambias estilos específicos si sabes CSS
st.markdown("""
    <style>
    .big-font {
        font-size:50px !important;
        color: #F63366;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONEXIÓN DB ---


@st.cache_resource
def get_database_connection():
    return create_engine(DATABASE_URL)


engine = get_database_connection()

# --- [NIVEL 1] SIDEBAR (Barra Lateral) ---
# Todo lo que pongas bajo 'st.sidebar' irá a la izquierda
st.sidebar.image(
    "https://cryptologos.cc/logos/bitcoin-btc-logo.png", width=100)
st.sidebar.title("Configuración")
st.sidebar.markdown("Panel de control del ETL")
filtro_cantidad = st.sidebar.slider(
    "Datos a mostrar", 10, 500, 100)  # Slider interactivo
if st.sidebar.button("Refrescar manualmente"):
    st.cache_data.clear()

# --- CUERPO PRINCIPAL ---
# Usamos la clase CSS que definimos arriba
st.markdown('<p class="big-font">🪙 Bitcoin Real-Time Monitor</p>',
            unsafe_allow_html=True)

placeholder = st.empty()

while True:
    with placeholder.container():
        # Usamos el valor del slider (filtro_cantidad) en la query
        query = f"SELECT * FROM opiniones ORDER BY id DESC LIMIT {filtro_cantidad}"
        df = pd.read_sql(query, engine)

        if not df.empty:
            precio_actual = df.iloc[0]['texto_original'].split()[3]
            sentimiento_medio = df['sentimiento'].mean()

            # Métricas con colores nativos (delta)
            col1, col2, col3 = st.columns(3)
            col1.metric("Precio BTC", f"${precio_actual}", delta="En vivo")
            col2.metric("Sentimiento Promedio",
                        f"{sentimiento_medio:.4f}", delta_color="off")
            col3.metric("Registros Analizados", len(df))

            # Pestañas para organizar la vista
            tab1, tab2 = st.tabs(["📉 Gráfica", "📋 Datos Recientes"])

            with tab1:
                st.line_chart(df.set_index('fecha_creacion')['sentimiento'])

            with tab2:
                st.dataframe(df, use_container_width=True)

        time.sleep(10)  # Actualización en seg

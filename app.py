import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Configuración de la página con tema oscuro
st.set_page_config(
    page_title="Dashboard de Ventas 2023-2024",
    page_icon="📊", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema oscuro con colores violetas/morados
st.markdown("""
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* TODO EL TEXTO EN BLANCO */
    .stApp, .stApp p, .stApp div, .stApp span, .stApp h1, .stApp h2, .stApp h3, .stApp label {
        color: white !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1cypcdb, section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2d1b69 0%, #1a1a2e 100%) !important;
    }
    
    /* Texto del sidebar en blanco */
    .css-1d391kg *, section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* ETIQUETAS DEL MULTISELECT - MORADO OSCURO */
    .stMultiSelect span[data-baseweb="tag"] {
        background-color: #4c1d95 !important;
        color: white !important;
        border: 1px solid #6d28d9 !important;
    }
    
    /* Botón X de las etiquetas */
    .stMultiSelect span[data-baseweb="tag"] svg {
        fill: white !important;
    }
    
    /* Métricas personalizadas */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #6a4c93 0%, #9b59b6 100%) !important;
        border: 1px solid #8e44ad !important;
        padding: 1rem !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px rgba(142, 68, 173, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    /* Todo el texto de las métricas en blanco */
    div[data-testid="metric-container"] * {
        color: white !important;
    }
    
    /* Títulos */
    .main-header {
        background: linear-gradient(90deg, #8b5cf6, #a855f7, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    .section-header {
        color: white !importan;
        font-size: 1.5rem !important;
        font-weight: bold !important;
        margin: 1rem 0 !important;
        border-bottom: 2px solid #8b5cf6 !important;
        padding-bottom: 0.5rem !important;
    }
    
    /* Multiselect container */
    .stMultiSelect > div > div {
        background-color: #2d1b69 !important;
        border: 1px solid #8e44ad !important;
        color: white !important;
    }
    
    /* Dropdown del multiselect */
    .stMultiSelect ul {
        background-color: #2d1b69 !important;
        border: 1px solid #8e44ad !important;
    }
    
    .stMultiSelect li {
        color: white !important;
        background-color: #2d1b69 !important;
    }
    
    .stMultiSelect li:hover {
        background-color: #6d28d9 !important;
    }
    
    /* Sidebar filters */
    .sidebar-filter {
        background: rgba(139, 92, 246, 0.1) !important;
        padding: 1rem !important;
        border-radius: 10px !important;
        margin-bottom: 1rem !important;
        border: 1px solid #8b5cf6 !important;
    }
    
    /* Labels del sidebar */
    .css-1d391kg label, section[data-testid="stSidebar"] label {
        color: white !important;
        font-weight: 500 !important;
    }
    
    /* Placeholder text */
    .stMultiSelect input::placeholder {
        color: #c084fc !important;
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a2e;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #6d28d9, #8b5cf6);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #8b5cf6, #a855f7);
    }
</style>
""", unsafe_allow_html=True)

# Creamos datos sintéticos realistas (tu código existente)
np.random.seed(42)
fechas = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
n_productos = ['Laptop','Mouse','Teclado','Monitor','Auriculares']
regiones = ['Norte', 'Sur', 'Este', 'Oeste', 'Centro']

# Generamos el dataset
data = []
for fecha in fechas:
    for _ in range(np.random.poisson(10)):
        data.append({
            'fecha': fecha,
            'producto': np.random.choice(n_productos),
            'region': np.random.choice(regiones),
            'cantidad': np.random.randint(1, 6),
            'precio_unitario': np.random.uniform(50, 1500),
            'vendedor': f'Vendedor_{np.random.randint(1, 21)}',
        })

df = pd.DataFrame(data)
df['venta_total'] = df['cantidad'] * df['precio_unitario']

# Paleta de colores violeta/morado/fucsia
COLOR_PALETTE = [
    '#8b5cf6', '#a855f7', '#c084fc', '#e879f9', '#f0abfc',
    '#6d28d9', '#7c3aed', '#8b5cf6', '#a78bfa', '#c4b5fd'
]

# Tema oscuro para plotly
PLOTLY_THEME = {
    'layout': {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'white'},
        'title': {'font': {'color': 'white'}}, # título principal de cada gráfico
        'colorway': COLOR_PALETTE,
        'xaxis': {
            'gridcolor': 'rgba(139, 92, 246, 0.3)',
            'zerolinecolor': 'rgba(139, 92, 246, 0.5)',
            'automargin': True 
        },
        'yaxis': {
            'gridcolor': 'rgba(139, 92, 246, 0.3)',
            'zerolinecolor': 'rgba(139, 92, 246, 0.5)',
            'automargin': True 
        }
    }
}

# Título principal con estilo
st.markdown('<h1 class="main-header">📊 Dashboard de Análisis de Ventas 2023-2024</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar para los filtros con estilo
st.sidebar.markdown('<div class="sidebar-filter">', unsafe_allow_html=True)
st.sidebar.markdown("### 🎯 Filtros de Análisis")

productos_seleccionados = st.sidebar.multiselect(
    "Selecciona Productos:",
    options=df['producto'].unique(),
    default=df['producto'].unique()
)

regiones_seleccionadas = st.sidebar.multiselect(
    "Selecciona Regiones:",
    options=df['region'].unique(),
    default=df['region'].unique()
)
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# Filtrar datos
df_filtered = df[
    (df['producto'].isin(productos_seleccionados)) &
    (df['region'].isin(regiones_seleccionadas))
]

# Métricas principales con mejor diseño
st.markdown('<div class="section-header">📈 Métricas Principales</div>', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Ventas Totales", 
        f"${df_filtered['venta_total'].sum():,.0f}",
        delta=f"+{(df_filtered['venta_total'].sum()/1000000):.1f}M"
    )

with col2:
    st.metric(
        "📊 Promedio por Venta", 
        f"${df_filtered['venta_total'].mean():.0f}",
        delta=f"+{((df_filtered['venta_total'].mean()/2000)-1)*100:.1f}%"
    )

with col3:
    st.metric(
        "🔢 Número de Ventas", 
        f"{len(df_filtered):,}",
        delta=f"+{len(df_filtered)//100}"
    )

with col4:
    crecimiento = ((df_filtered[df_filtered['fecha'] >= '2024-01-01']['venta_total'].sum() /
                    df_filtered[df_filtered['fecha'] < '2024-01-01']['venta_total'].sum()) - 1) * 100
    st.metric(
        "📈 Crecimiento 2024", 
        f"{crecimiento:.1f}%",
        delta=f"{crecimiento:.1f}%"
    )

st.markdown("<br>", unsafe_allow_html=True)

# Creación de gráficos con tema personalizado

# 1. Ventas por mes
df_monthly = df_filtered.groupby([df_filtered['fecha'].dt.to_period('M')]).agg({'venta_total': 'sum'}).reset_index()
df_monthly['fecha'] = df_monthly['fecha'].astype(str)

fig_monthly = px.line(
    df_monthly, x='fecha', y='venta_total', 
    title='📈 Tendencia de Ventas Mensuales',
    labels={'venta_total': 'Ventas ($)', 'fecha': 'Mes'}
)
fig_monthly.update_traces(
    line=dict(width=4, color='#8b5cf6'),
    fill='tonexty',
    fillcolor='rgba(139, 92, 246, 0.2)'
)
fig_monthly.update_layout(PLOTLY_THEME['layout'])

# 2. Top productos
df_productos = df_filtered.groupby('producto')['venta_total'].sum().sort_values(ascending=True)
fig_productos = px.bar(
    x=df_productos.values, 
    y=df_productos.index, 
    orientation='h', 
    title='🛍️ Ventas por Producto',
    labels={'x': 'Ventas Totales ($)', 'y': 'Producto'},
    color=df_productos.values,
    color_continuous_scale='Viridis'
)
fig_productos.update_layout(PLOTLY_THEME['layout'])
fig_productos.update_traces(marker_color=COLOR_PALETTE)

# 3. Análisis geográfico
df_regiones = df_filtered.groupby('region')['venta_total'].sum().reset_index()
fig_regiones = px.pie(
    df_regiones, 
    values='venta_total', 
    names='region',
    title='🌍 Distribución de Ventas por Región',
    color_discrete_sequence=COLOR_PALETTE
)
fig_regiones.update_layout(PLOTLY_THEME['layout'])

# 4. Correlaciones
df_corr = df_filtered[['cantidad','precio_unitario','venta_total']].corr()
fig_heatmap = px.imshow(
    df_corr, 
    text_auto=True, 
    aspect="auto",
    title='🔥 Correlaciones entre Variables',
    color_continuous_scale='Viridis'
)
fig_heatmap.update_layout(PLOTLY_THEME['layout'])

# 5. Distribución de ventas
fig_dist = px.histogram(
    df_filtered, 
    x='venta_total', 
    nbins=50,
    title='📊 Distribución de Ventas Totales',
    color_discrete_sequence=['#8b5cf6']
)
fig_dist.update_layout(PLOTLY_THEME['layout'])

# Layout con gráficos
st.markdown('<div class="section-header">📊 Análisis Visual</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_monthly, use_container_width=True)
    st.plotly_chart(fig_productos, use_container_width=True)

with col2:
    st.plotly_chart(fig_regiones, use_container_width=True)
    st.plotly_chart(fig_heatmap, use_container_width=True)

# Gráfico completo en la parte inferior
st.plotly_chart(fig_dist, use_container_width=True)

# Footer personalizado
st.markdown("""
<div style='text-align: center; padding: 2rem; color: #c084fc; border-top: 1px solid #8b5cf6; margin-top: 2rem;'>
    <p>✨ Dashboard creado con Streamlit & Plotly | por Helena De La Cruz Vergara </p>
</div>
""", unsafe_allow_html=True)
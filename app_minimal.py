"""
CEAPSI Analytics - Interfaz Minimalista
Enfocada en datos y visualizaciones
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import os
from datetime import datetime
import numpy as np

# Configuración minimalista
st.set_page_config(
    page_title="CEAPSI Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Minimalista
st.markdown("""
<style>
    /* Fondo más limpio */
    .stApp {
        background-color: #fafafa;
    }
    
    /* Headers más sutiles */
    h1, h2, h3 {
        font-weight: 300;
        color: #2c3e50;
    }
    
    /* Métricas con estilo plano */
    [data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e0e0e0;
        padding: 15px;
        border-radius: 5px;
        box-shadow: none;
    }
    
    /* Navegación horizontal */
    .nav-container {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        border-bottom: 1px solid #e0e0e0;
        padding-bottom: 10px;
    }
    
    .nav-item {
        padding: 8px 16px;
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 20px;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .nav-item:hover {
        background: #f0f0f0;
        transform: translateY(-2px);
    }
    
    .nav-item.active {
        background: #2c3e50;
        color: white;
        border-color: #2c3e50;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Inicializar estado mínimo necesario"""
    if 'vista_actual' not in st.session_state:
        st.session_state.vista_actual = 'resumen'
    if 'datos_cargados' not in st.session_state:
        st.session_state.datos_cargados = False
    if 'df_datos' not in st.session_state:
        st.session_state.df_datos = None
    if 'metricas' not in st.session_state:
        st.session_state.metricas = {}

def cargar_datos():
    """Carga de datos simplificada"""
    archivo = st.file_uploader("", type=['csv', 'xlsx'], label_visibility="collapsed")
    
    if archivo:
        try:
            if archivo.name.endswith('.csv'):
                df = pd.read_csv(archivo, sep=';')
            else:
                df = pd.read_excel(archivo)
            
            # Procesamiento básico
            df['FECHA'] = pd.to_datetime(df['FECHA'], dayfirst=True)
            df = df[df['FECHA'] <= pd.Timestamp.now()]
            
            st.session_state.df_datos = df
            st.session_state.datos_cargados = True
            calcular_metricas(df)
            
            return True
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return False
    return False

def calcular_metricas(df):
    """Calcular métricas clave"""
    st.session_state.metricas = {
        'total_llamadas': len(df),
        'llamadas_atendidas': len(df[df['ATENDIDA'] == 'SI']),
        'tasa_atencion': len(df[df['ATENDIDA'] == 'SI']) / len(df) * 100,
        'promedio_diario': df.groupby(df['FECHA'].dt.date).size().mean(),
        'pico_horario': df.groupby(df['FECHA'].dt.hour).size().idxmax()
    }

def navegacion_horizontal():
    """Navegación horizontal minimalista"""
    vistas = ['resumen', 'temporal', 'patrones', 'predicciones']
    
    cols = st.columns(len(vistas))
    for i, vista in enumerate(vistas):
        with cols[i]:
            if st.button(
                vista.capitalize(), 
                key=f"nav_{vista}",
                use_container_width=True,
                type="primary" if st.session_state.vista_actual == vista else "secondary"
            ):
                st.session_state.vista_actual = vista
                st.rerun()

def mostrar_resumen():
    """Vista de resumen con métricas clave"""
    if not st.session_state.datos_cargados:
        st.info("Carga un archivo para comenzar")
        return
    
    # Métricas principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Llamadas", 
            f"{st.session_state.metricas['total_llamadas']:,}"
        )
    
    with col2:
        st.metric(
            "Tasa Atención", 
            f"{st.session_state.metricas['tasa_atencion']:.1f}%"
        )
    
    with col3:
        st.metric(
            "Promedio Diario", 
            f"{st.session_state.metricas['promedio_diario']:.0f}"
        )
    
    with col4:
        st.metric(
            "Hora Pico", 
            f"{st.session_state.metricas['pico_horario']}:00"
        )
    
    # Gráfico de tendencia simple
    st.markdown("### Tendencia de Llamadas")
    df_daily = st.session_state.df_datos.groupby(
        st.session_state.df_datos['FECHA'].dt.date
    ).size().reset_index(name='llamadas')
    
    fig = px.line(
        df_daily, 
        x='FECHA', 
        y='llamadas',
        line_shape='spline'
    )
    
    fig.update_layout(
        showlegend=False,
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_title="",
        yaxis_title="Llamadas",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxis(showgrid=False)
    fig.update_yaxis(showgrid=True, gridcolor='#f0f0f0')
    
    st.plotly_chart(fig, use_container_width=True)

def mostrar_analisis_temporal():
    """Análisis temporal simplificado"""
    if not st.session_state.datos_cargados:
        st.info("Carga un archivo para ver análisis temporal")
        return
    
    df = st.session_state.df_datos
    
    # Selector de granularidad
    granularidad = st.radio(
        "Granularidad",
        ["Diario", "Semanal", "Mensual"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    # Preparar datos según granularidad
    if granularidad == "Diario":
        df_grouped = df.groupby(df['FECHA'].dt.date).size()
    elif granularidad == "Semanal":
        df_grouped = df.groupby(df['FECHA'].dt.to_period('W')).size()
    else:
        df_grouped = df.groupby(df['FECHA'].dt.to_period('M')).size()
    
    # Visualización
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_grouped.index.astype(str),
        y=df_grouped.values,
        mode='lines+markers',
        line=dict(color='#2c3e50', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        xaxis_title="",
        yaxis_title="Llamadas",
        plot_bgcolor='white',
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Estadísticas rápidas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Máximo", f"{df_grouped.max():,}")
    with col2:
        st.metric("Promedio", f"{df_grouped.mean():.0f}")
    with col3:
        st.metric("Mínimo", f"{df_grouped.min():,}")

def mostrar_patrones():
    """Análisis de patrones simplificado"""
    if not st.session_state.datos_cargados:
        st.info("Carga un archivo para ver patrones")
        return
    
    df = st.session_state.df_datos
    
    # Patrón por hora
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Distribución Horaria")
        df_hora = df.groupby(df['FECHA'].dt.hour).size()
        
        fig = go.Figure(data=[
            go.Bar(
                x=df_hora.index,
                y=df_hora.values,
                marker_color='#2c3e50'
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="Hora",
            yaxis_title="Llamadas",
            showlegend=False,
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Distribución Semanal")
        dias = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
        df_dia = df.groupby(df['FECHA'].dt.dayofweek).size()
        
        fig = go.Figure(data=[
            go.Bar(
                x=dias,
                y=df_dia.reindex(range(7), fill_value=0).values,
                marker_color='#34495e'
            )
        ])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="",
            yaxis_title="Llamadas",
            showlegend=False,
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def mostrar_predicciones():
    """Vista de predicciones simplificada"""
    st.info("Módulo de predicciones en desarrollo")
    
    # Placeholder para predicciones
    if st.session_state.datos_cargados:
        st.markdown("#### Proyección próximos 7 días")
        
        # Simulación simple
        df = st.session_state.df_datos
        promedio = df.groupby(df['FECHA'].dt.date).size().mean()
        
        fechas_futuras = pd.date_range(
            start=df['FECHA'].max() + pd.Timedelta(days=1),
            periods=7,
            freq='D'
        )
        
        predicciones = [
            promedio * (1 + np.random.uniform(-0.1, 0.1))
            for _ in range(7)
        ]
        
        fig = go.Figure()
        
        # Histórico reciente
        df_recent = df[df['FECHA'] >= df['FECHA'].max() - pd.Timedelta(days=30)]
        df_daily = df_recent.groupby(df_recent['FECHA'].dt.date).size()
        
        fig.add_trace(go.Scatter(
            x=df_daily.index,
            y=df_daily.values,
            mode='lines',
            name='Histórico',
            line=dict(color='#7f8c8d')
        ))
        
        # Predicciones
        fig.add_trace(go.Scatter(
            x=fechas_futuras.date,
            y=predicciones,
            mode='lines+markers',
            name='Predicción',
            line=dict(color='#e74c3c', dash='dash')
        ))
        
        fig.update_layout(
            height=400,
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis_title="",
            yaxis_title="Llamadas",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    """Función principal"""
    init_session_state()
    
    # Header minimalista
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# CEAPSI Analytics")
    with col2:
        cargar_datos()
    
    # Navegación
    navegacion_horizontal()
    
    # Mostrar vista actual
    if st.session_state.vista_actual == 'resumen':
        mostrar_resumen()
    elif st.session_state.vista_actual == 'temporal':
        mostrar_analisis_temporal()
    elif st.session_state.vista_actual == 'patrones':
        mostrar_patrones()
    elif st.session_state.vista_actual == 'predicciones':
        mostrar_predicciones()

if __name__ == "__main__":
    main()
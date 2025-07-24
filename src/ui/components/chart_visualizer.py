"""
Visualizador de Gráficos con Logging Estratégico
Maneja la creación y visualización de gráficos
"""
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from datetime import datetime

# Configurar logger
logger = logging.getLogger('CEAPSI.ChartVisualizer')

class ChartVisualizer:
    """Maneja la visualización de gráficos del dashboard"""
    
    def __init__(self, data_validator=None):
        self.data_validator = data_validator
        logger.info("ChartVisualizer inicializado")
        
        # Colores para modelos
        self.colores = {
            'yhat_prophet': '#1f77b4',
            'yhat_arima': '#ff7f0e', 
            'yhat_random_forest': '#2ca02c',
            'yhat_gradient_boosting': '#d62728',
            'yhat_ensemble': '#9467bd',
            'yhat_lower': 'rgba(148, 103, 189, 0.2)',
            'yhat_upper': 'rgba(148, 103, 189, 0.2)'
        }
    
    def mostrar_grafico_predicciones_detallado(self, df_predicciones, df_historico=None):
        """
        Muestra gráfico detallado con predicciones y datos históricos con logging
        """
        logger.info("📊 CREANDO GRÁFICO DE PREDICCIONES DETALLADO")
        
        # Validar datos de entrada
        if df_predicciones is None or len(df_predicciones) == 0:
            logger.warning("❌ No hay predicciones para mostrar")
            st.warning("No hay predicciones disponibles para mostrar")
            return
        
        logger.info(f"   - Predicciones: {len(df_predicciones)} puntos")
        logger.info(f"   - Rango predicciones: {df_predicciones['ds'].min()} → {df_predicciones['ds'].max()}")
        
        # Crear figura con subplots
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.7, 0.3],
            shared_xaxes=True,
            vertical_spacing=0.1,
            subplot_titles=('Predicciones vs Histórico', 'Intervalos de Confianza')
        )
        
        # Agregar datos históricos si están disponibles
        if df_historico is not None and len(df_historico) > 0:
            logger.info(f"📈 PROCESANDO DATOS HISTÓRICOS:")
            logger.info(f"   - Total registros históricos: {len(df_historico)}")
            
            # Validar y limpiar datos históricos
            df_hist_filtrado, alertas = self.data_validator.validar_integridad_cientifica_datos(
                df_historico, 
                "Datos Históricos"
            )
            
            # Mostrar alertas de validación
            for alerta in alertas:
                if "✅" in alerta:
                    st.success(alerta)
                elif "🚨" in alerta or "❌" in alerta:
                    st.error(alerta)
                elif "⚠️" in alerta:
                    st.warning(alerta)
                else:
                    st.info(alerta)
            
            # OPTIMIZACIÓN CRÍTICA: Reducir datos históricos solo si es EXTREMADAMENTE grande
            if len(df_hist_filtrado) > 50000:
                logger.warning(f"⚠️ Optimizando visualización: {len(df_hist_filtrado)} → 10000 puntos")
                st.info(f"⚡ Optimizando visualización: {len(df_hist_filtrado)} → 10000 puntos históricos")
                df_hist_optimized = self.data_validator.optimizar_datos_para_plot(
                    df_hist_filtrado, 
                    max_puntos=10000, 
                    nombre_dataset="Histórico"
                )
            else:
                df_hist_optimized = df_hist_filtrado
                logger.info(f"   - No requiere optimización: {len(df_hist_optimized)} puntos")
            
            if len(df_hist_optimized) > 0:
                # LOG: Información del gráfico histórico
                logger.info(f"📊 GRAFICANDO HISTÓRICO:")
                logger.info(f"   - Puntos a graficar: {len(df_hist_optimized)}")
                logger.info(f"   - Rango: {df_hist_optimized['ds'].min()} → {df_hist_optimized['ds'].max()}")
                
                fig.add_trace(
                    go.Scatter(
                        x=df_hist_optimized['ds'],
                        y=df_hist_optimized['y'],
                        mode='lines',
                        name='Histórico Real',
                        line=dict(color='black', width=2),
                        opacity=0.7,
                        hovertemplate='<b>Histórico</b><br>Fecha: %{x}<br>Llamadas: %{y}<extra></extra>'
                    ),
                    row=1, col=1
                )
                
                # Agregar línea vertical separadora
                fecha_corte = df_predicciones['ds'].min()
                fig.add_vline(
                    x=fecha_corte, 
                    line_dash="dash", 
                    line_color="gray",
                    annotation_text="Inicio Predicciones",
                    annotation_position="top left",
                    row=1, col=1
                )
                
                # Mostrar estadísticas de optimización
                if len(df_hist_filtrado) != len(df_hist_optimized):
                    with st.expander("📊 Detalles de Optimización"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Datos Originales", f"{len(df_hist_filtrado):,}")
                        with col2:
                            st.metric("Datos Mostrados", f"{len(df_hist_optimized):,}")
                        with col3:
                            reduccion = (1 - len(df_hist_optimized)/len(df_hist_filtrado)) * 100
                            st.metric("Reducción", f"{reduccion:.1f}%")
            else:
                logger.warning("⚠️ No hay datos históricos válidos para mostrar")
                st.warning("⚠️ No hay datos históricos válidos para mostrar en el gráfico")
        
        # LOG: Agregar predicciones
        logger.info(f"📊 GRAFICANDO PREDICCIONES:")
        
        # Agregar predicciones de cada modelo
        for col in df_predicciones.columns:
            if col.startswith('yhat_') and col in self.colores:
                modelo_name = col.replace('yhat_', '').replace('_', ' ').title()
                logger.info(f"   - Modelo {modelo_name}: {df_predicciones[col].mean():.1f} promedio")
                
                # Estilo especial para ensemble
                if col == 'yhat_ensemble':
                    line_style = dict(color=self.colores[col], width=3, dash='solid')
                    showlegend = True
                else:
                    line_style = dict(color=self.colores[col], width=2, dash='dot')
                    showlegend = True
                
                fig.add_trace(
                    go.Scatter(
                        x=df_predicciones['ds'],
                        y=df_predicciones[col],
                        mode='lines',
                        name=modelo_name,
                        line=line_style,
                        showlegend=showlegend,
                        hovertemplate=f'<b>{modelo_name}</b><br>Fecha: %{{x}}<br>Predicción: %{{y:.0f}}<extra></extra>'
                    ),
                    row=1, col=1
                )
        
        # Agregar intervalo de confianza si existe
        if 'yhat_lower' in df_predicciones.columns and 'yhat_upper' in df_predicciones.columns:
            # Banda de confianza
            fig.add_trace(
                go.Scatter(
                    x=df_predicciones['ds'].tolist() + df_predicciones['ds'].tolist()[::-1],
                    y=df_predicciones['yhat_upper'].tolist() + df_predicciones['yhat_lower'].tolist()[::-1],
                    fill='toself',
                    fillcolor='rgba(148, 103, 189, 0.1)',
                    line=dict(color='rgba(255,255,255,0)'),
                    name='Intervalo 95%',
                    showlegend=True,
                    hoverinfo='skip'
                ),
                row=1, col=1
            )
            
            # Subplot de intervalos
            fig.add_trace(
                go.Scatter(
                    x=df_predicciones['ds'],
                    y=df_predicciones['yhat_upper'] - df_predicciones['yhat_lower'],
                    mode='lines',
                    name='Amplitud IC',
                    line=dict(color='orange', width=2),
                    showlegend=False,
                    hovertemplate='<b>Amplitud IC</b><br>Fecha: %{x}<br>Amplitud: %{y:.0f}<extra></extra>'
                ),
                row=2, col=1
            )
        
        # Actualizar layout
        fig.update_xaxes(title_text="Fecha", row=2, col=1)
        fig.update_yaxes(title_text="Llamadas", row=1, col=1)
        fig.update_yaxes(title_text="Amplitud", row=2, col=1)
        
        fig.update_layout(
            height=700,
            hovermode='x unified',
            title={
                'text': "Análisis Detallado de Predicciones",
                'x': 0.5,
                'xanchor': 'center'
            },
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        logger.info("✅ Gráfico completado")
        st.plotly_chart(fig, use_container_width=True)
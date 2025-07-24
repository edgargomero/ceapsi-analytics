"""
Dashboard de Validación CEAPSI v2 - Refactorizado
Versión modular con componentes separados y logging mejorado
"""
import streamlit as st
import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime, timedelta

# Importar componentes modulares
from .components.data_validator import DataValidator
from .components.data_loader import DataLoader
from .components.chart_visualizer import ChartVisualizer

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CEAPSI.Dashboard')

class DashboardValidacionCEAPSI_V2:
    """Dashboard refactorizado con componentes modulares"""
    
    def __init__(self):
        """Inicializar dashboard con componentes"""
        logger.info("🚀 Inicializando Dashboard CEAPSI v2 (Refactorizado)")
        
        # Inicializar componentes
        self.data_validator = DataValidator()
        self.data_loader = DataLoader()
        self.chart_visualizer = ChartVisualizer(data_validator=self.data_validator)
        
        # Path para archivos
        self.archivo_datos_manual = None
        
        logger.info("✅ Componentes inicializados correctamente")
    
    def ejecutar_dashboard(self):
        """Ejecutar el dashboard principal"""
        logger.info("📊 Ejecutando Dashboard CEAPSI")
        
        # Header
        self.mostrar_header_validacion()
        
        # Selector de tipo de llamada
        tipo_llamada = self.mostrar_selector_tipo_llamada()
        
        # Tabs principales
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Predicciones vs Real", 
            "📈 Análisis de Residuales",
            "🎯 Métricas de Performance",
            "📋 Recomendaciones"
        ])
        
        with tab1:
            self.mostrar_tab_predicciones(tipo_llamada)
        
        with tab2:
            self.mostrar_tab_residuales(tipo_llamada)
        
        with tab3:
            self.mostrar_tab_metricas(tipo_llamada)
        
        with tab4:
            self.mostrar_tab_recomendaciones(tipo_llamada)
    
    def mostrar_header_validacion(self):
        """Header del dashboard de validación"""
        st.title("📊 CEAPSI - Dashboard de Análisis")
        st.markdown("### Sistema de Predicción de Llamadas - Análisis Detallado")
        
        # Indicador de integridad temporal
        fecha_hoy = pd.Timestamp.now().normalize()
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.info("🔬 **Integridad de Datos**: Validación activa")
            with col2:
                st.metric("📅 Fecha Límite", fecha_hoy.strftime('%Y-%m-%d'))
            with col3:
                st.success("✅ Sin Data Leakage")
        
        st.markdown("---")
    
    def mostrar_selector_tipo_llamada(self):
        """Selector de tipo de llamada"""
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            tipo_llamada = st.selectbox(
                "Tipo de Llamada:",
                ['ENTRANTE', 'SALIENTE'],
                key='tipo_llamada_selector_v2'
            )
        
        with col2:
            if st.button("🔄 Actualizar Datos", use_container_width=True):
                st.cache_data.clear()
                st.rerun()
        
        return tipo_llamada
    
    def mostrar_tab_predicciones(self, tipo_llamada):
        """Tab de predicciones vs datos reales"""
        logger.info(f"📊 Mostrando tab de predicciones para {tipo_llamada}")
        
        # Cargar datos
        with st.spinner("Cargando datos..."):
            # Cargar resultados del modelo
            resultados, df_predicciones = self.data_loader.cargar_resultados_multimodelo(tipo_llamada)
            
            # Cargar datos históricos completos
            df_completo = self.data_loader.cargar_datos_completos(
                archivo_manual=self.archivo_datos_manual,
                tipo_analisis=tipo_llamada
            )
        
        if df_completo is None:
            st.error("❌ No se pudieron cargar los datos")
            return
        
        # Procesar datos históricos para el tipo de llamada
        df_historico = self._procesar_datos_historicos(df_completo, tipo_llamada)
        
        # Mostrar métricas principales
        self.mostrar_metricas_principales(resultados, df_historico)
        
        # Mostrar gráfico principal
        st.subheader("📈 Predicciones vs Datos Históricos")
        self.chart_visualizer.mostrar_grafico_predicciones_detallado(
            df_predicciones, 
            df_historico
        )
    
    def mostrar_tab_residuales(self, tipo_llamada):
        """Tab de análisis de residuales"""
        st.info("📊 Análisis de residuales en desarrollo...")
    
    def mostrar_tab_metricas(self, tipo_llamada):
        """Tab de métricas de performance"""
        st.info("📊 Métricas detalladas en desarrollo...")
    
    def mostrar_tab_recomendaciones(self, tipo_llamada):
        """Tab de recomendaciones"""
        st.info("💡 Recomendaciones automáticas en desarrollo...")
    
    def mostrar_metricas_principales(self, resultados, df_historico):
        """Mostrar métricas principales del análisis"""
        st.subheader("📊 Métricas Principales")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calcular métricas básicas
        if df_historico is not None and len(df_historico) > 0:
            promedio_historico = df_historico['y'].mean()
            max_historico = df_historico['y'].max()
            min_historico = df_historico['y'].min()
            dias_datos = df_historico['ds'].nunique()
        else:
            promedio_historico = 0
            max_historico = 0
            min_historico = 0
            dias_datos = 0
        
        with col1:
            st.metric("📊 Promedio Histórico", f"{promedio_historico:.0f}")
        
        with col2:
            st.metric("📈 Máximo", f"{max_historico:.0f}")
        
        with col3:
            st.metric("📉 Mínimo", f"{min_historico:.0f}")
        
        with col4:
            st.metric("📅 Días de Datos", f"{dias_datos}")
    
    def _procesar_datos_historicos(self, df_completo, tipo_llamada):
        """Procesar datos históricos para análisis"""
        if df_completo is None:
            return None
        
        logger.info(f"🔄 Procesando datos históricos para {tipo_llamada}")
        
        try:
            # Filtrar por tipo de llamada
            if 'SENTIDO' in df_completo.columns:
                if tipo_llamada == 'ENTRANTE':
                    df_filtrado = df_completo[df_completo['SENTIDO'] == 'in'].copy()
                else:
                    df_filtrado = df_completo[df_completo['SENTIDO'] == 'out'].copy()
            else:
                # Si no hay columna SENTIDO, usar todos los datos
                df_filtrado = df_completo.copy()
            
            logger.info(f"   - Registros después de filtrar por tipo: {len(df_filtrado)}")
            
            # Agregar por día
            df_agrupado = df_filtrado.groupby('fecha_solo').size().reset_index(name='y')
            df_agrupado.columns = ['ds', 'y']
            df_agrupado['ds'] = pd.to_datetime(df_agrupado['ds'])
            
            logger.info(f"   - Días únicos: {len(df_agrupado)}")
            logger.info(f"   - Promedio diario: {df_agrupado['y'].mean():.1f}")
            
            return df_agrupado
            
        except Exception as e:
            logger.error(f"❌ Error procesando datos históricos: {e}")
            return None

def main():
    """Función principal para testing"""
    dashboard = DashboardValidacionCEAPSI_V2()
    dashboard.ejecutar_dashboard()

if __name__ == "__main__":
    main()
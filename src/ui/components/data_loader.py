"""
Cargador de Datos con Logging Estratégico
Maneja la carga de archivos CSV y resultados del pipeline
"""
import pandas as pd
import streamlit as st
import os
import json
import logging
from pathlib import Path
from datetime import datetime

# Configurar logger específico
logger = logging.getLogger('CEAPSI.DataLoader')

class DataLoader:
    """Maneja la carga de datos desde archivos y resultados"""
    
    def __init__(self):
        self.archivo_datos_manual = None
        logger.info("DataLoader inicializado")
    
    @st.cache_data(ttl=300)
    def cargar_datos_completos(_self, archivo_manual=None, tipo_analisis='TODOS'):
        """
        Carga datos completos con logging detallado
        """
        logger.info(f"🔄 INICIANDO CARGA DE DATOS - Tipo: {tipo_analisis}")
        
        try:
            # PRIORIDAD 1: Usar archivo manual si está disponible
            if archivo_manual and os.path.exists(archivo_manual):
                archivo_llamadas = archivo_manual
                logger.info(f"📁 Usando archivo manual: {archivo_llamadas}")
                logger.info(f"   Tamaño: {os.path.getsize(archivo_llamadas) / 1024 / 1024:.2f} MB")
            # PRIORIDAD 2: Buscar archivo de session state
            elif hasattr(st.session_state, 'archivo_datos') and st.session_state.archivo_datos:
                archivo_llamadas = st.session_state.archivo_datos
                logger.info(f"📁 Usando archivo de session_state: {archivo_llamadas}")
                if os.path.exists(archivo_llamadas):
                    logger.info(f"   Tamaño: {os.path.getsize(archivo_llamadas) / 1024 / 1024:.2f} MB")
            else:
                # Solo usar datos de ejemplo si realmente no hay archivo manual
                logger.warning("⚠️ No hay archivo de datos cargado")
                st.warning("📁 No hay archivo de datos cargado. Dashboard usará datos de ejemplo limitados...")
                st.info("💡 Sube un archivo de datos para análisis completo con tu información real.")
                return _self._crear_datos_ejemplo_completos()
            
            # Intentar diferentes encodings
            for encoding in ['utf-8', 'latin-1', 'cp1252']:
                try:
                    logger.info(f"   Intentando encoding: {encoding}")
                    df_completo = pd.read_csv(archivo_llamadas, sep=';', encoding=encoding)
                    logger.info(f"✅ Archivo cargado con encoding {encoding}")
                    break
                except UnicodeDecodeError:
                    continue
            else:
                logger.error("❌ No se pudo cargar el archivo con ningún encoding")
                st.error("No se pudo cargar el archivo con ningún encoding")
                return None
            
            # LOG: Información inicial del dataset
            logger.info(f"📊 DATASET CARGADO:")
            logger.info(f"   - Total registros: {len(df_completo):,}")
            logger.info(f"   - Columnas: {list(df_completo.columns)}")
            
            # Procesar fechas con validación estricta
            try:
                df_completo['FECHA'] = pd.to_datetime(df_completo['FECHA'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
            except:
                # Fallback para otros formatos
                df_completo['FECHA'] = pd.to_datetime(df_completo['FECHA'], dayfirst=True, errors='coerce')
            
            fechas_invalidas = df_completo['FECHA'].isna().sum()
            if fechas_invalidas > 0:
                logger.warning(f"⚠️ {fechas_invalidas} fechas inválidas encontradas")
            
            df_completo = df_completo.dropna(subset=['FECHA'])
            
            # LOG: Rango de fechas
            fecha_min = df_completo['FECHA'].min()
            fecha_max = df_completo['FECHA'].max()
            logger.info(f"📅 RANGO DE FECHAS:")
            logger.info(f"   - Desde: {fecha_min}")
            logger.info(f"   - Hasta: {fecha_max}")
            logger.info(f"   - Días totales: {(fecha_max - fecha_min).days}")
            
            # VALIDACIÓN CRÍTICA: Filtrar fechas futuras
            fecha_hoy = pd.Timestamp.now().normalize()
            fechas_futuras = df_completo[df_completo['FECHA'] > fecha_hoy]
            
            if len(fechas_futuras) > 0:
                logger.warning(f"🚨 FECHAS FUTURAS DETECTADAS: {len(fechas_futuras)} registros")
                logger.info(f"   Rango futuro: {fechas_futuras['FECHA'].min()} → {fechas_futuras['FECHA'].max()}")
                st.warning(f"⚠️ DATOS FUTUROS DETECTADOS: {len(fechas_futuras)} registros con fechas > {fecha_hoy.date()}")
                st.info("🔧 Filtrando automáticamente a datos históricos válidos")
                df_completo = df_completo[df_completo['FECHA'] <= fecha_hoy]
            
            # Agregar columnas derivadas
            df_completo['fecha_solo'] = df_completo['FECHA'].dt.date
            df_completo['hora'] = df_completo['FECHA'].dt.hour
            df_completo['dia_semana'] = df_completo['FECHA'].dt.day_name()
            df_completo['mes'] = df_completo['FECHA'].dt.month
            df_completo['ano'] = df_completo['FECHA'].dt.year
            
            # LOG: NO filtrar días laborales - mantener todos los datos
            logger.info("📊 MANTENIENDO TODOS LOS DÍAS (incluye fines de semana)")
            
            # LOG: Estadísticas finales
            logger.info(f"✅ DATOS FINALES:")
            logger.info(f"   - Total registros: {len(df_completo):,}")
            logger.info(f"   - Días únicos: {df_completo['fecha_solo'].nunique()}")
            
            if 'SENTIDO' in df_completo.columns:
                entrantes = len(df_completo[df_completo['SENTIDO'] == 'in'])
                salientes = len(df_completo[df_completo['SENTIDO'] == 'out'])
                logger.info(f"   - Llamadas entrantes: {entrantes:,}")
                logger.info(f"   - Llamadas salientes: {salientes:,}")
            
            # OPTIMIZACIÓN CRÍTICA: Para archivos muy grandes, dar aviso de optimizaciones
            if len(df_completo) > 50000:
                logger.warning(f"⚠️ Dataset grande: {len(df_completo):,} registros - se aplicarán optimizaciones")
                st.success(f"✅ Archivo grande cargado: {len(df_completo):,} registros")
                st.info("⚡ Las visualizaciones se optimizarán automáticamente para mejor rendimiento") 
                with st.expander("📊 Estrategias de Optimización Aplicadas"):
                    st.markdown("""
                    - **Gráficos Históricos**: Sampling inteligente a ~10000 puntos
                    - **Análisis de Patrones**: Muestra representativa estratificada  
                    - **Heatmaps**: Limitado a períodos recientes más relevantes
                    - **Hover Details**: Información completa mantenida
                    - **Cálculos**: Realizados sobre datos completos, visualización optimizada
                    """)
            
            return df_completo
            
        except Exception as e:
            logger.error(f"❌ Error cargando datos completos: {e}")
            st.error(f"Error cargando datos completos: {e}")
            return None
    
    @st.cache_data(ttl=300)
    def cargar_resultados_multimodelo(_self, tipo_llamada='ENTRANTE'):
        """Carga resultados del sistema multi-modelo con logging"""
        logger.info(f"🔄 Cargando resultados multi-modelo para {tipo_llamada}")
        
        try:
            # Buscar archivo más reciente en el directorio actual
            archivos = [f for f in os.listdir('.') 
                       if f.startswith(f'predicciones_multimodelo_{tipo_llamada.lower()}') and f.endswith('.json')]
            
            if not archivos:
                logger.warning(f"📁 No se encontraron resultados para {tipo_llamada}")
                st.info(f"📁 No se encontraron resultados para {tipo_llamada}. Creando predicciones de ejemplo...")
                return _self._crear_resultados_ejemplo(tipo_llamada)
            
            archivo_reciente = sorted(archivos)[-1]
            logger.info(f"📁 Usando archivo: {archivo_reciente}")
            
            with open(archivo_reciente, 'r', encoding='utf-8') as f:
                resultados = json.load(f)
            
            # Convertir predicciones a DataFrame
            df_pred = pd.DataFrame(resultados['predicciones'])
            df_pred['ds'] = pd.to_datetime(df_pred['ds'])
            
            logger.info(f"✅ Resultados cargados: {len(df_pred)} predicciones")
            
            return resultados, df_pred
            
        except Exception as e:
            logger.error(f"❌ Error cargando resultados: {e}")
            st.error(f"Error cargando resultados: {e}")
            return _self._crear_resultados_ejemplo(tipo_llamada)
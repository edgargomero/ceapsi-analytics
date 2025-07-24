"""
Validador de Datos con Logging Estratégico
Separa la lógica de validación y optimización de datos
"""
import pandas as pd
import streamlit as st
import numpy as np
import logging
from datetime import datetime

# Configurar logger específico para validación
logger = logging.getLogger('CEAPSI.DataValidator')

class DataValidator:
    """Maneja validación y optimización de datos para visualización"""
    
    def __init__(self):
        self.alertas = []
        logger.info("DataValidator inicializado")
    
    def validar_integridad_cientifica_datos(self, df, nombre_dataset="Dataset"):
        """
        Valida integridad científica de datos con logging detallado
        """
        if df is None or len(df) == 0:
            logger.warning(f"{nombre_dataset}: DataFrame vacío o None")
            return df, ["❌ No hay datos para validar"]
        
        # LOG: Estado inicial
        logger.info(f"🔍 VALIDANDO {nombre_dataset}: {len(df)} registros iniciales")
        logger.info(f"📅 Columnas disponibles: {list(df.columns)}")
        
        alertas = []
        df_limpio = df.copy()
        
        # Verificar columna de fechas
        if 'ds' not in df_limpio.columns:
            logger.error(f"{nombre_dataset}: No se encontró columna 'ds'")
            alertas.append(f"❌ {nombre_dataset}: No se encontró columna de fechas 'ds'")
            return df_limpio, alertas
        
        # LOG: Rango de fechas original
        fecha_min_original = df_limpio['ds'].min()
        fecha_max_original = df_limpio['ds'].max()
        logger.info(f"📅 Rango original: {fecha_min_original} → {fecha_max_original}")
        
        # Convertir fechas
        df_limpio['ds'] = pd.to_datetime(df_limpio['ds'], errors='coerce')
        
        # Eliminar fechas inválidas
        fechas_invalidas = df_limpio['ds'].isna().sum()
        if fechas_invalidas > 0:
            logger.warning(f"⚠️ {nombre_dataset}: {fechas_invalidas} fechas inválidas eliminadas")
            alertas.append(f"⚠️ {nombre_dataset}: {fechas_invalidas} fechas inválidas eliminadas")
            df_limpio = df_limpio.dropna(subset=['ds'])
        
        # VALIDACIÓN CRÍTICA: Filtrar fechas futuras
        fecha_hoy = pd.Timestamp.now().normalize()
        registros_futuros = df_limpio[df_limpio['ds'] > fecha_hoy]
        
        if len(registros_futuros) > 0:
            logger.warning(f"🚨 {nombre_dataset}: {len(registros_futuros)} registros con fechas futuras")
            logger.info(f"   Fechas futuras detectadas: {registros_futuros['ds'].min()} → {registros_futuros['ds'].max()}")
            alertas.append(f"🚨 {nombre_dataset}: {len(registros_futuros)} registros futuros eliminados (data leakage prevention)")
            df_limpio = df_limpio[df_limpio['ds'] <= fecha_hoy]
        else:
            logger.info(f"✅ {nombre_dataset}: Sin fechas futuras detectadas")
            alertas.append(f"✅ {nombre_dataset}: Todos los {len(df)} registros son históricamente válidos")
        
        # LOG: Rango de fechas después de limpieza
        if len(df_limpio) > 0:
            fecha_min_limpia = df_limpio['ds'].min()
            fecha_max_limpia = df_limpio['ds'].max()
            logger.info(f"📅 Rango limpio: {fecha_min_limpia} → {fecha_max_limpia}")
            logger.info(f"📊 Registros después de limpieza: {len(df_limpio)}")
        
        # Verificar ordenamiento temporal
        if not df_limpio['ds'].is_monotonic_increasing:
            logger.info(f"🔧 {nombre_dataset}: Reordenando datos cronológicamente")
            alertas.append(f"🔧 {nombre_dataset}: Datos reordenados cronológicamente")
            df_limpio = df_limpio.sort_values('ds').reset_index(drop=True)
        
        # Verificar gaps temporales
        if len(df_limpio) > 1:
            gaps = df_limpio['ds'].diff()
            gaps_grandes = gaps[gaps > pd.Timedelta(days=7)]
            if len(gaps_grandes) > 0:
                logger.warning(f"⚠️ {nombre_dataset}: {len(gaps_grandes)} gaps temporales > 7 días")
                alertas.append(f"⚠️ {nombre_dataset}: {len(gaps_grandes)} gaps temporales > 7 días detectados")
        
        return df_limpio, alertas
    
    def optimizar_datos_para_plot(self, df, max_puntos=10000, nombre_dataset="Dataset"):
        """
        Optimiza datasets grandes para visualización eficiente con logging
        """
        if df is None or len(df) == 0:
            logger.warning(f"{nombre_dataset}: No hay datos para optimizar")
            return df
            
        # Si el dataset es pequeño, no optimizar
        if len(df) <= max_puntos:
            logger.info(f"{nombre_dataset}: {len(df)} puntos - no requiere optimización")
            return df
            
        logger.info(f"📊 OPTIMIZANDO {nombre_dataset}: {len(df)} → {max_puntos} puntos")
        st.info(f"📊 {nombre_dataset}: Optimizando {len(df)} registros → {max_puntos} puntos para visualización")
        
        # ESTRATEGIA 1: Sampling inteligente preservando tendencias
        # Mantener los primeros y últimos puntos siempre (más generoso con datos)
        inicio_puntos = min(1000, len(df) // 4)
        fin_puntos = min(1000, len(df) // 4)
        medio_puntos = max_puntos - inicio_puntos - fin_puntos
        
        logger.info(f"   Estrategia: {inicio_puntos} inicio + {medio_puntos} medio + {fin_puntos} fin")
        
        # Dividir el rango medio y hacer sampling uniforme
        df_inicio = df.head(inicio_puntos)
        df_fin = df.tail(fin_puntos)
        
        if medio_puntos > 0 and len(df) > (inicio_puntos + fin_puntos):
            df_medio = df.iloc[inicio_puntos:-fin_puntos]
            if len(df_medio) > medio_puntos:
                # Sampling uniforme del medio
                indices = np.linspace(0, len(df_medio)-1, medio_puntos, dtype=int)
                df_medio_sampled = df_medio.iloc[indices]
            else:
                df_medio_sampled = df_medio
                
            # Combinar todos los segmentos
            df_optimized = pd.concat([df_inicio, df_medio_sampled, df_fin], ignore_index=True)
        else:
            df_optimized = pd.concat([df_inicio, df_fin], ignore_index=True)
        
        # Asegurar ordenamiento temporal si existe columna de fechas
        if 'ds' in df_optimized.columns:
            df_optimized = df_optimized.sort_values('ds').reset_index(drop=True)
        
        logger.info(f"✅ Optimización completada: {len(df_optimized)} puntos finales")
        
        return df_optimized
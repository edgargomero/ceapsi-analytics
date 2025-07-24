#!/usr/bin/env python3
"""
CEAPSI - Sistema de Autodetección de Campos en Archivos CSV/Excel
Detecta automáticamente columnas de fecha, teléfono, sentido, etc.
"""

import pandas as pd
import numpy as np
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import streamlit as st

class FieldAutoDetector:
    """Sistema inteligente de autodetección de campos en archivos de datos"""
    
    def __init__(self):
        self.field_patterns = {
            'FECHA': {
                'keywords': ['fecha', 'date', 'time', 'timestamp', 'hora', 'datetime', 'created', 'updated'],
                'patterns': [
                    r'\d{1,2}[-/]\d{1,2}[-/]\d{2,4}',  # DD-MM-YYYY o DD/MM/YYYY
                    r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',    # YYYY-MM-DD
                    r'\d{1,2}:\d{2}:\d{2}',            # HH:MM:SS
                ],
                'required': True,
                'priority': 1
            },
            'TELEFONO': {
                'keywords': ['telefono', 'phone', 'tel', 'numero', 'extension', 'ext', 'anexo', 'caller', 'number'],
                'patterns': [
                    r'^\+?[0-9]{7,15}$',               # Teléfonos internacionales
                    r'^[0-9]{7,10}$',                  # Teléfonos locales
                    r'^\d{3,4}$',                      # Extensiones
                ],
                'required': True,
                'priority': 2
            },
            'SENTIDO': {
                'keywords': ['sentido', 'direction', 'tipo', 'type', 'call_type', 'inbound', 'outbound'],
                'values': ['in', 'out', 'inbound', 'outbound', 'entrada', 'salida', 'entrante', 'saliente'],
                'required': True,
                'priority': 3
            },
            'ATENDIDA': {
                'keywords': ['atendida', 'answered', 'status', 'estado', 'result', 'outcome'],
                'values': ['si', 'no', 'yes', 'no', 'answered', 'missed', 'busy', 'failed'],
                'required': False,
                'priority': 4
            },
            'DURACION': {
                'keywords': ['duracion', 'duration', 'tiempo', 'length', 'call_time'],
                'patterns': [
                    r'^\d+:\d{2}:\d{2}$',              # HH:MM:SS
                    r'^\d+$',                          # Segundos
                ],
                'required': False,
                'priority': 5
            },
            'USUARIO': {
                'keywords': ['usuario', 'user', 'agent', 'agente', 'operator', 'name', 'nombre'],
                'required': False,
                'priority': 6
            },
            'CARGO': {
                'keywords': ['cargo', 'role', 'position', 'puesto', 'job', 'title'],
                'required': False,
                'priority': 7
            }
        }
    
    def detect_fields(self, df: pd.DataFrame) -> Dict[str, str]:
        """Detecta automáticamente los campos en el DataFrame"""
        
        if df is None or len(df) == 0:
            return {}
        
        st.info("🔍 Ejecutando autodetección inteligente de campos...")
        
        detected_mapping = {}
        confidence_scores = {}
        
        # Analizar cada columna del DataFrame
        for col in df.columns:
            best_field, confidence = self._analyze_column(df, col)
            if best_field and confidence > 0.3:  # Umbral mínimo de confianza
                detected_mapping[best_field] = col
                confidence_scores[best_field] = confidence
        
        # Validar campos requeridos
        missing_required = self._validate_required_fields(detected_mapping)
        
        # Mostrar resultados de detección
        self._display_detection_results(detected_mapping, confidence_scores, missing_required)
        
        return detected_mapping
    
    def _analyze_column(self, df: pd.DataFrame, col: str) -> Tuple[Optional[str], float]:
        """Analiza una columna específica para determinar su tipo"""
        
        col_lower = col.lower().strip()
        sample_data = df[col].dropna().head(100)  # Muestra para análisis
        
        best_field = None
        best_score = 0.0
        
        for field_name, field_config in self.field_patterns.items():
            score = self._calculate_field_score(col_lower, sample_data, field_config)
            
            if score > best_score:
                best_score = score
                best_field = field_name
        
        return best_field, best_score
    
    def _calculate_field_score(self, col_name: str, sample_data: pd.Series, field_config: dict) -> float:
        """Calcula el score de confianza para un campo específico"""
        
        score = 0.0
        
        # 1. Análisis por keywords en nombre de columna (40% del score)
        keyword_score = 0.0
        for keyword in field_config.get('keywords', []):
            if keyword in col_name:
                keyword_score = 0.4
                break
        
        # 2. Análisis por patrones en los datos (35% del score)
        pattern_score = 0.0
        if 'patterns' in field_config and len(sample_data) > 0:
            pattern_matches = 0
            total_samples = len(sample_data)
            
            for pattern in field_config['patterns']:
                matches = sample_data.astype(str).str.match(pattern).sum()
                match_ratio = matches / total_samples
                pattern_score = max(pattern_score, match_ratio * 0.35)
        
        # 3. Análisis por valores esperados (25% del score)
        value_score = 0.0
        if 'values' in field_config and len(sample_data) > 0:
            expected_values = [v.lower() for v in field_config['values']]
            sample_values = sample_data.astype(str).str.lower().unique()
            
            matches = sum(1 for val in sample_values if any(exp in val for exp in expected_values))
            value_score = (matches / len(sample_values)) * 0.25 if len(sample_values) > 0 else 0
        
        # Score total
        total_score = keyword_score + pattern_score + value_score
        
        return min(total_score, 1.0)  # Máximo 1.0
    
    def _validate_required_fields(self, mapping: Dict[str, str]) -> List[str]:
        """Valida que los campos requeridos estén presentes"""
        
        missing_required = []
        
        for field_name, field_config in self.field_patterns.items():
            if field_config.get('required', False) and field_name not in mapping:
                missing_required.append(field_name)
        
        return missing_required
    
    def _display_detection_results(self, mapping: Dict[str, str], confidence: Dict[str, float], missing: List[str]):
        """Muestra los resultados de la detección al usuario"""
        
        st.subheader("🎯 Resultados de Autodetección")
        
        if mapping:
            st.success(f"✅ **{len(mapping)} campos detectados automáticamente**")
            
            # Mostrar mapeo detectado
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.write("**Campo CEAPSI**")
            with col2:
                st.write("**Columna Detectada**")
            with col3:
                st.write("**Confianza**")
            
            st.markdown("---")
            
            # Ordenar por prioridad
            sorted_mapping = sorted(mapping.items(), 
                                  key=lambda x: self.field_patterns[x[0]].get('priority', 99))
            
            for field, column in sorted_mapping:
                conf = confidence.get(field, 0)
                
                with col1:
                    icon = "📅" if field == "FECHA" else "📞" if field == "TELEFONO" else "🔄" if field == "SENTIDO" else "✅" if field == "ATENDIDA" else "⏱️" if field == "DURACION" else "👤"
                    st.write(f"{icon} **{field}**")
                with col2:
                    st.write(f"`{column}`")
                with col3:
                    color = "green" if conf > 0.7 else "orange" if conf > 0.4 else "red"
                    st.markdown(f"<span style='color: {color}'>{conf:.0%}</span>", unsafe_allow_html=True)
        
        # Mostrar campos faltantes
        if missing:
            st.warning(f"⚠️ **Campos requeridos no detectados**: {', '.join(missing)}")
            st.info("💡 Puedes mapear manualmente estos campos en la siguiente sección")
        
        # Estadísticas de detección
        if mapping:
            with st.expander("📊 Estadísticas de Detección"):
                total_cols = len(mapping)
                high_conf = sum(1 for c in confidence.values() if c > 0.7)
                medium_conf = sum(1 for c in confidence.values() if 0.4 <= c <= 0.7)
                low_conf = sum(1 for c in confidence.values() if c < 0.4)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Detectado", total_cols)
                with col2:
                    st.metric("Alta Confianza", high_conf, f"{high_conf/total_cols:.0%}")
                with col3:
                    st.metric("Media Confianza", medium_conf, f"{medium_conf/total_cols:.0%}")
                with col4:
                    st.metric("Baja Confianza", low_conf, f"{low_conf/total_cols:.0%}")
    
    def create_manual_mapping_interface(self, df: pd.DataFrame, detected_mapping: Dict[str, str]) -> Dict[str, str]:
        """Crea interfaz para corrección manual del mapeo"""
        
        st.subheader("🔧 Corrección Manual de Mapeo")
        st.info("Ajusta el mapeo automático si es necesario")
        
        available_columns = ['-- No mapear --'] + list(df.columns)
        final_mapping = {}
        
        # Crear selectboxes para cada campo
        for field_name, field_config in sorted(self.field_patterns.items(), key=lambda x: x[1].get('priority', 99)):
            
            # Determinar valor por defecto
            current_mapping = detected_mapping.get(field_name, '-- No mapear --')
            try:
                default_index = available_columns.index(current_mapping)
            except ValueError:
                default_index = 0
            
            # Crear interfaz
            col1, col2, col3 = st.columns([2, 3, 1])
            
            with col1:
                required_text = " ⭐" if field_config.get('required', False) else ""
                st.write(f"**{field_name}**{required_text}")
            
            with col2:
                selected_column = st.selectbox(
                    label=f"Mapear {field_name}",
                    options=available_columns,
                    index=default_index,
                    key=f"mapping_{field_name}",
                    label_visibility="collapsed"
                )
            
            with col3:
                if selected_column != '-- No mapear --':
                    # Mostrar preview de datos
                    sample_data = df[selected_column].dropna().head(3).tolist()
                    preview_text = ", ".join(str(x)[:20] for x in sample_data)
                    st.caption(f"📋 {preview_text}...")
            
            # Guardar mapeo si está seleccionado
            if selected_column != '-- No mapear --':
                final_mapping[field_name] = selected_column
        
        return final_mapping
    
    def validate_final_mapping(self, mapping: Dict[str, str], df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """Valida el mapeo final antes de procesar"""
        
        errors = []
        
        # Verificar campos requeridos
        for field_name, field_config in self.field_patterns.items():
            if field_config.get('required', False) and field_name not in mapping:
                errors.append(f"Campo requerido '{field_name}' no está mapeado")
        
        # Verificar que las columnas existen
        for field_name, column_name in mapping.items():
            if column_name not in df.columns:
                errors.append(f"Columna '{column_name}' no existe en el archivo")
        
        # Verificar duplicados
        mapped_columns = list(mapping.values())
        duplicates = [col for col in mapped_columns if mapped_columns.count(col) > 1]
        if duplicates:
            errors.append(f"Columnas duplicadas en mapeo: {', '.join(set(duplicates))}")
        
        return len(errors) == 0, errors
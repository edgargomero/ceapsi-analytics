# 📞 CEAPSI - Sistema de Análisis Inteligente para Call Center

Sistema completo de predicción y análisis de llamadas para call center usando machine learning avanzado y visualizaciones interactivas.

## 🎯 Características Principales

### 📊 Dashboard v2 con Analytics Avanzado
- **5 Tabs de Análisis**: Predicciones, Residuales, Métricas, Mapas de Calor, Recomendaciones
- **🔥 Mapas de Calor Temporales**: 
  - Semanas vs Días (últimas 20 semanas)
  - Días vs Horas (patrón horario)
  - Calendario Mensual (últimos 90 días)
- **📈 Análisis de Residuales**: Distribución temporal y estadísticas
- **🎯 Métricas de Performance**: Comparación de modelos con interpretación automática
- **📊 Análisis de Estabilidad**: Detección de anomalías y tendencias

### 🤖 Machine Learning
- **4 Modelos**: Prophet, ARIMA, Random Forest, Gradient Boosting
- **Pipeline Optimizado**: ~5 segundos para 341k registros
- **Métricas en Tiempo Real**: MAE, RMSE, MAPE, R²
- **Predicciones**: 28 días hacia adelante

### 🚀 Características del Sistema
- **Auto-detección de Campos**: Mapeo inteligente de columnas CSV/Excel
- **Monitor de Recursos**: CPU y RAM en tiempo real durante procesamiento
- **Autenticación Supabase**: Login seguro requerido
- **Progreso Visual**: Pipeline de 4 etapas con logging detallado
- **Exportación de Resultados**: JSON, CSV, visualizaciones

## 📋 Requisitos

### Columnas Requeridas en Datos
- `FECHA`: Fecha y hora (formato: DD-MM-YYYY HH:MM:SS)
- `TELEFONO`: Número de teléfono
- `SENTIDO`: 'in' (entrante) o 'out' (saliente)
- `ATENDIDA`: 'Si' o 'No'

### Dependencias
```bash
pip install -r requirements.txt
```

Principales librerías:
- streamlit>=1.32.0
- pandas>=2.0.3
- plotly>=5.17.0
- prophet>=1.1.5
- scikit-learn>=1.3.0
- supabase==2.8.0
- psutil>=5.9.0
- scipy>=1.11.0

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone https://github.com/edgargomero/ceapsia.git
cd ceapsia
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
Crear archivo `.env`:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### 4. Ejecutar la aplicación
```bash
streamlit run app.py
```

## 🔄 Flujo de Trabajo

1. **Login**: Autenticación con Supabase
2. **Carga de Datos**: Subir CSV/Excel desde panel lateral
3. **Auto-detección**: Sistema mapea campos automáticamente
4. **Pipeline Automático**:
   - 🔍 Auditoría (15s) - Validación de calidad
   - 🔀 Segmentación (20s) - Separación entrante/saliente
   - 🤖 Entrenamiento (45s) - 4 modelos ML
   - 🔮 Predicciones (25s) - 28 días de pronóstico
5. **Dashboard**: Visualización interactiva de resultados

## 📊 Estructura del Proyecto

```
ceapsia/
├── app.py                              # Aplicación principal
├── src/
│   ├── ui/
│   │   ├── dashboard_comparacion_v2.py # Dashboard refactorizado
│   │   ├── dashboard_analytics.py      # Módulo de analytics
│   │   └── components/                 # Componentes modulares
│   │       ├── data_loader.py         # Carga de datos
│   │       ├── data_validator.py      # Validación
│   │       └── chart_visualizer.py    # Visualizaciones
│   ├── models/                         # Modelos ML
│   ├── auth/                           # Autenticación
│   └── services/                       # Servicios
├── requirements.txt                    # Dependencias
└── docs/                              # Documentación
```

## 🎨 Nuevas Funcionalidades Dashboard v2

### 1. Predicciones vs Real
- Gráfico interactivo con navegación mejorada
- Rangos predefinidos: 30D, 3M, 6M, Todo
- Slider de rango temporal
- Marcador visual de separación histórico/predicciones

### 2. Análisis de Residuales
- Gráfico temporal de residuales
- Histograma de distribución
- Estadísticas: Media, Desv. Estándar, Min, Max

### 3. Métricas de Performance
- Tabla comparativa de modelos
- Gráficos de barras R² y MAPE
- Interpretación automática de métricas
- Análisis de estabilidad temporal
- Comparación entre períodos

### 4. Mapas de Calor
- **Semanal**: Identifica patrones y días problemáticos
- **Horario**: Optimiza asignación de personal
- **Calendario**: Vista mensual de actividad
- Insights automáticos con estadísticas

## 🔧 Solución de Problemas

### Error de autenticación
- Verificar variables SUPABASE_URL y SUPABASE_ANON_KEY
- Confirmar que el usuario existe en Supabase

### Pipeline muy lento
- Verificar tamaño del dataset (óptimo < 500k registros)
- Monitorear CPU/RAM durante ejecución
- Considerar filtrar datos históricos muy antiguos

### Gráficos no cargan
- Verificar formato de fechas (DD-MM-YYYY HH:MM:SS)
- Confirmar que hay datos para el tipo de llamada seleccionado
- Revisar logs en consola para errores específicos

## 📈 Performance

- **Velocidad Pipeline**: ~5 segundos para 341k registros
- **Visualización**: Optimizada para 10k puntos máximo
- **Memoria**: Procesamiento eficiente por lotes
- **Cache**: Datos en session_state, 5 min TTL

## 🌟 Flujo de Desarrollo con Git

### Ramas Principales
- **`main`**: Rama principal con código estable (producción)
- **`development`**: Rama de desarrollo para pruebas y nuevas funciones

### Flujo de Trabajo Recomendado

#### 1. Desarrollo Diario
```bash
# Cambiar a rama de desarrollo
git checkout development

# Actualizar con últimos cambios
git pull origin development

# Hacer cambios y commits
git add .
git commit -m "Update: descripción del cambio"
git push origin development
```

#### 2. Nueva Funcionalidad
```bash
# Crear rama desde development
git checkout development
git checkout -b feature/nombre-descriptivo

# Desarrollar y hacer commits
git add .
git commit -m "Add: nueva funcionalidad"

# Subir rama feature
git push origin feature/nombre-descriptivo

# Merge a development cuando esté listo
git checkout development
git merge feature/nombre-descriptivo
git push origin development
```

#### 3. Actualizar Producción
```bash
# Solo cuando development esté probado y estable
git checkout main
git merge development
git push origin main
```

### Comandos Útiles
```bash
# Ver rama actual
git branch

# Ver todas las ramas (locales y remotas)
git branch -a

# Ver diferencias entre ramas
git diff main development

# Eliminar rama local
git branch -d feature/nombre

# Ver historial de commits
git log --oneline --graph --all
```

## 🤝 Contribuir

1. Fork el proyecto
2. Clonar tu fork (`git clone https://github.com/tu-usuario/ceapsi-analytics.git`)
3. Crear rama desde `development` (`git checkout -b feature/NuevaCaracteristica`)
4. Commit cambios (`git commit -m 'Add: Nueva característica'`)
5. Push al branch (`git push origin feature/NuevaCaracteristica`)
6. Crear Pull Request hacia `development` (no a `main`)

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver archivo `LICENSE` para más detalles.

## 📧 Soporte

- **GitHub Issues**: https://github.com/edgargomero/ceapsia/issues
- **Email**: soporte@ceapsi.cl
- **Documentación**: Ver carpeta `/docs`

---

**CEAPSI v2.0** - Sistema de Análisis Inteligente para Call Center 🚀
# 🤝 Guía de Contribución - CEAPSI Analytics

¡Gracias por tu interés en contribuir al proyecto CEAPSI! Esta guía te ayudará a entender nuestro flujo de trabajo y mejores prácticas.

## 🌟 Flujo de Trabajo Git

### Estructura de Ramas

```
main (producción)
  └── development (desarrollo activo)
       ├── feature/nueva-funcionalidad
       ├── feature/mejora-dashboard
       └── bugfix/correccion-error
```

### Tipos de Ramas

- **`main`**: Código estable en producción
- **`development`**: Desarrollo y pruebas activas
- **`feature/*`**: Nuevas funcionalidades
- **`bugfix/*`**: Corrección de errores
- **`hotfix/*`**: Correcciones urgentes en producción

## 📋 Proceso de Contribución

### 1. Preparar Entorno

```bash
# Clonar repositorio
git clone https://github.com/edgargomero/ceapsi-analytics.git
cd ceapsi-analytics

# Cambiar a development
git checkout development
git pull origin development

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales
```

### 2. Crear Nueva Feature

```bash
# Asegurarse de estar en development actualizado
git checkout development
git pull origin development

# Crear rama para nueva feature
git checkout -b feature/descripcion-breve

# Ejemplo:
git checkout -b feature/export-pdf-reports
```

### 3. Desarrollo

```bash
# Hacer cambios en el código
# ...

# Ver cambios
git status
git diff

# Agregar cambios
git add .

# Commit con mensaje descriptivo
git commit -m "Add: export functionality for PDF reports"
```

### 4. Mensajes de Commit

Usa estos prefijos para mantener consistencia:

- `Add:` Nueva funcionalidad
- `Update:` Actualización de funcionalidad existente
- `Fix:` Corrección de error
- `Remove:` Eliminación de código/archivos
- `Refactor:` Refactorización sin cambios funcionales
- `Docs:` Cambios en documentación
- `Test:` Adición o modificación de tests

Ejemplos:
```bash
git commit -m "Add: heatmap visualization for weekly patterns"
git commit -m "Fix: datetime format error in calendar view"
git commit -m "Update: improve performance metrics calculation"
git commit -m "Docs: add git workflow guide to README"
```

### 5. Probar Cambios

```bash
# Ejecutar aplicación
streamlit run app.py

# Validar sistema
python verify_ceapsi.py

# Probar con datos de ejemplo
# Subir assets/data/ejemplo_datos_llamadas.csv
```

### 6. Subir Cambios

```bash
# Subir rama al repositorio
git push origin feature/descripcion-breve

# Si es primera vez
git push -u origin feature/descripcion-breve
```

### 7. Pull Request

1. Ir a GitHub
2. Crear Pull Request desde tu rama hacia `development`
3. Describir cambios y adjuntar screenshots si es visual
4. Esperar revisión

## 🧪 Testing

### Antes de hacer PR, verificar:

- [ ] La aplicación inicia sin errores
- [ ] Los datos de ejemplo cargan correctamente
- [ ] Las visualizaciones se muestran bien
- [ ] No hay errores en la consola
- [ ] El pipeline completa en < 10 segundos
- [ ] Los mapas de calor funcionan correctamente

### Comandos de Testing

```bash
# Verificar sistema
python verify_ceapsi.py

# Probar con diferentes datasets
# - Subir ejemplo_datos_llamadas.csv
# - Probar con archivos Excel
# - Verificar detección automática de campos
```

## 📐 Estándares de Código

### Python
- Seguir PEP 8
- Usar nombres descriptivos en español o inglés (consistente)
- Documentar funciones complejas
- Manejar errores con try/except y logging

### Estructura de Archivos
```python
# Imports ordenados
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime

# Luego imports locales
from src.ui.dashboard_analytics import AnalyticsModule
```

### Logging
```python
import logging
logger = logging.getLogger('CEAPSI.ModuleName')

# Usar apropiadamente
logger.info("Proceso iniciado")
logger.error(f"Error: {e}")
logger.debug("Detalles para debugging")
```

## 🚀 Merge a Producción

Solo los maintainers pueden hacer merge a `main`:

```bash
# Desde development probado
git checkout main
git merge development
git push origin main

# Crear tag de versión
git tag -a v2.1.0 -m "Version 2.1.0: Add PDF export"
git push origin v2.1.0
```

## ❓ FAQ

### ¿Cómo actualizo mi rama con cambios de development?

```bash
git checkout development
git pull origin development
git checkout feature/mi-feature
git merge development
```

### ¿Qué hacer si hay conflictos?

```bash
# Resolver conflictos manualmente
# Editar archivos en conflicto
git add archivos-resueltos
git commit -m "Fix: merge conflicts with development"
```

### ¿Cómo elimino una rama local?

```bash
# Después de merge
git branch -d feature/mi-feature

# Forzar eliminación
git branch -D feature/mi-feature
```

## 📞 Soporte

- **Issues**: https://github.com/edgargomero/ceapsi-analytics/issues
- **Discussions**: https://github.com/edgargomero/ceapsi-analytics/discussions
- **Email**: soporte@ceapsi.cl

---

¡Gracias por contribuir a CEAPSI Analytics! 🚀
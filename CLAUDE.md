# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**CEAPSI** is a comprehensive call center prediction and analysis system with a Streamlit-based architecture for interactive analysis. The system leverages multiple machine learning models for call volume prediction and includes advanced analytics features.

## Key Commands

### Git Workflow Commands
```bash
# Development branch (for daily work)
git checkout development
git pull origin development

# Feature branches (for new features)
git checkout -b feature/feature-name
git push origin feature/feature-name

# Production updates (only stable code)
git checkout main
git merge development
git push origin main
```

### Streamlit Application
```bash
# Main application
streamlit run app.py

# Development launcher
python scripts/development/run.py

# Legacy versions (backup)
streamlit run app_legacy.py
streamlit run app_too_optimized.py
```

### Testing and Validation
```bash
# System validation
python verify_ceapsi.py
python fix_ceapsi.py

# Backend tests (if using API)
cd backend
pytest tests/
```

### Development Dependencies
```bash
# Install dependencies
pip install -r requirements.txt

# Code formatting (optional)
black .
isort .
flake8 .
```

## Architecture Overview

### Single Page Application Architecture
- **Frontend**: Streamlit app (`app.py`) - Interactive dashboard with ML predictions
- **Dashboard**: Dashboard v2 (`src/ui/dashboard_comparacion_v2.py`) - Advanced analytics
- **Database**: Supabase - Authentication and data persistence
- **Storage**: Local files + Supabase for session data

### Core Components

#### Frontend Layer (`src/`)
- **UI Components** (`src/ui/`): 
  - `dashboard_comparacion_v2.py` - Main dashboard with 5 tabs
  - `components/` - Modular components (data_loader, data_validator, chart_visualizer)
  - `dashboard_analytics.py` - Advanced analytics module
- **ML Models** (`src/models/`): Multi-model ensemble (Prophet, ARIMA, Random Forest, Gradient Boosting)
- **Services** (`src/services/`): Data processing pipelines and automation
- **Authentication** (`src/auth/`): Supabase integration with secure token management

#### Dashboard v2 Features
1. **📊 Predicciones vs Real**: Interactive predictions with enhanced navigation
2. **📈 Análisis de Residuales**: Temporal and distribution analysis
3. **🎯 Métricas de Performance**: Model comparison with stability analysis
4. **🔥 Mapas de Calor**: 3 temporal heatmap views (weekly, hourly, calendar)
5. **📋 Recomendaciones**: Automated insights (in development)

#### Data Flow Architecture
1. **Data Input**: CSV/Excel upload with automatic field detection
2. **Processing**: 4-stage pipeline (Audit → Segment → Train → Predict)
3. **Storage**: Results in `st.session_state.resultados_pipeline`
4. **Output**: Interactive Plotly visualizations

### Security Features
- **Authentication**: Supabase JWT required for access
- **File Validation**: Format verification and encoding detection
- **Error Handling**: Secure error messages without sensitive data
- **Key Management**: ANON_KEY for frontend, SERVICE_ROLE_KEY for backend only

## Development Patterns

### Data Processing Pipeline
- **Required Columns**: `FECHA`, `TELEFONO`, `SENTIDO`, `ATENDIDA`
- **Supported Formats**: CSV (semicolon-separated), Excel
- **Processing Speed**: ~5 seconds for 341k records
- **Automatic Features**:
  - Field auto-detection with manual override
  - Multiple encoding support (utf-8, latin-1, cp1252)
  - Future date filtering
  - Missing user assignment to 'WEB_CEAPSI'

### Machine Learning Workflow
- **Models**: Prophet, ARIMA, Random Forest, Gradient Boosting
- **Pipeline Stages**:
  1. 🔍 Auditoría (15s) - Data quality validation
  2. 🔀 Segmentación (20s) - Inbound/outbound separation
  3. 🤖 Entrenamiento (45s) - Model training
  4. 🔮 Predicciones (25s) - 28-day forecasting
- **Results**: Stored in session state for dashboard access

### Advanced Analytics Features
- **Residual Analysis**: Error patterns and distribution
- **Performance Metrics**: MAE, RMSE, MAPE, R² with interpretations
- **Stability Analysis**: Temporal stability with anomaly detection
- **Period Comparison**: Recent vs previous period metrics
- **Heatmaps**: Weekly patterns, hourly patterns, calendar view

## Configuration Management

### Environment Variables
```bash
# Supabase Configuration (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key  # Backend only

# External APIs (Optional)
API_KEY=Token your-reservo-api-key
API_URL=https://reservo.cl/APIpublica/v2

# Development
ENVIRONMENT=development  # Shows dev warnings
```

### Streamlit Configuration
- **Page Config**: Wide layout, expanded sidebar
- **Custom CSS**: Professional styling with gradients
- **Resource Monitoring**: psutil integration for CPU/RAM tracking

## File Structure

```
ceapsia/
├── app.py                              # Main application (2007 lines)
├── src/
│   ├── ui/
│   │   ├── dashboard_comparacion_v2.py # Dashboard v2 (refactored)
│   │   ├── dashboard_analytics.py      # Analytics module
│   │   └── components/                 # Modular components
│   │       ├── data_loader.py
│   │       ├── data_validator.py
│   │       └── chart_visualizer.py
│   ├── models/
│   │   └── sistema_multi_modelo.py     # ML ensemble
│   ├── auth/
│   │   └── supabase_auth.py           # Authentication
│   └── services/                       # Processing services
├── requirements.txt                    # Dependencies
└── docs/                              # Documentation
```

## Common Workflows

### Running the Application
1. Set environment variables or create `.env` file
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Login with Supabase credentials
5. Upload CSV/Excel file
6. Pipeline executes automatically
7. View results in Dashboard

### Adding New Analytics
1. Implement in `src/ui/dashboard_analytics.py`
2. Add new tab in `dashboard_comparacion_v2.py`
3. Update navigation and logging
4. Test with sample data

### Debugging Pipeline Issues
1. Check console logs for detailed pipeline stages
2. Verify data format matches requirements
3. Monitor resource usage (CPU/RAM indicators)
4. Review `st.session_state.resultados_pipeline` structure

## Performance Optimization

- **Large Datasets**: Automatic sampling for visualization (10k points)
- **Pipeline Speed**: Optimized from minutes to ~5 seconds
- **Memory Usage**: Efficient batch processing
- **Caching**: Streamlit's `@st.cache_data` for expensive operations

## Development Workflow

### Branch Strategy
- **`main`**: Production-ready stable code
- **`development`**: Active development and testing
- **`feature/*`**: Individual feature development

### Development Process
1. **Always work in `development` or feature branches**
   ```bash
   git checkout development
   git pull origin development
   ```

2. **Create feature branches for new functionality**
   ```bash
   git checkout -b feature/analytics-improvements
   ```

3. **Test thoroughly before merging to main**
   - Run all validation scripts
   - Test with sample data
   - Verify dashboard functionality

4. **Merge to production only when stable**
   ```bash
   git checkout main
   git merge development
   git push origin main
   ```

### Best Practices
- Never commit directly to `main`
- Always pull latest changes before starting work
- Use descriptive branch names
- Test in `development` before production
- Keep feature branches small and focused

## Current Status

✅ **Completed**:
- Dashboard v2 with advanced analytics
- Residual analysis implementation
- Performance metrics with visualizations
- Temporal heatmaps (3 types)
- Stability and period comparison analysis
- Complete removal of Dashboard v1
- Field auto-detection system
- Resource monitoring
- Git workflow with branch strategy

🚧 **In Development**:
- Automated recommendations tab
- Cross-analysis with user data
- API integration improvements

## Support

For issues or questions:
- GitHub: https://github.com/edgargomero/analisis_resultados
- Email: soporte@ceapsi.cl
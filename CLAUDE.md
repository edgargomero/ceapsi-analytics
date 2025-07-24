# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**CEAPSI** is a comprehensive call center prediction and analysis system with dual architecture - a Streamlit frontend for interactive analysis and a FastAPI backend for secure API operations. The system leverages multiple machine learning models for call volume prediction and includes advanced security features.

## Key Commands

### Streamlit Frontend (Primary Interface)
```bash
# Main application
streamlit run app.py

# Development launcher
python scripts/development/run.py

# Legacy version (backup)
streamlit run app_legacy.py
```

### FastAPI Backend (Optional API Layer)
```bash
# Start backend server
cd backend
uvicorn app.main:app --reload --port 8000

# Backend deployment
python scripts/deployment/deploy_backend.py
```

### Testing and Validation
```bash
# Backend tests (pytest-based)
cd backend
pytest tests/unit/
pytest tests/integration/ 
pytest tests/fixtures/

# System validation (custom)
python verify_ceapsi.py
python fix_ceapsi.py
```

### Development Dependencies
```bash
# Frontend dependencies
pip install -r requirements.txt

# Backend dependencies  
pip install -r backend/requirements.txt

# Code formatting (backend)
cd backend
black .
isort .
flake8 .
```

## Architecture Overview

### Hybrid Architecture
- **Frontend**: Streamlit app (`app.py`) - Interactive dashboard with ML predictions
- **Backend**: FastAPI (`backend/app/main.py`) - Optional secure API layer
- **Database**: Supabase - Authentication, session storage, and data persistence
- **Storage**: Local files + Supabase for session data and analysis results

### Core Components

#### Frontend Layer (`src/`)
- **UI Components** (`src/ui/`): Optimized, reusable dashboard components with lazy loading
- **ML Models** (`src/models/`): Multi-model ensemble (Prophet, XGBoost, Random Forest, Linear Regression)
- **Services** (`src/services/`): Data processing pipelines and automation
- **Authentication** (`src/auth/`): Supabase integration with secure token management

#### Backend Layer (`backend/app/`)
- **Security** (`core/`): Rate limiting, file validation, error handling, authentication
- **API Routes** (`api/routers/`): REST endpoints for analysis, data, sessions, models
- **Configuration** (`core/config.py`): Environment-based settings management

#### Data Flow Architecture
1. **Data Input**: CSV/Excel upload with format validation
2. **Processing**: Multi-model training and prediction pipeline
3. **Storage**: Results cached in Supabase with session management
4. **Output**: Interactive Plotly visualizations and downloadable reports

### Security Features
- **Rate Limiting**: 60 requests/minute per IP
- **File Validation**: Anti-malware scanning and format verification
- **Authentication**: Supabase JWT with role-based access (Admin/Analyst/Viewer)
- **Key Separation**: Anonymous keys for frontend, service role keys for backend
- **Error Handling**: Secure error messages without sensitive data exposure

## Development Patterns

### Data Processing Pipeline
- **Required Columns**: `FECHA`, `TELEFONO`, `SENTIDO`, `ATENDIDA`
- **Supported Formats**: CSV, Excel with automatic encoding detection
- **Batch Processing**: Configurable batch sizes to prevent memory issues
- **Error Recovery**: Comprehensive retry logic and fallback mechanisms

### Machine Learning Workflow
- **Multi-Model Ensemble**: Combines Prophet (time series), XGBoost, Random Forest, Linear Regression
- **Performance Targets**: MAE < 10, RMSE < 15, MAPE < 25%
- **Cross-Validation**: Temporal splits for time series validation
- **Model Persistence**: Serialized models with timestamp versioning

### Session Management (MCP Protocol)
- **Session Tracking**: UUID-based session identification
- **State Persistence**: Analysis results and uploaded files cached
- **User Context**: Role-based feature access and data visibility
- **Database Integration**: Automatic session metadata storage

## Configuration Management

### Environment Variables
```bash
# Supabase Configuration (Required)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

# External APIs
API_KEY=Token your-reservo-api-key
API_URL=https://reservo.cl/APIpublica/v2

# Backend Configuration
SECRET_KEY=your-secret-key
DEBUG=false
HOST=0.0.0.0
PORT=8000
```

### Streamlit Configuration
- **Config File**: `config/streamlit_config.toml`
- **Deployment**: Optimized for Streamlit Cloud with secrets management
- **Responsive Design**: Mobile-optimized dashboard components

## Data Integration

### External APIs
- **Reservo API**: Professional and appointment data synchronization
- **Rate Limits**: 5 requests/hour for external API calls
- **Caching**: Response caching to minimize API usage

### Database Schema
- **Sessions Table**: Analysis session metadata and results
- **Users Table**: Authentication and role management
- **Audit Logs**: Comprehensive system activity tracking

## File Structure Highlights

```
ceapsia/
├── app.py                          # Main Streamlit application (v2.0 optimized)
├── backend/app/main.py             # FastAPI backend entry point
├── src/
│   ├── ui/optimized_frontend.py    # Reusable UI components
│   ├── models/sistema_multi_modelo.py # ML ensemble system
│   ├── core/mcp_session_manager.py # Session management
│   └── services/automatizacion_completa.py # Complete automation pipeline
├── scripts/development/run.py      # Development launcher
├── database/migrations/            # SQL migration files
└── docs/                          # Comprehensive documentation
```

## Testing Strategy

### Frontend Testing
- **Data Validation**: CSV/Excel format verification with sample data
- **UI Components**: Interactive dashboard functionality across different datasets
- **Model Performance**: Prediction accuracy against known datasets

### Backend Testing  
- **Unit Tests**: Individual component testing with pytest
- **Integration Tests**: API endpoint testing with authentication
- **Security Tests**: Rate limiting, file validation, error handling

### System Testing
- **End-to-End**: Complete workflow from data upload to predictions
- **Performance**: Load testing with large datasets
- **Security**: Authentication flows and data protection

## Deployment Considerations

### Streamlit Cloud Deployment
- **Secrets Management**: Environment variables configured in Streamlit Cloud settings
- **Performance**: Optimized with lazy loading and component caching
- **Security**: Rate limiting and secure error handling for production

### FastAPI Backend Deployment
- **Container Ready**: Dockerizable FastAPI application
- **Health Checks**: Built-in endpoint monitoring
- **Scaling**: Async operations with proper resource management

## Common Workflows

### Adding New ML Models
1. Implement in `src/models/sistema_multi_modelo.py`
2. Update ensemble weighting logic
3. Add validation metrics
4. Test with sample datasets

### Implementing New API Endpoints  
1. Create router in `backend/app/api/routers/`
2. Add authentication decorators
3. Implement rate limiting
4. Add comprehensive error handling

### Security Updates
1. Review `backend/app/core/` security modules
2. Update rate limits and validation rules
3. Test authentication flows
4. Verify error message sanitization
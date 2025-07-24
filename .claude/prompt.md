# CEAPSI Project Context

## Overview
CEAPSI is a comprehensive call center prediction and analysis system with dual architecture:
- **Frontend**: Streamlit app for interactive ML-powered analytics
- **Backend**: FastAPI for secure API operations
- **Database**: Supabase for authentication and data persistence

## Architecture
- **UI Components** (`src/ui/`): Optimized dashboard components with lazy loading
- **ML Models** (`src/models/`): Multi-model ensemble (Prophet, XGBoost, Random Forest, Linear Regression)
- **Services** (`src/services/`): Data processing pipelines and automation
- **Authentication** (`src/auth/`): Supabase integration with secure token management

## Key Features
- Multi-model ML ensemble for call volume prediction
- Real-time data processing and visualization
- Session management with MCP protocol
- Comprehensive security features (rate limiting, file validation)
- Role-based access control (Admin/Analyst/Viewer)

## Data Requirements
- **Required Columns**: `FECHA`, `TELEFONO`, `SENTIDO`, `ATENDIDA`
- **Supported Formats**: CSV, Excel with automatic encoding detection
- **Performance Targets**: MAE < 10, RMSE < 15, MAPE < 25%

## Development Guidelines
- Follow existing patterns in `src/` directory structure
- Use Supabase for all authentication and data persistence
- Implement proper error handling and rate limiting
- Maintain ML model performance metrics
- Test with small datasets before full deployment

## Common Tasks
- Adding ML models: Update `src/models/sistema_multi_modelo.py`
- New API endpoints: Create in `backend/app/api/routers/`
- UI components: Add to `src/ui/optimized_frontend.py`
- Security updates: Review `backend/app/core/` modules
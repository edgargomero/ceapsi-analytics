# Configuración de CEAPSI en Streamlit Cloud

## Variables de Entorno Requeridas

En Streamlit Cloud, configura las siguientes variables en Settings > Secrets:

```toml
# IMPORTANTE: Usar ANON KEY para frontend, NO service role key
SUPABASE_URL = "https://lvouimzndppleeolbbhj.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imx2b3VpbXpuZHBwbGVlb2xiYmhqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTMyMTk0ODAsImV4cCI6MjA2ODc5NTQ4MH0.-zTF-4dHjEFI2MP6XPumrGhFaBzYymTOv7gar1EVEmk"

# API de Reservo (opcional)
RESERVO_API_KEY = "Token 53db414936e40ec5091e2e6074bdaced68709821"

# NO INCLUIR service role key en frontend por seguridad
```

## Validación de Seguridad

El sistema valida automáticamente que se esté usando la ANON KEY correcta:
- ✅ Si detecta "anon" en la key: Configuración correcta
- ❌ Si detecta "service_role": ERROR de seguridad - no se conectará
- ⚠️ Si la key es muy larga (>250 chars): Probablemente es service role key

## Estructura de Archivos

El sistema carga las credenciales en este orden de prioridad:
1. `st.secrets['SUPABASE_ANON_KEY']` (Streamlit Cloud)
2. `os.getenv('SUPABASE_ANON_KEY')` (desarrollo local)
3. `st.secrets['SUPABASE_KEY']` (fallback - no recomendado)

## Verificación Post-Despliegue

Después de desplegar, verifica en los logs:
- Busca: "✅ Usando ANON KEY correctamente para frontend"
- Si ves: "⚠️ PELIGRO: Frontend está usando SERVICE ROLE KEY" - corrige inmediatamente

## Notas de Seguridad

- **NUNCA** incluyas la SERVICE_ROLE_KEY en el frontend
- La SERVICE_ROLE_KEY solo debe usarse en backend seguro
- La ANON_KEY tiene permisos limitados apropiados para frontend
- Streamlit Cloud es público - cualquier secret puede ser expuesto
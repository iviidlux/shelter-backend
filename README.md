# ShelterControl - Backend Python

Backend de Python para generación de reportes PDF con análisis de datos y gráficas.

## 🚀 Características

- **Generación de Reportes PDF**: Reportes semanales y mensuales con gráficas profesionales
- **Análisis de Datos**: Estadísticas avanzadas con pandas
- **Gráficas Interactivas**: Visualizaciones con matplotlib
- **Integración con Supabase**: Conexión directa a la base de datos
- **API REST**: Endpoints para Flutter

## 📋 Requisitos

- Python 3.9 o superior
- pip (gestor de paquetes)
- Cuenta de Supabase configurada

## 🛠️ Instalación

### 1. Crear entorno virtual

```bash
cd python_backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

Copia el archivo `.env.example` a `.env`:

```bash
cp .env.example .env
```

Edita `.env` y agrega tus credenciales de Supabase:

```
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_anon_key
PORT=5000
```

### 4. Iniciar servidor

```bash
python app.py
```

O usa el script de inicio:

```bash
chmod +x start.sh
./start.sh
```

El servidor estará disponible en `http://localhost:5000`

## 📡 Endpoints API

### Health Check

```
GET /health
```

Verifica el estado del servidor.

**Respuesta:**
```json
{
  "status": "ok",
  "message": "ShelterControl Backend is running",
  "timestamp": "2025-11-25T10:00:00"
}
```

### Generar Reporte Semanal

```
POST /api/reports/weekly
```

**Body:**
```json
{
  "start_date": "2025-11-18",
  "end_date": "2025-11-25",
  "shelter_name": "Albergue Central"
}
```

**Respuesta:**
Archivo PDF descargable

### Generar Reporte Mensual

```
POST /api/reports/monthly
```

**Body:**
```json
{
  "month": 11,
  "year": 2025,
  "shelter_name": "Albergue Central"
}
```

**Respuesta:**
Archivo PDF descargable

### Obtener Resumen Analítico

```
POST /api/analytics/summary
```

**Body:**
```json
{
  "start_date": "2025-11-01",
  "end_date": "2025-11-30"
}
```

**Respuesta:**
```json
{
  "total_personas": 45,
  "personas_activas": 38,
  "total_donaciones": 120,
  "total_entregas": 95,
  "alimentos_disponibles": 25,
  "total_donadores": 18,
  "avg_days_hospedaje": 15.5,
  "max_days_hospedaje": 45,
  "food_types": {
    "Perecedero": 40,
    "No Perecedero": 50,
    "Bebidas": 30
  }
}
```

## 📊 Contenido de los Reportes

### Reporte Semanal

- **Resumen Ejecutivo**: Estadísticas clave
- **Análisis de Personas**: Gráfica de personas por día
- **Análisis de Donaciones**: Gráfica por tipo de alimento
- **Análisis de Entregas**: Gráfica de entregas diarias
- **Top 10 Donadores**: Tabla de principales donantes
- **Detalle de Entregas**: Tabla con últimas 20 entregas

### Reporte Mensual

Todo lo del reporte semanal, más:
- **Tendencias Semanales**: Gráfica de entregas por semana
- **Distribución por Tipo**: Gráfica de pastel
- **Top Donadores del Mes**: Gráfica de barras
- **Estadísticas Detalladas**: Tabla con métricas avanzadas

## 🎨 Personalización

### Colores del Sistema

Los colores utilizan la paleta de iOS:
- Azul: `#007AFF` (Personas)
- Verde: `#34C759` (Disponible/Éxito)
- Naranja: `#FF9500` (Entregas)
- Rojo: `#FF3B30` (Alertas)
- Morado: `#AF52DE` (Tendencias)
- Cyan: `#5AC8FA` (Donadores)

### Modificar Estilos

Edita `services/report_generator.py` en el método `_setup_custom_styles()`.

## 🔧 Desarrollo

### Estructura del Proyecto

```
python_backend/
├── app.py                  # Aplicación Flask principal
├── requirements.txt        # Dependencias
├── .env.example           # Plantilla de variables
├── start.sh               # Script de inicio
├── services/
│   ├── __init__.py
│   ├── supabase_service.py    # Conexión a Supabase
│   └── report_generator.py    # Generación de PDFs
└── README.md
```

### Agregar Nuevos Endpoints

Edita `app.py` y agrega nuevas rutas:

```python
@app.route('/api/nuevo-endpoint', methods=['POST'])
def nuevo_endpoint():
    # Tu código aquí
    return jsonify({'message': 'Éxito'})
```

### Agregar Nuevas Gráficas

Edita `services/report_generator.py` y crea métodos como:

```python
def _create_custom_chart(self, data: List[Dict]) -> Image:
    # Tu código de matplotlib aquí
    return Image(img_buffer, width=6*inch, height=3*inch)
```

## 🐛 Troubleshooting

### Error: ModuleNotFoundError

Asegúrate de tener el entorno virtual activado:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Error: SUPABASE_URL not found

Verifica que el archivo `.env` existe y tiene las variables correctas.

### Error al generar PDFs

Verifica que matplotlib tiene el backend correcto:
```python
import matplotlib
matplotlib.use('Agg')
```

## 📦 Dependencias Principales

- **Flask**: Framework web
- **Flask-CORS**: Soporte para CORS
- **Supabase**: Cliente de Supabase
- **pandas**: Análisis de datos
- **matplotlib**: Gráficas
- **ReportLab**: Generación de PDFs
- **python-dotenv**: Variables de entorno

## 🚀 Deploy

### Opción 1: Railway

1. Conecta tu repositorio
2. Agrega variables de entorno
3. Deploy automático

### Opción 2: Heroku

```bash
heroku create shelter-control-backend
heroku config:set SUPABASE_URL=tu_url
heroku config:set SUPABASE_KEY=tu_key
git push heroku main
```

### Opción 3: Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 📄 Licencia

Parte del proyecto ShelterControl v1.0

## 👥 Soporte

Para problemas o preguntas:
- Email: soporte@sheltercontrol.com
- GitHub Issues: [crear issue]

---

**ShelterControl Backend** - Sistema de Gestión de Albergues

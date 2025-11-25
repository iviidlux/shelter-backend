"""
ShelterControl - Backend Python para Generación de Reportes PDF
Analiza datos y genera reportes con gráficas semanales
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import io

from services.supabase_service import SupabaseService
from services.report_generator import ReportGenerator

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Inicializar servicios
supabase_service = SupabaseService()
report_generator = ReportGenerator()

@app.route('/health', methods=['GET'])
def health_check():
    """Verificar estado del servidor"""
    return jsonify({
        'status': 'ok',
        'message': 'ShelterControl Backend is running',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/reports/weekly', methods=['POST'])
def generate_weekly_report():
    """
    Generar reporte semanal en PDF
    Body: {
        "start_date": "2025-11-18",
        "end_date": "2025-11-25",
        "shelter_name": "Albergue Central"
    }
    """
    try:
        data = request.get_json()
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        shelter_name = data.get('shelter_name', 'Albergue')
        
        # Si no se proporcionan fechas, usar última semana
        if not start_date or not end_date:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
        else:
            start_date = datetime.fromisoformat(start_date)
            end_date = datetime.fromisoformat(end_date)
        
        # Obtener datos de Supabase
        persons_data = supabase_service.get_persons_data(start_date, end_date)
        food_data = supabase_service.get_food_donations_data(start_date, end_date)
        deliveries_data = supabase_service.get_deliveries_data(start_date, end_date)
        
        # Generar PDF
        pdf_buffer = report_generator.generate_weekly_report(
            start_date=start_date,
            end_date=end_date,
            shelter_name=shelter_name,
            persons_data=persons_data,
            food_data=food_data,
            deliveries_data=deliveries_data
        )
        
        # Generar nombre de archivo
        filename = f"reporte_semanal_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error al generar el reporte'
        }), 500

@app.route('/api/reports/monthly', methods=['POST'])
def generate_monthly_report():
    """
    Generar reporte mensual en PDF
    Body: {
        "month": 11,
        "year": 2025,
        "shelter_name": "Albergue Central"
    }
    """
    try:
        data = request.get_json()
        month = data.get('month', datetime.now().month)
        year = data.get('year', datetime.now().year)
        shelter_name = data.get('shelter_name', 'Albergue')
        
        # Calcular fechas del mes
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Obtener datos
        persons_data = supabase_service.get_persons_data(start_date, end_date)
        food_data = supabase_service.get_food_donations_data(start_date, end_date)
        deliveries_data = supabase_service.get_deliveries_data(start_date, end_date)
        
        # Generar PDF
        pdf_buffer = report_generator.generate_monthly_report(
            month=month,
            year=year,
            shelter_name=shelter_name,
            persons_data=persons_data,
            food_data=food_data,
            deliveries_data=deliveries_data
        )
        
        filename = f"reporte_mensual_{year}_{month:02d}.pdf"
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error al generar el reporte mensual'
        }), 500

@app.route('/api/analytics/summary', methods=['POST'])
def get_analytics_summary():
    """
    Obtener resumen analítico sin generar PDF
    """
    try:
        data = request.get_json()
        start_date = datetime.fromisoformat(data.get('start_date'))
        end_date = datetime.fromisoformat(data.get('end_date'))
        
        # Obtener datos
        persons_data = supabase_service.get_persons_data(start_date, end_date)
        food_data = supabase_service.get_food_donations_data(start_date, end_date)
        deliveries_data = supabase_service.get_deliveries_data(start_date, end_date)
        
        # Calcular estadísticas
        summary = report_generator.calculate_statistics(
            persons_data, food_data, deliveries_data
        )
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'Error al obtener analíticas'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

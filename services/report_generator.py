"""
Generador de reportes PDF simplificado (sin pandas ni matplotlib)
"""

import io
from datetime import datetime, timedelta
from typing import List, Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from collections import Counter, defaultdict

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Configurar estilos personalizados"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#007AFF'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34C759'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=12,
            alignment=TA_LEFT
        ))
    
    def generate_weekly_report(self, start_date: datetime, end_date: datetime, 
                              shelter_name: str, persons_data: List[Dict],
                              food_data: List[Dict], deliveries_data: List[Dict]) -> io.BytesIO:
        """Generar reporte semanal completo en PDF"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        
        # Título
        title = f"Reporte Semanal - {shelter_name}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        
        # Período
        period = f"Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}"
        story.append(Paragraph(period, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Resumen Ejecutivo
        story.append(Paragraph("📊 Resumen Ejecutivo", self.styles['CustomSubtitle']))
        summary_stats = self._calculate_summary_stats(persons_data, food_data, deliveries_data)
        summary_table = self._create_summary_table(summary_stats)
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Análisis de Personas
        story.append(Paragraph("👥 Análisis de Personas Albergadas", self.styles['CustomSubtitle']))
        persons_table = self._create_persons_summary_table(persons_data)
        story.append(persons_table)
        story.append(Spacer(1, 20))
        
        # Análisis de Donaciones
        story.append(Paragraph("🍽️ Análisis de Donaciones de Alimentos", self.styles['CustomSubtitle']))
        food_table = self._create_food_summary_table(food_data)
        story.append(food_table)
        story.append(Spacer(1, 20))
        
        # Top Donadores
        story.append(Paragraph("⭐ Top 10 Donadores", self.styles['CustomSubtitle']))
        donors_table = self._create_top_donors_table(food_data)
        story.append(donors_table)
        story.append(Spacer(1, 20))
        
        # PageBreak
        story.append(PageBreak())
        
        # Análisis de Entregas
        story.append(Paragraph("📦 Análisis de Entregas", self.styles['CustomSubtitle']))
        deliveries_summary = self._create_deliveries_summary_table(deliveries_data)
        story.append(deliveries_summary)
        story.append(Spacer(1, 20))
        
        # Detalle de Entregas
        story.append(Paragraph("📋 Detalle de Entregas", self.styles['CustomSubtitle']))
        deliveries_table = self._create_deliveries_detail_table(deliveries_data)
        story.append(deliveries_table)
        
        # Pie de página
        story.append(Spacer(1, 30))
        footer = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')} | ShelterControl v1.0"
        story.append(Paragraph(footer, self.styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def generate_monthly_report(self, month: int, year: int, shelter_name: str,
                               persons_data: List[Dict], food_data: List[Dict],
                               deliveries_data: List[Dict]) -> io.BytesIO:
        """Generar reporte mensual"""
        
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        
        # Título
        month_names = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        title = f"Reporte Mensual - {shelter_name}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        
        period = f"{month_names[month-1]} {year}"
        story.append(Paragraph(period, self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Resumen mensual
        story.append(Paragraph("📊 Resumen del Mes", self.styles['CustomSubtitle']))
        summary_stats = self._calculate_summary_stats(persons_data, food_data, deliveries_data)
        summary_table = self._create_summary_table(summary_stats)
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Análisis de tendencias
        story.append(Paragraph("📈 Análisis de Tendencias", self.styles['CustomSubtitle']))
        trends_table = self._create_monthly_trends_table(persons_data, food_data, deliveries_data)
        story.append(trends_table)
        story.append(Spacer(1, 20))
        
        # Top Donadores del mes
        story.append(Paragraph("⭐ Top 10 Donadores del Mes", self.styles['CustomSubtitle']))
        donors_table = self._create_top_donors_table(food_data)
        story.append(donors_table)
        
        # Pie de página
        story.append(Spacer(1, 30))
        footer = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')} | ShelterControl v1.0"
        story.append(Paragraph(footer, self.styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _calculate_summary_stats(self, persons_data: List[Dict], 
                                 food_data: List[Dict], 
                                 deliveries_data: List[Dict]) -> Dict:
        """Calcular estadísticas resumidas"""
        
        # Personas activas
        active_persons = sum(1 for p in persons_data if p.get('is_active', False))
        total_persons = len(persons_data)
        
        # Donaciones
        total_donations = len(food_data)
        total_kg = sum(d.get('quantity_kg', 0) for d in food_data)
        
        # Entregas
        total_deliveries = len(deliveries_data)
        total_delivered_kg = sum(d.get('quantity_kg', 0) for d in deliveries_data)
        
        # Donadores únicos
        unique_donors = len(set(d.get('donor_name', '') for d in food_data if d.get('donor_name')))
        
        return {
            'active_persons': active_persons,
            'total_persons': total_persons,
            'total_donations': total_donations,
            'total_kg': total_kg,
            'total_deliveries': total_deliveries,
            'total_delivered_kg': total_delivered_kg,
            'unique_donors': unique_donors
        }
    
    def _create_summary_table(self, stats: Dict) -> Table:
        """Crear tabla de resumen"""
        data = [
            ['Métrica', 'Valor'],
            ['Personas Activas', f"{stats['active_persons']} / {stats['total_persons']}"],
            ['Total Donaciones', str(stats['total_donations'])],
            ['Kilos Donados', f"{stats['total_kg']:.2f} kg"],
            ['Total Entregas', str(stats['total_deliveries'])],
            ['Kilos Entregados', f"{stats['total_delivered_kg']:.2f} kg"],
            ['Donadores Únicos', str(stats['unique_donors'])]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007AFF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_persons_summary_table(self, persons_data: List[Dict]) -> Table:
        """Crear tabla resumen de personas"""
        active = sum(1 for p in persons_data if p.get('is_active', False))
        inactive = len(persons_data) - active
        
        data = [
            ['Estado', 'Cantidad', 'Porcentaje'],
            ['Activos', str(active), f"{(active/len(persons_data)*100):.1f}%" if persons_data else "0%"],
            ['Inactivos', str(inactive), f"{(inactive/len(persons_data)*100):.1f}%" if persons_data else "0%"],
            ['Total', str(len(persons_data)), "100%"]
        ]
        
        table = Table(data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34C759')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_food_summary_table(self, food_data: List[Dict]) -> Table:
        """Crear tabla resumen de donaciones"""
        
        # Agrupar por tipo de alimento
        food_types = defaultdict(lambda: {'count': 0, 'kg': 0.0})
        for donation in food_data:
            food_type = donation.get('food_type', 'Sin especificar')
            food_types[food_type]['count'] += 1
            food_types[food_type]['kg'] += donation.get('quantity_kg', 0)
        
        # Ordenar por kilos
        sorted_types = sorted(food_types.items(), key=lambda x: x[1]['kg'], reverse=True)
        
        data = [['Tipo de Alimento', 'Donaciones', 'Kilos']]
        for food_type, stats in sorted_types[:10]:  # Top 10
            data.append([
                food_type,
                str(stats['count']),
                f"{stats['kg']:.2f} kg"
            ])
        
        # Totales
        total_count = sum(ft['count'] for ft in food_types.values())
        total_kg = sum(ft['kg'] for ft in food_types.values())
        data.append(['TOTAL', str(total_count), f"{total_kg:.2f} kg"])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9500')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFD60A')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
        ]))
        
        return table
    
    def _create_top_donors_table(self, food_data: List[Dict]) -> Table:
        """Crear tabla de top donadores"""
        
        # Agrupar por donador
        donors = defaultdict(lambda: {'count': 0, 'kg': 0.0})
        for donation in food_data:
            donor = donation.get('donor_name', 'Anónimo')
            donors[donor]['count'] += 1
            donors[donor]['kg'] += donation.get('quantity_kg', 0)
        
        # Ordenar por kilos
        sorted_donors = sorted(donors.items(), key=lambda x: x[1]['kg'], reverse=True)
        
        data = [['Donador', 'Donaciones', 'Kilos Totales']]
        for donor, stats in sorted_donors[:10]:  # Top 10
            data.append([
                donor,
                str(stats['count']),
                f"{stats['kg']:.2f} kg"
            ])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF2D55')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_deliveries_summary_table(self, deliveries_data: List[Dict]) -> Table:
        """Crear tabla resumen de entregas"""
        
        # Agrupar por tipo de alimento
        food_types = defaultdict(lambda: {'count': 0, 'kg': 0.0})
        for delivery in deliveries_data:
            food_type = delivery.get('food_type', 'Sin especificar')
            food_types[food_type]['count'] += 1
            food_types[food_type]['kg'] += delivery.get('quantity_kg', 0)
        
        # Ordenar por cantidad
        sorted_types = sorted(food_types.items(), key=lambda x: x[1]['kg'], reverse=True)
        
        data = [['Tipo de Alimento', 'Entregas', 'Kilos']]
        for food_type, stats in sorted_types[:10]:
            data.append([
                food_type,
                str(stats['count']),
                f"{stats['kg']:.2f} kg"
            ])
        
        # Totales
        total_count = sum(ft['count'] for ft in food_types.values())
        total_kg = sum(ft['kg'] for ft in food_types.values())
        data.append(['TOTAL', str(total_count), f"{total_kg:.2f} kg"])
        
        table = Table(data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#5856D6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#AF52DE')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold')
        ]))
        
        return table
    
    def _create_deliveries_detail_table(self, deliveries_data: List[Dict]) -> Table:
        """Crear tabla detallada de entregas recientes"""
        
        # Ordenar por fecha (más recientes primero)
        sorted_deliveries = sorted(
            deliveries_data,
            key=lambda x: x.get('delivery_date', ''),
            reverse=True
        )[:20]  # Últimas 20 entregas
        
        data = [['Fecha', 'Persona', 'Alimento', 'Cantidad']]
        for delivery in sorted_deliveries:
            date_str = delivery.get('delivery_date', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    date_formatted = date_obj.strftime('%d/%m/%Y')
                except:
                    date_formatted = date_str[:10]
            else:
                date_formatted = 'N/A'
            
            data.append([
                date_formatted,
                delivery.get('person_name', 'N/A'),
                delivery.get('food_type', 'N/A'),
                f"{delivery.get('quantity_kg', 0):.2f} kg"
            ])
        
        table = Table(data, colWidths=[1.2*inch, 2*inch, 1.8*inch, 1.2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007AFF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_monthly_trends_table(self, persons_data: List[Dict],
                                    food_data: List[Dict],
                                    deliveries_data: List[Dict]) -> Table:
        """Crear tabla de tendencias mensuales"""
        
        # Agrupar entregas por día
        daily_deliveries = defaultdict(lambda: {'count': 0, 'kg': 0.0})
        for delivery in deliveries_data:
            date_str = delivery.get('delivery_date', '')
            if date_str:
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    day_key = date_obj.strftime('%d/%m')
                    daily_deliveries[day_key]['count'] += 1
                    daily_deliveries[day_key]['kg'] += delivery.get('quantity_kg', 0)
                except:
                    pass
        
        # Promedios
        avg_deliveries_per_day = len(deliveries_data) / max(len(daily_deliveries), 1)
        total_kg = sum(d['kg'] for d in daily_deliveries.values())
        avg_kg_per_day = total_kg / max(len(daily_deliveries), 1)
        
        data = [
            ['Métrica', 'Valor'],
            ['Promedio entregas/día', f"{avg_deliveries_per_day:.1f}"],
            ['Promedio kg/día', f"{avg_kg_per_day:.2f} kg"],
            ['Días con entregas', str(len(daily_deliveries))],
            ['Total donaciones', str(len(food_data))],
            ['Total entregas', str(len(deliveries_data))]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34C759')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table

"""
Generador de reportes PDF con gráficas y análisis
"""

import io
from datetime import datetime, timedelta
from typing import List, Dict, Any
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import matplotlib.dates as mdates

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        
    def _setup_custom_styles(self):
        """Configurar estilos personalizados"""
        # Título principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#007AFF'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtítulo
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34C759'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Texto normal
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
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
        
        # Gráfica de Personas
        story.append(Paragraph("👥 Análisis de Personas Albergadas", self.styles['CustomSubtitle']))
        persons_chart = self._create_persons_chart(persons_data, start_date, end_date)
        if persons_chart:
            story.append(persons_chart)
        story.append(Spacer(1, 20))
        
        # Gráfica de Donaciones
        story.append(Paragraph("🍽️ Análisis de Donaciones de Alimentos", self.styles['CustomSubtitle']))
        food_chart = self._create_food_donations_chart(food_data)
        if food_chart:
            story.append(food_chart)
        story.append(Spacer(1, 20))
        
        # PageBreak
        story.append(PageBreak())
        
        # Gráfica de Entregas
        story.append(Paragraph("📦 Análisis de Entregas", self.styles['CustomSubtitle']))
        deliveries_chart = self._create_deliveries_chart(deliveries_data, start_date, end_date)
        if deliveries_chart:
            story.append(deliveries_chart)
        story.append(Spacer(1, 20))
        
        # Top Donadores
        story.append(Paragraph("⭐ Top 10 Donadores", self.styles['CustomSubtitle']))
        donors_table = self._create_top_donors_table(food_data)
        story.append(donors_table)
        story.append(Spacer(1, 20))
        
        # Tabla de Entregas Detallada
        story.append(Paragraph("📋 Detalle de Entregas", self.styles['CustomSubtitle']))
        deliveries_table = self._create_deliveries_detail_table(deliveries_data)
        story.append(deliveries_table)
        
        # Pie de página
        story.append(Spacer(1, 30))
        footer = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')} | ShelterControl v1.0"
        story.append(Paragraph(footer, self.styles['Normal']))
        
        # Construir PDF
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
        
        # Tendencias por semana
        story.append(Paragraph("📈 Tendencias Semanales", self.styles['CustomSubtitle']))
        weekly_trends_chart = self._create_weekly_trends_chart(deliveries_data, start_date, end_date)
        if weekly_trends_chart:
            story.append(weekly_trends_chart)
        story.append(Spacer(1, 20))
        
        # Distribución por tipo de alimento
        story.append(Paragraph("🥘 Distribución por Tipo de Alimento", self.styles['CustomSubtitle']))
        food_types_chart = self._create_food_types_pie_chart(food_data)
        if food_types_chart:
            story.append(food_types_chart)
        
        story.append(PageBreak())
        
        # Comparativa de donadores
        story.append(Paragraph("👥 Top Donadores del Mes", self.styles['CustomSubtitle']))
        donors_chart = self._create_donors_bar_chart(food_data)
        if donors_chart:
            story.append(donors_chart)
        story.append(Spacer(1, 20))
        
        # Estadísticas detalladas
        story.append(Paragraph("📊 Estadísticas Detalladas", self.styles['CustomSubtitle']))
        detailed_stats = self._create_detailed_stats_table(persons_data, food_data, deliveries_data)
        story.append(detailed_stats)
        
        # Pie de página
        story.append(Spacer(1, 30))
        footer = f"Generado el: {datetime.now().strftime('%d/%m/%Y %H:%M')} | ShelterControl v1.0"
        story.append(Paragraph(footer, self.styles['Normal']))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _calculate_summary_stats(self, persons_data: List[Dict], 
                                 food_data: List[Dict], 
                                 deliveries_data: List[Dict]) -> Dict[str, Any]:
        """Calcular estadísticas de resumen"""
        return {
            'total_personas': len(persons_data),
            'personas_activas': len([p for p in persons_data if p.get('is_active', False)]),
            'total_donaciones': len(food_data),
            'total_entregas': len(deliveries_data),
            'alimentos_disponibles': len([f for f in food_data if not f.get('is_delivered', False)]),
            'total_donadores': len(set([f.get('donor_name', 'Anónimo') for f in food_data]))
        }
    
    def _create_summary_table(self, stats: Dict[str, Any]) -> Table:
        """Crear tabla de resumen"""
        data = [
            ['Métrica', 'Valor'],
            ['Total de Personas Registradas', str(stats['total_personas'])],
            ['Personas Activas', str(stats['personas_activas'])],
            ['Total de Donaciones', str(stats['total_donaciones'])],
            ['Alimentos Disponibles', str(stats['alimentos_disponibles'])],
            ['Total de Entregas', str(stats['total_entregas'])],
            ['Donadores Únicos', str(stats['total_donadores'])]
        ]
        
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007AFF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_persons_chart(self, persons_data: List[Dict], 
                             start_date: datetime, end_date: datetime) -> Image:
        """Crear gráfica de personas por día"""
        if not persons_data:
            return None
        
        # Crear DataFrame
        df = pd.DataFrame(persons_data)
        df['entry_date'] = pd.to_datetime(df['entry_date'])
        
        # Contar personas por día
        daily_counts = df.groupby(df['entry_date'].dt.date).size()
        
        # Crear gráfica
        fig, ax = plt.subplots(figsize=(8, 4))
        daily_counts.plot(kind='bar', color='#007AFF', ax=ax)
        ax.set_title('Personas Registradas por Día', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=11)
        ax.set_ylabel('Cantidad', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Guardar en buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=6*inch, height=3*inch)
    
    def _create_food_donations_chart(self, food_data: List[Dict]) -> Image:
        """Crear gráfica de donaciones por tipo"""
        if not food_data:
            return None
        
        df = pd.DataFrame(food_data)
        type_counts = df['food_type'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        colors_map = ['#007AFF', '#34C759', '#FF9500', '#FF3B30', '#AF52DE', '#5AC8FA']
        type_counts.plot(kind='barh', color=colors_map[:len(type_counts)], ax=ax)
        ax.set_title('Donaciones por Tipo de Alimento', fontsize=14, fontweight='bold')
        ax.set_xlabel('Cantidad', fontsize=11)
        ax.set_ylabel('Tipo', fontsize=11)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=6*inch, height=3*inch)
    
    def _create_deliveries_chart(self, deliveries_data: List[Dict],
                                start_date: datetime, end_date: datetime) -> Image:
        """Crear gráfica de entregas por día"""
        if not deliveries_data:
            return None
        
        df = pd.DataFrame(deliveries_data)
        df['delivery_date'] = pd.to_datetime(df['delivery_date'])
        
        daily_deliveries = df.groupby(df['delivery_date'].dt.date).size()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        daily_deliveries.plot(kind='line', marker='o', color='#34C759', linewidth=2, ax=ax)
        ax.set_title('Entregas Realizadas por Día', fontsize=14, fontweight='bold')
        ax.set_xlabel('Fecha', fontsize=11)
        ax.set_ylabel('Cantidad de Entregas', fontsize=11)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=6*inch, height=3*inch)
    
    def _create_top_donors_table(self, food_data: List[Dict]) -> Table:
        """Crear tabla de top donadores"""
        if not food_data:
            data = [['Donador', 'Cantidad de Donaciones'], ['No hay datos', '0']]
        else:
            df = pd.DataFrame(food_data)
            top_donors = df['donor_name'].value_counts().head(10)
            
            data = [['Donador', 'Cantidad de Donaciones']]
            for donor, count in top_donors.items():
                data.append([donor, str(count)])
        
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34C759')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_deliveries_detail_table(self, deliveries_data: List[Dict]) -> Table:
        """Crear tabla detallada de entregas"""
        if not deliveries_data:
            data = [['Fecha', 'Alimento', 'Persona', 'Cantidad'], 
                   ['No hay entregas registradas', '-', '-', '-']]
        else:
            data = [['Fecha', 'Alimento', 'Persona', 'Cantidad']]
            for delivery in deliveries_data[:20]:  # Limitar a 20 entregas
                date = datetime.fromisoformat(delivery['delivery_date'].replace('Z', '+00:00'))
                food_name = delivery.get('food_donations', {}).get('food_name', 'N/A')
                person_name = delivery.get('sheltered_persons', {}).get('full_name', 'N/A')
                quantity = f"{delivery.get('quantity', 0)} {delivery.get('unit', '')}"
                
                data.append([
                    date.strftime('%d/%m/%Y'),
                    food_name[:30],
                    person_name[:30],
                    quantity
                ])
        
        table = Table(data, colWidths=[1.2*inch, 2.5*inch, 2*inch, 1*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9500')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def _create_weekly_trends_chart(self, deliveries_data: List[Dict],
                                   start_date: datetime, end_date: datetime) -> Image:
        """Crear gráfica de tendencias semanales"""
        if not deliveries_data:
            return None
        
        df = pd.DataFrame(deliveries_data)
        df['delivery_date'] = pd.to_datetime(df['delivery_date'])
        df['week'] = df['delivery_date'].dt.isocalendar().week
        
        weekly_counts = df.groupby('week').size()
        
        fig, ax = plt.subplots(figsize=(8, 4))
        weekly_counts.plot(kind='bar', color='#AF52DE', ax=ax)
        ax.set_title('Entregas por Semana', fontsize=14, fontweight='bold')
        ax.set_xlabel('Semana del Año', fontsize=11)
        ax.set_ylabel('Cantidad', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=6*inch, height=3*inch)
    
    def _create_food_types_pie_chart(self, food_data: List[Dict]) -> Image:
        """Crear gráfica de pastel de tipos de alimento"""
        if not food_data:
            return None
        
        df = pd.DataFrame(food_data)
        type_counts = df['food_type'].value_counts()
        
        fig, ax = plt.subplots(figsize=(6, 6))
        colors_map = ['#007AFF', '#34C759', '#FF9500', '#FF3B30', '#AF52DE', '#5AC8FA']
        ax.pie(type_counts.values, labels=type_counts.index, autopct='%1.1f%%',
               colors=colors_map[:len(type_counts)], startangle=90)
        ax.set_title('Distribución por Tipo de Alimento', fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=5*inch, height=5*inch)
    
    def _create_donors_bar_chart(self, food_data: List[Dict]) -> Image:
        """Crear gráfica de barras de donadores"""
        if not food_data:
            return None
        
        df = pd.DataFrame(food_data)
        top_donors = df['donor_name'].value_counts().head(10)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        top_donors.plot(kind='barh', color='#5AC8FA', ax=ax)
        ax.set_title('Top 10 Donadores', fontsize=14, fontweight='bold')
        ax.set_xlabel('Cantidad de Donaciones', fontsize=11)
        ax.set_ylabel('Donador', fontsize=11)
        ax.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        return Image(img_buffer, width=6*inch, height=4*inch)
    
    def _create_detailed_stats_table(self, persons_data: List[Dict],
                                    food_data: List[Dict],
                                    deliveries_data: List[Dict]) -> Table:
        """Crear tabla de estadísticas detalladas"""
        
        # Calcular estadísticas avanzadas
        avg_days = 0
        if persons_data:
            df_persons = pd.DataFrame(persons_data)
            df_persons['entry_date'] = pd.to_datetime(df_persons['entry_date'])
            df_persons['days'] = (datetime.now() - df_persons['entry_date']).dt.days
            avg_days = df_persons['days'].mean()
        
        total_quantity = 0
        if deliveries_data:
            total_quantity = sum([d.get('quantity', 0) for d in deliveries_data])
        
        avg_deliveries_per_day = 0
        if deliveries_data:
            df_del = pd.DataFrame(deliveries_data)
            df_del['delivery_date'] = pd.to_datetime(df_del['delivery_date'])
            days_with_deliveries = df_del['delivery_date'].dt.date.nunique()
            avg_deliveries_per_day = len(deliveries_data) / max(days_with_deliveries, 1)
        
        data = [
            ['Estadística', 'Valor'],
            ['Promedio de Días de Hospedaje', f'{avg_days:.1f} días'],
            ['Cantidad Total Entregada', f'{total_quantity:.1f} unidades'],
            ['Promedio de Entregas por Día', f'{avg_deliveries_per_day:.1f}'],
            ['Tipos de Alimentos Diferentes', str(len(set([f.get('food_type', '') for f in food_data])))],
            ['Tasa de Entrega', f'{(len(deliveries_data)/max(len(food_data), 1)*100):.1f}%']
        ]
        
        table = Table(data, colWidths=[4*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF3B30')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        return table
    
    def calculate_statistics(self, persons_data: List[Dict],
                           food_data: List[Dict],
                           deliveries_data: List[Dict]) -> Dict[str, Any]:
        """Calcular todas las estadísticas"""
        stats = self._calculate_summary_stats(persons_data, food_data, deliveries_data)
        
        # Agregar estadísticas adicionales
        if persons_data:
            df = pd.DataFrame(persons_data)
            df['entry_date'] = pd.to_datetime(df['entry_date'])
            df['days'] = (datetime.now() - df['entry_date']).dt.days
            stats['avg_days_hospedaje'] = float(df['days'].mean())
            stats['max_days_hospedaje'] = int(df['days'].max())
        
        if food_data:
            df = pd.DataFrame(food_data)
            stats['food_types'] = df['food_type'].value_counts().to_dict()
        
        if deliveries_data:
            df = pd.DataFrame(deliveries_data)
            stats['total_quantity_delivered'] = sum([d.get('quantity', 0) for d in deliveries_data])
        
        return stats

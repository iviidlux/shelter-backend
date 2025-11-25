"""
Servicio para conectar con Supabase y obtener datos
"""

import os
from supabase import create_client, Client
from datetime import datetime
from typing import List, Dict, Any

class SupabaseService:
    def __init__(self):
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar configurados en .env")
        
        self.client: Client = create_client(url, key)
    
    def get_persons_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Obtener datos de personas en el rango de fechas"""
        try:
            response = self.client.table('sheltered_persons').select('*').execute()
            
            # Filtrar por fecha de ingreso
            filtered_data = []
            for person in response.data:
                entry_date = datetime.fromisoformat(person['entry_date'].replace('Z', '+00:00'))
                if start_date <= entry_date <= end_date:
                    filtered_data.append(person)
            
            return filtered_data
        except Exception as e:
            print(f"Error al obtener personas: {e}")
            return []
    
    def get_food_donations_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Obtener datos de donaciones de alimentos"""
        try:
            response = self.client.table('food_donations').select('*').execute()
            
            filtered_data = []
            for donation in response.data:
                donation_date = datetime.fromisoformat(donation['donation_date'].replace('Z', '+00:00'))
                if start_date <= donation_date <= end_date:
                    filtered_data.append(donation)
            
            return filtered_data
        except Exception as e:
            print(f"Error al obtener donaciones: {e}")
            return []
    
    def get_deliveries_data(self, start_date: datetime, end_date: datetime) -> List[Dict[str, Any]]:
        """Obtener datos de entregas"""
        try:
            response = self.client.table('food_deliveries').select('''
                *,
                food_donations(*),
                sheltered_persons(*),
                employees(*)
            ''').execute()
            
            filtered_data = []
            for delivery in response.data:
                delivery_date = datetime.fromisoformat(delivery['delivery_date'].replace('Z', '+00:00'))
                if start_date <= delivery_date <= end_date:
                    filtered_data.append(delivery)
            
            return filtered_data
        except Exception as e:
            print(f"Error al obtener entregas: {e}")
            return []
    
    def get_all_active_persons(self) -> int:
        """Obtener total de personas activas"""
        try:
            response = self.client.table('sheltered_persons')\
                .select('id', count='exact')\
                .eq('is_active', True)\
                .execute()
            return response.count or 0
        except Exception as e:
            print(f"Error al obtener personas activas: {e}")
            return 0
    
    def get_available_food_count(self) -> int:
        """Obtener total de alimentos disponibles"""
        try:
            response = self.client.table('food_donations')\
                .select('id', count='exact')\
                .eq('is_delivered', False)\
                .execute()
            return response.count or 0
        except Exception as e:
            print(f"Error al obtener alimentos disponibles: {e}")
            return 0

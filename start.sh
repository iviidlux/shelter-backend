#!/bin/bash

# Script para iniciar el backend de Python

echo "🚀 Iniciando Backend de ShelterControl..."

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 no está instalado. Por favor instálalo primero."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Verificar que existe el archivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Archivo .env no encontrado. Copia .env.example a .env y configura tus credenciales."
    echo "cp .env.example .env"
    exit 1
fi

# Iniciar servidor
echo "✅ Iniciando servidor Flask..."
python app.py

#!/bin/bash

# Script para iniciar Airflow rápidamente

echo "🚀 Iniciando Airflow..."

# Verificar si Docker está ejecutándose
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está ejecutándose. Por favor, inicia Docker Desktop."
    exit 1
fi

# Verificar si los contenedores ya están ejecutándose
if docker-compose ps | grep -q "Up"; then
    echo "⚠️  Airflow ya está ejecutándose."
    echo "Para reiniciar, ejecuta: docker-compose restart"
    echo "Para detener, ejecuta: docker-compose down"
    exit 0
fi

# Iniciar servicios
echo "🔧 Iniciando servicios de Airflow..."
docker-compose up -d

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "✅ Airflow iniciado exitosamente!"
echo ""
echo "🌐 Acceso a la interfaz web:"
echo "   URL: http://localhost:8080"
echo "   Usuario: airflow"
echo "   Contraseña: airflow"
echo ""
echo "📋 Comandos útiles:"
echo "   Ver logs: docker-compose logs -f"
echo "   Detener: docker-compose down"
echo "   Reiniciar: docker-compose restart"
echo ""
echo "🎯 Para ejecutar el pipeline:"
echo "   1. Ve a http://localhost:8080"
echo "   2. Busca el DAG 'kedro_ml_pipeline'"
echo "   3. Actívalo y ejecútalo"

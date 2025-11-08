#!/bin/bash

# Script para inicializar Airflow con Docker Compose

echo "🚀 Inicializando Airflow con Docker Compose..."

# Crear directorios necesarios
mkdir -p logs dags plugins data

# Establecer permisos correctos
echo "📁 Configurando permisos de directorios..."
sudo chown -R 50000:0 logs dags plugins data

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cat > .env << EOF
# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW_GID=0
AIRFLOW_PROJ_DIR=.

# Airflow User
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow

# Database Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow

# Kedro Configuration
KEDRO_CONFIG_FILE=conf/local/credentials.yml
EOF
fi

# Inicializar Airflow
echo "🔧 Inicializando base de datos de Airflow..."
docker-compose up airflow-init

echo "✅ Inicialización completada!"
echo ""
echo "Para iniciar Airflow, ejecuta:"
echo "  docker-compose up -d"
echo ""
echo "Para ver los logs:"
echo "  docker-compose logs -f"
echo ""
echo "Para detener Airflow:"
echo "  docker-compose down"
echo ""
echo "Acceso a la interfaz web: http://localhost:8080"
echo "Usuario: airflow"
echo "Contraseña: airflow"

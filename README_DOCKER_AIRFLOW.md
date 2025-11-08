# 🚀 Proyecto Kedro con Airflow y Docker

Este proyecto integra Kedro con Apache Airflow usando Docker para crear un pipeline completo de Machine Learning.

## 📋 Requisitos Previos

- Docker Desktop instalado y ejecutándose
- Docker Compose v2.0+
- Al menos 4GB de RAM disponible
- Al menos 10GB de espacio en disco

## 🛠️ Instalación y Configuración

### 1. Clonar y configurar el proyecto

```bash
# Navegar al directorio del proyecto
cd analisis

# Hacer ejecutable el script de inicialización
chmod +x init_airflow.sh

# Ejecutar script de inicialización
./init_airflow.sh
```

### 2. Iniciar Airflow

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f airflow-webserver
```

### 3. Acceder a la interfaz web

- **URL**: http://localhost:8080
- **Usuario**: `airflow`
- **Contraseña**: `airflow`

## 📊 Estructura del Pipeline

El DAG `kedro_ml_pipeline` incluye las siguientes tareas:

1. **Validaciones Previas**
   - Verificación de disponibilidad de datos
   - Validación de instalación de Kedro

2. **Ingestion de Datos** (`data_ingestion`)
   - Carga de datos de compra y venta
   - Validación de formato

3. **Procesamiento de Datos** (`data_processing`)
   - Limpieza y normalización
   - Extracción de características

4. **Análisis Exploratorio** (`data_analysis`)
   - Generación de visualizaciones
   - Estadísticas descriptivas

5. **Modelos de Clasificación** (`modelos_clasificacion`)
   - Entrenamiento de modelos de clasificación
   - Evaluación y métricas

6. **Modelos de Regresión** (`modelos_regresion`)
   - Entrenamiento de modelos de regresión
   - Evaluación y métricas

## 🐳 Comandos Docker Útiles

### Gestión de contenedores

```bash
# Ver estado de contenedores
docker-compose ps

# Detener todos los servicios
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Reconstruir imágenes
docker-compose build --no-cache

# Ejecutar comando en contenedor
docker-compose exec airflow-webserver bash
```

### Logs y debugging

```bash
# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs airflow-scheduler

# Seguir logs en tiempo real
docker-compose logs -f airflow-webserver
```

### Limpieza

```bash
# Limpiar contenedores parados
docker-compose rm

# Limpiar imágenes no utilizadas
docker image prune

# Limpiar todo (¡CUIDADO!)
docker system prune -a
```

## 🔧 Configuración Avanzada

### Variables de entorno

Edita el archivo `.env` para personalizar la configuración:

```env
# Airflow Configuration
AIRFLOW_UID=50000
AIRFLOW_GID=0

# Airflow User
_AIRFLOW_WWW_USER_USERNAME=airflow
_AIRFLOW_WWW_USER_PASSWORD=airflow

# Database Configuration
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
POSTGRES_DB=airflow
```

### Personalizar DAGs

Los DAGs se encuentran en el directorio `dags/`. Para agregar nuevos DAGs:

1. Crea el archivo Python en `dags/`
2. Reinicia Airflow: `docker-compose restart airflow-webserver`

### Acceso a datos

Los datos se montan en `/opt/airflow/data` dentro del contenedor. Para acceder desde el host:

```bash
# Copiar datos al contenedor
docker cp data/ airflow-webserver:/opt/airflow/data/

# Copiar datos del contenedor
docker cp airflow-webserver:/opt/airflow/data/ ./data/
```

## 🚨 Solución de Problemas

### Error de permisos

```bash
# Establecer permisos correctos
sudo chown -R 50000:0 logs dags plugins data
```

### Puerto ya en uso

```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "8081:8080"  # Usar puerto 8081 en lugar de 8080
```

### Problemas de memoria

- Aumentar memoria disponible para Docker
- Reducir el número de workers en `docker-compose.yml`

### DAG no aparece

1. Verificar sintaxis del DAG
2. Revisar logs: `docker-compose logs airflow-scheduler`
3. Reiniciar scheduler: `docker-compose restart airflow-scheduler`

## 📈 Monitoreo

### Flower (opcional)

Para monitorear tareas de Celery:

```bash
# Iniciar Flower
docker-compose --profile flower up -d

# Acceder a Flower
# URL: http://localhost:5555
```

### Métricas de Airflow

- **Web UI**: http://localhost:8080
- **API**: http://localhost:8080/api/v1/
- **Health Check**: http://localhost:8080/health

## 🔄 Flujo de Trabajo

1. **Desarrollo**: Modifica código en el host
2. **Testing**: Ejecuta DAGs desde la interfaz web
3. **Producción**: Programa ejecuciones automáticas
4. **Monitoreo**: Revisa logs y métricas

## 📚 Recursos Adicionales

- [Documentación de Airflow](https://airflow.apache.org/docs/)
- [Documentación de Kedro](https://docs.kedro.org/)
- [Docker Compose Reference](https://docs.docker.com/compose/)

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

#!/usr/bin/env python3
"""
Script de validación para verificar que el proyecto Kedro con Airflow esté correctamente configurado.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verificar versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Se requiere Python 3.9+")
        return False

def check_docker():
    """Verificar que Docker esté instalado y ejecutándose"""
    print("🐳 Verificando Docker...")
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker instalado: {result.stdout.strip()}")
            
            # Verificar que Docker esté ejecutándose
            result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
            if result.returncode == 0:
                print("✅ Docker está ejecutándose")
                return True
            else:
                print("❌ Docker no está ejecutándose")
                return False
        else:
            print("❌ Docker no está instalado")
            return False
    except FileNotFoundError:
        print("❌ Docker no está instalado")
        return False

def check_docker_compose():
    """Verificar Docker Compose"""
    print("🐙 Verificando Docker Compose...")
    try:
        result = subprocess.run(['docker-compose', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Docker Compose: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker Compose no está disponible")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose no está instalado")
        return False

def check_kedro():
    """Verificar instalación de Kedro"""
    print("🔧 Verificando Kedro...")
    try:
        result = subprocess.run([sys.executable, '-m', 'kedro', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Kedro: {result.stdout.strip()}")
            return True
        else:
            print("❌ Kedro no está instalado")
            return False
    except Exception as e:
        print(f"❌ Error verificando Kedro: {e}")
        return False

def check_project_structure():
    """Verificar estructura del proyecto"""
    print("📁 Verificando estructura del proyecto...")
    
    required_files = [
        'pyproject.toml',
        'requirements.txt',
        'Dockerfile',
        'Dockerfile.airflow',
        'docker-compose.yml',
        'dags/kedro_pipelines_dag.py',
        'src/analisis/pipeline_registry.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Estructura del proyecto - OK")
        return True

def check_data_files():
    """Verificar archivos de datos"""
    print("📊 Verificando archivos de datos...")
    
    data_dir = Path('data/01_raw')
    required_data_files = ['matriz-compra.csv', 'matriz-venta.csv']
    
    if not data_dir.exists():
        print(f"❌ Directorio de datos no encontrado: {data_dir}")
        return False
    
    missing_data = []
    for file in required_data_files:
        if not (data_dir / file).exists():
            missing_data.append(file)
    
    if missing_data:
        print("❌ Archivos de datos faltantes:")
        for file in missing_data:
            print(f"   - data/01_raw/{file}")
        return False
    else:
        print("✅ Archivos de datos - OK")
        return True

def check_airflow_dag():
    """Verificar sintaxis del DAG de Airflow"""
    print("🔄 Verificando DAG de Airflow...")
    
    dag_file = Path('dags/kedro_pipelines_dag.py')
    if not dag_file.exists():
        print("❌ Archivo DAG no encontrado")
        return False
    
    try:
        # Verificar sintaxis básica del archivo Python
        with open(dag_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Compilar el código para verificar sintaxis
        compile(content, str(dag_file), 'exec')
        
        # Verificar que contenga elementos básicos de Airflow
        if 'from airflow import DAG' in content and 'BashOperator' in content:
            print("✅ DAG de Airflow - OK")
            return True
        else:
            print("❌ DAG no contiene elementos básicos de Airflow")
            return False
            
    except SyntaxError as e:
        print(f"❌ Error de sintaxis en DAG: {e}")
        return False
    except Exception as e:
        print(f"❌ Error verificando DAG: {e}")
        return False

def main():
    """Función principal de validación"""
    print("🚀 Validando configuración del proyecto Kedro con Airflow...")
    print("=" * 60)
    
    checks = [
        check_python_version,
        check_docker,
        check_docker_compose,
        check_kedro,
        check_project_structure,
        check_data_files,
        check_airflow_dag
    ]
    
    results = []
    for check in checks:
        results.append(check())
        print()
    
    print("=" * 60)
    print("📋 RESUMEN DE VALIDACIÓN")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ Todas las validaciones pasaron ({passed}/{total})")
        print()
        print("🎉 ¡El proyecto está listo para usar!")
        print()
        print("Para iniciar Airflow:")
        print("  ./start_airflow.sh")
        print()
        print("Para inicializar por primera vez:")
        print("  ./init_airflow.sh")
        return True
    else:
        print(f"❌ {total - passed} validaciones fallaron ({passed}/{total})")
        print()
        print("🔧 Por favor, corrige los errores antes de continuar.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

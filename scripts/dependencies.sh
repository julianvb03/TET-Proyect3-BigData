#!/bin/bash

# ============================================
# Instala dependencias necesarias para la ejecución del step de analitica
# ============================================


echo "Installing numpy..."
pip install numpy==2.0.2

echo "Installing setuptools (distutils)..."
pip install setuptools==59.6.0

echo "Installing boto3 ..."
pip install boto3==1.38.22

# Verificar instalaciones
echo "Verifying installations..."
python3 -c "import numpy; print(f'NumPy version: {numpy.__version__}')"
python3 -c "import distutils; print('distutils imported successfully')"
python3 -c "import boto3; print(f'boto3 version: se importo bien')"

# Configurar variables de entorno para Spark
# echo "export PYSPARK_PYTHON=python3" | sudo tee -a /etc/environment
# echo "export PYSPARK_DRIVER_PYTHON=python3" | sudo tee -a /etc/environment

echo "Script completed successfully!"
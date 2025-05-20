# Proyecto 3 – Arquitectura Batch para Big Data (ST0263 - EAFIT)

## General Description
This project implements a big data example that automates the complete process of capturing, ingesting, processing, and outputting actionable data using AWS services.

## Architecture


# Tasks
### Configuración inicial
- [ ] Crear buckets S3: Zonificado (Raw, Trusted y Refined)

### Captura e ingesta de datos
- [ ] Desarrollar script de descarga de datos desde URL/archivos de sobre el covid-19
- [ ] Desarrollar script de consumo de API de XXX
- [ ] Implementar base de datos relacional (MySQL/PostgreSQL en RDS)
- [ ] Crear script de extracción de datos de la base de datos relacional
- [ ] Automatizar ingesta a S3 Raw usando Lambda y EventBridge
- [ ] Implementar verificación de duplicados en la zona Raw

### Procesamiento ETL
- [ ] Desarrollar scripts PySpark para limpieza y unión de datos
- [ ] Automatizar creación de clúster EMR (CLI/CloudFormation)
- [ ] Configurar Steps de EMR para ejecución automática de ETL
- [ ] Definir estructura de almacenamiento en S3 Trusted

### Análisis y analítica avanzada
- [ ] Implementar scripts de análisis descriptivo con SparkSQL
- [ ] Desarrollar pipeline de ML con SparkML
- [ ] Configurar Steps de EMR para análisis y almacenamiento en S3 Refined
- [ ] Definir dependencias entre Steps ETL y analítica

### Acceso y visualización
- [ ] Configurar AWS Athena para consultas en S3 Refined
- [ ] Crear API Gateway con backend Lambda para acceso programático
- [ ] Desarrollar notebook Jupyter para demostración de consultas
- [ ] Implementar cliente de prueba para la API

### Orquestación y automatización
- [ ] Integrar flujo completo con AWS Step Functions
- [ ] Programar ejecuciones periódicas usando EventBridge
- [ ] Configurar alertas y monitoreo con CloudWatch
- [ ] Crear dashboard de monitoreo en AWS
---

## Repository Structure

```
/
├── docs/                 # Additional documentation
├── scripts/
│   ├── ingestion/        # Data ingestion scripts
│   ├── etl/              # ETL transformation scripts
│   ├── analytics/        # Analysis and ML scripts
│   └── deployment/       # Deployment scripts
├── infrastructure/       # Infrastructure definitions (CloudFormation, etc.)
├── api/                  # API Gateway code
├── notebooks/            # Jupyter notebooks for examples
├── tests/                # Automated tests
└── README.md
```

---

# Configuraciones

## 📂 Requisitos
- Python 3.12.0
- Paquetes:
  - `pandas`
  - `requests`

## :floppy_disk: Bucket S3

Se creó un bucket en S3 con el siguiente nombre:

```text
st0263-proyecto3
```

### Estructura esperada:
```plaintext
s3://st0263-proyecto3/
├── raw/
│   ├── covid/
│   │   └── covid_YYYYMMDD_HHMMSS.csv
```

> ⚠️ Debido a restricciones de AWS Academy (sin acceso a IAM), el bucket tiene habilitado el acceso público limitado a `s3:PutObject` mediante una política de bucket.

---

## ⚙️ Configuración de permisos (AWS Academy)

Debido a las restricciones de IAM en AWS Academy:

- El bucket tiene la política pública **temporal** para permitir `PutObject`:

```json
{
  "Effect": "Allow",
  "Principal": "*",
  "Action": "s3:PutObject",
  "Resource": "arn:aws:s3:::st0263-proyecto3/*"
}

```
En general se expondran de manera pública todos los recursos, para simplificar el despliegue y hacer enfasis en la creación de la infraestrutura y servicios necesarios.

## Usage

---
## Authors
**Nombres:** 
	- Juan Felipe Restrepo Buitrago
	- Kevin Quiroz González
	- Julian Estiven Valencia Bolaños
	- Julian Agudelo Cifuentes
**Curso:** ST0263 - Tópicos Especiales en Telemática  
**Universidad:** EAFIT  
**Periodo:** 2025-1
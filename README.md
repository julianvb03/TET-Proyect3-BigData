# Project 3 – Batch Architecture for Big Data (ST0263 - EAFIT)

## 🧠 General Overview
This project showcases a complete batch data processing pipeline using AWS services. It automates the capture, ingestion, transformation, analysis, and visualization of COVID-19 data.

---

## 🏗️ Architecture Diagram

```mermaid
graph TD
    Client[("Client A<br>Accesses COVID-19 Data")]:::client
    subgraph AWS_Academy[AWS Academy]
        Athena{{"Athena / API Gateway<br>Processed Data Access"}}:::awsService
        CloudWatch["CloudWatch<br>Triggers Scheduled Jobs"]:::awsService
        S3[("S3 BigData Bucket<br>Raw, Trusted, Refined")]:::awsStorage
        subgraph Lambda[AWS Lambda]
            ShowResults["Show Results<br>Returns Processed Data"]:::lambda
            IngestData["Ingest Data<br>From External Sources"]:::lambda
            CreateEMR["Create EMR<br>Launch and Configure Cluster"]:::lambda
        end
        subgraph EMR[AWS EMR]
            Steps["Steps<br>ETL, SparkSQL, ML"]:::emr
        end

        ExternalDB[("External DB<br>Simulated DB")]:::external
    end
    ArchivoCSV["CSV File<br>COVID-19 Dataset"]:::external

    Client -->|Queries| Athena
    Athena -->|Displays| ShowResults
    IngestData -->|Stores Raw| S3
    Steps -->|Stores Trusted/Refined| S3
    CloudWatch -->|Triggers| IngestData
    IngestData -->|Invokes| CreateEMR
    CreateEMR -->|Starts| EMR
    IngestData -->|Pulls from| ArchivoCSV
    IngestData -->|Pulls from| ExternalDB

    %% Estilos mejorados
    classDef client fill:#E9D5FF,stroke:#6B21A8,stroke-width:2px,color:#1E1B4B;
    classDef awsService fill:#FACC15,stroke:#92400E,stroke-width:2px,color:#1E1B4B;
    classDef awsStorage fill:#34D399,stroke:#065F46,stroke-width:2px,color:#1E1B4B;
    classDef lambda fill:#FBBF24,stroke:#92400E,stroke-width:2px,color:#1E1B4B;
    classDef emr fill:#60A5FA,stroke:#1E3A8A,stroke-width:2px,color:#1E1B4B;
    classDef external fill:#F87171,stroke:#991B1B,stroke-width:2px,color:#1E1B4B;

```

---

## ✅ Task Checklist

### 📦 Initial Setup
- [ ] Create an S3 bucket with zones: Raw, Trusted, and Refined.

### 🔽 Capture & Ingestion
- [ ] Script to download COVID-19 data.
- [ ] Set up PostgreSQL (RDS) and import CSV.
- [ ] Extract data from DB into S3 Raw using Lambda.
- [ ] Add duplicate check in Raw zone.

### ⚙️ ETL Processing
- [ ] Clean and join data with PySpark.
- [ ] Launch EMR via CLI or Lambda.
- [ ] Define and run EMR steps.
- [ ] Organize data into S3 Trusted zone.

### 📊 Advanced Analytics
- [ ] Use SparkSQL for descriptive statistics.
- [ ] Train models using SparkML.
- [ ] Save analytics output in S3 Refined zone.
- [ ] Link ETL and ML steps in EMR.

### 📈 Visualization & API Access
- [ ] Set up Athena for querying S3.
- [ ] Create Lambda-backed API Gateway.
- [ ] Test API with Postman.

### 🔁 Automation & Monitoring
- [ ] Use AWS Step Functions to orchestrate.
- [ ] Schedule runs with EventBridge.
- [ ] Monitor using CloudWatch.
- [ ] Build dashboard for observability.

---

## 🔧 Setup Instructions

### S3 Bucket Configuration
Follow instructions to create the S3 bucket and attach the required bucket policy (see original version).

### PostgreSQL RDS Setup
1. Create DB named `covid_data`.
2. Upload `country_data.csv` into the DB.

### Lambda Ingestion
Set up a Lambda function with the code in `scripts/data_insertion.py`, update environment variables, attach the layer (`ingestion_layer.zip`) and set a CloudWatch trigger.

### EMR Lambda Setup
Configure a Lambda using `scripts/emr_creation.py`, adjust IAM roles and bucket names.

### EMR Scripts Upload
Create a `scripts/` folder in S3. Upload:
- `ETL.py` (edit bucket name)
- `dependencies.sh`
- `Analytics-EMR.py`

### Athena Setup
Create database and tables using provided SQL scripts. Set `athena_results/` as query output.

### Lambda for Results
Create `show_results.py` Lambda to fetch Athena results based on table names.

### API Gateway Integration
Expose the `showResults` Lambda via HTTP POST route `/showResults`. Test using Postman.

---

## 👥 Authors
- **Juan Felipe Restrepo Buitrago**
- **Kevin Quiroz González**
- **Julian Estiven Valencia Bolaños**
- **Julian Agudelo Cifuentes**

**Course:** ST0263 – Special Topics in Telematics  
**University:** EAFIT  
**Term:** 2025-1

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg, max, desc, sum, stddev, corr
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.clustering import KMeans
from pyspark.ml import Pipeline
import sys
import argparse
import traceback

def Analytics(data_source: str, output_uri: str) -> None:
    try:
        with SparkSession.builder.appName("COVID_Analytics_EMR").getOrCreate() as spark:

            # Cargar datos
            print(f"Leyendo datos desde: {data_source}")
            df_joined = spark.read.parquet(data_source)

            total_records = df_joined.count()
            print(f"Total de registros cargados: {total_records}")
            if total_records == 0:
                return

            # Cache y vista temporal
            df_joined.cache()
            df_joined.createOrReplaceTempView("covid_data")

            # Verificar columnas disponibles
            available_cols = df_joined.columns
            print(f"Columnas disponibles: {available_cols}")

            # Estadísticas por continente
            if 'continent' in available_cols:
                basic_stats = df_joined.filter(col("continent").isNotNull()) \
                    .groupBy("continent") \
                    .agg(count("*").alias("countries")) \
                    .orderBy(desc("countries"))

                # Guardar estadísticas básicas directamente
                basic_stats.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/descriptive/continent_stats/")
                print("Guardadas estadísticas por continente")

            # Análisis de columnas numéricas
            numeric_cols = [col for col in ['total_cases', 'total_deaths', 'population', 'cases_per_thousand'] if col in available_cols]
            print(f"Columnas numéricas identificadas: {numeric_cols}")
            
            if numeric_cols:
                agg_expressions = [count("*").alias("total_records")]
                for col_name in numeric_cols:
                    agg_expressions.extend([
                        avg(col(col_name)).alias(f"avg_{col_name}"),
                        max(col(col_name)).alias(f"max_{col_name}")
                    ])

                numeric_summary = df_joined.agg(*agg_expressions)

                # Guardar resumen numérico directamente
                numeric_summary.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/descriptive/numeric_summary/")
                print("Guardado resumen numérico")
            
            # Top 10 países por casos
            if 'location' in available_cols and 'total_cases' in available_cols:
                top_countries = df_joined.select("location", "continent", "total_cases", "population", "cases_per_thousand") \
                    .filter(col("total_cases").isNotNull()) \
                    .orderBy(desc("total_cases")) \
                    .limit(10)
                
                top_countries.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/exploratory/top_countries/")
                print("Guardado top 10 países por casos")

            # Análisis de correlaciones
            corr_cols = ['human_development_index', 'gdp_per_capita', 'population_density', 'cases_per_thousand']
            if all(col in available_cols for col in corr_cols) and 'continent' in available_cols:
                # Análisis de correlaciones por continente
                correlation_analysis = spark.sql("""
                    SELECT 
                        continent,
                        CORR(human_development_index, cases_per_thousand) as hdi_cases_correlation,
                        CORR(gdp_per_capita, cases_per_thousand) as gdp_cases_correlation,
                        CORR(population_density, cases_per_thousand) as density_cases_correlation,
                        COUNT(*) as country_count,
                        AVG(human_development_index) as avg_hdi,
                        AVG(gdp_per_capita) as avg_gdp
                    FROM covid_data 
                    WHERE human_development_index IS NOT NULL 
                        AND cases_per_thousand IS NOT NULL
                        AND gdp_per_capita IS NOT NULL
                        AND population_density IS NOT NULL
                    GROUP BY continent
                    ORDER BY hdi_cases_correlation DESC NULLS LAST
                """)
                
                correlation_analysis.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/exploratory/correlation_analysis/")
                print("Guardado análisis de correlaciones")

            # Análisis por HDI
            if 'human_development_index' in available_cols:
                hdi_ranges = spark.sql("""
                    SELECT 
                        CASE 
                            WHEN human_development_index >= 0.8 THEN 'Very High HDI (≥0.8)'
                            WHEN human_development_index >= 0.7 THEN 'High HDI (0.7-0.8)'
                            WHEN human_development_index >= 0.55 THEN 'Medium HDI (0.55-0.7)'
                            ELSE 'Low HDI (<0.55)'
                        END as hdi_category,
                        COUNT(*) as countries,
                        AVG(cases_per_thousand) as avg_cases_per_thousand,
                        AVG(total_deaths_per_million) as avg_deaths_per_million
                    FROM covid_data 
                    WHERE human_development_index IS NOT NULL
                    GROUP BY hdi_category
                    ORDER BY avg_cases_per_thousand DESC
                """)
                
                hdi_ranges.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/exploratory/hdi_analysis/")
                print("Guardado análisis por HDI")

            # === ANÁLISIS AVANZADO (ML) ===
            ml_features = ['human_development_index', 'gdp_per_capita', 'population_density', 'cases_per_thousand']
            
            if all(col in available_cols for col in ml_features):
                # Preparar datos para ML
                ml_data = df_joined.filter(
                    col("human_development_index").isNotNull() &
                    col("gdp_per_capita").isNotNull() &
                    col("population_density").isNotNull() &
                    col("cases_per_thousand").isNotNull() &
                    (col("human_development_index") > 0) &
                    (col("gdp_per_capita") > 0) &
                    (col("population_density") > 0)
                ).select(
                    "location", "continent", "human_development_index", 
                    "gdp_per_capita", "population_density", "cases_per_thousand",
                    "total_deaths_per_million" if "total_deaths_per_million" in available_cols else "total_deaths"
                )
                
                ml_count = ml_data.count()
                print(f"Datos válidos para ML: {ml_count} registros")
                
                if ml_count > 10:  # Asegurar que hay suficientes datos
                    # Clustering K-Means
                    features = ["human_development_index", "gdp_per_capita", "population_density"]
                    
                    assembler = VectorAssembler(inputCols=features, outputCol="features_raw")
                    scaler = StandardScaler(inputCol="features_raw", outputCol="features_scaled")
                    kmeans = KMeans(featuresCol="features_scaled", predictionCol="cluster", k=4, seed=42)
                    
                    pipeline = Pipeline(stages=[assembler, scaler, kmeans])
                    
                    print("Entrenando modelo de clustering...")
                    model = pipeline.fit(ml_data)
                    clustered_data = model.transform(ml_data)
                    
                    # Análisis de clusters
                    cluster_summary = clustered_data.groupBy("cluster") \
                        .agg(
                            count("location").alias("countries"),
                            avg("human_development_index").alias("avg_hdi"),
                            avg("gdp_per_capita").alias("avg_gdp"),
                            avg("population_density").alias("avg_density"),
                            avg("cases_per_thousand").alias("avg_cases_per_thousand")
                        ).orderBy("cluster")
                    
                    # Guardar resultados del clustering
                    clustering_results = clustered_data.select(
                        "location", "continent", "cluster", "human_development_index", 
                        "gdp_per_capita", "cases_per_thousand"
                    )
                    
                    clustering_results.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/advanced/clusters/")
                    cluster_summary.coalesce(1).write.mode("overwrite").option("header", "true").csv(f"{output_uri}/advanced/cluster_summary/")
                    print("Guardado análisis de clustering")
                else:
                    print("No hay suficientes datos válidos para el análisis de ML")
            else:
                print(f"Faltan columnas necesarias para ML. Requeridas: {ml_features}")

    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()
        raise

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--data_source", required=True, help="Ruta a los datos Parquet")
        parser.add_argument("--output_uri", required=True, help="Ruta de salida para los resultados")
        args = parser.parse_args()

        Analytics(args.data_source, args.output_uri)
    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()
        raise
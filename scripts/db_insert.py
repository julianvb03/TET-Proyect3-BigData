import pandas as pd
import psycopg2

csv_path = "../data/country_data.csv"

# Read the csv file
df = pd.read_csv(csv_path, sep=",") 

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="database-p3.cr7nhi9bkmhs.us-east-1.rds.amazonaws.com",
    port=5432,
    database="postgres",
    user="user",
    password="password"
)

cur = conn.cursor()

# Create table
cur.execute("""
    CREATE TABLE IF NOT EXISTS country_data (
        location TEXT PRIMARY KEY,
        continent TEXT,
        population BIGINT,
        population_density NUMERIC,
        median_age NUMERIC,
        aged_65_older NUMERIC,
        aged_70_older NUMERIC,
        gdp_per_capita NUMERIC,
        extreme_poverty NUMERIC,
        cardiovasc_death_rate NUMERIC,
        diabetes_prevalence NUMERIC,
        female_smokers NUMERIC,
        male_smokers NUMERIC,
        handwashing_facilities NUMERIC,
        hospital_beds_per_thousand NUMERIC,
        life_expectancy NUMERIC,
        human_development_index NUMERIC
    )
""")
conn.commit()

# Insert the data
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO country_data (
            location, continent, population, population_density, median_age,
            aged_65_older, aged_70_older, gdp_per_capita, extreme_poverty,
            cardiovasc_death_rate, diabetes_prevalence, female_smokers,
            male_smokers, handwashing_facilities, hospital_beds_per_thousand,
            life_expectancy, human_development_index
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (location) DO NOTHING
    """, (
        row['location'],
        row['continent'],
        row['population'],
        row['population_density'],
        row['median_age'],
        row['aged_65_older'],
        row['aged_70_older'],
        row['gdp_per_capita'],
        row['extreme_poverty'],
        row['cardiovasc_death_rate'],
        row['diabetes_prevalence'],
        row['female_smokers'],
        row['male_smokers'],
        row['handwashing_facilities'],
        row['hospital_beds_per_thousand'],
        row['life_expectancy'],
        row['human_development_index']
    ))

conn.commit()
cur.close()
conn.close()

print("Data inserted successfully.")

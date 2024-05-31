from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row

from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()


# Prueba 

df = spark.createDataFrame([
    Row(a=1, b=2., c='string1', d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
    Row(a=2, b=3., c='string2', d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
    Row(a=4, b=5., c='string3', d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0))
])
df

# Excel to Spark

from pyspark.sql import SparkSession
import pandas

spark = SparkSession.builder.appName("Test").getOrCreate()

db_dir = ""
schema_dir = ""
file = "foo.xlsx"

def file_path(file_name: str, db_path: str = db_dir, schema_path:str = schema_dir) -> str:
    if (schema_path != None) and (db_path != None): # Everything is given
        return f"{db_dir}\\{schema_path}\\{file_name}"
    
    if schema_path == None: 
        if db_dir == None: # Missing both, schema and db path
            return f"{file_name}"
        
        # Missing just schema path
        return f"{db_dir}\\{file_name}"
    
    # Missing just db path
    return f"{schema_dir}\\{file_name}"


def excel_to_spark(file: str, sheet_name: str = None):
    if sheet_name:
        pdf = pandas.read_excel(file, sheet_name = sheet_name)
    else:
        pdf = pandas.read_excel(file)
        
    return spark.createDataFrame(pdf)

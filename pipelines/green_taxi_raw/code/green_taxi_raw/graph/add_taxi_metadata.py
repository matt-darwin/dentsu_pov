from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from green_taxi_raw.config.ConfigStore import *
from green_taxi_raw.udfs.UDFs import *

def add_taxi_metadata(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0\
        .withColumn("taxi_type", lit(Config.taxi_type))\
        .withColumn("year", lit(Config.year))\
        .withColumn("month", lit(Config.month))\
        .withColumn("pickup_date", col("pickup_datetime").cast(DateType()))\
        .withColumn("dropoff_date", col("dropoff_datetime").cast(DateType()))

from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from green_taxi_raw.config.ConfigStore import *
from green_taxi_raw.udfs.UDFs import *

def taxi_data_reformat(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("VendorID"), 
        col("lpep_pickup_datetime").alias("pickup_datetime"), 
        col("lpep_dropoff_datetime").alias("dropoff_datetime"), 
        col("passenger_count"), 
        col("trip_distance"), 
        col("RatecodeID"), 
        col("store_and_fwd_flag"), 
        col("PULocationID"), 
        col("DOLocationID"), 
        col("payment_type"), 
        col("fare_amount"), 
        col("extra"), 
        col("mta_tax"), 
        col("tip_amount"), 
        col("tolls_amount"), 
        col("improvement_surcharge"), 
        col("total_amount"), 
        col("congestion_surcharge"), 
        create_map(lit("ehail_fee"), col("ehail_fee"), lit("trip_type"), col("trip_type"))\
          .alias("additional_information")
    )

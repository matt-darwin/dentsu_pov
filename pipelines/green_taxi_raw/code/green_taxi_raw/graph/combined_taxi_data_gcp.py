from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from green_taxi_raw.config.ConfigStore import *
from green_taxi_raw.udfs.UDFs import *

def combined_taxi_data_gcp(spark: SparkSession, in0: DataFrame):
    in0.write\
        .format("parquet")\
        .mode("overwrite")\
        .partitionBy("taxi_type", "year", "month")\
        .save("gs://md-demo-prophecy-demo-dataproc-config/nyc_taxi/transformed/trips/")

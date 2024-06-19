from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from yellow_taxi_raw.config.ConfigStore import *
from yellow_taxi_raw.udfs.UDFs import *

def yellow_taxi_raw(spark: SparkSession) -> DataFrame:
    return spark.read\
        .format("parquet")\
        .load(f"{Config.cloud_storage_path}{Config.taxi_type}/{Config.year}/{Config.month}/{Config.taxi_type}_tripdata_{Config.year}-{Config.month}.parquet")

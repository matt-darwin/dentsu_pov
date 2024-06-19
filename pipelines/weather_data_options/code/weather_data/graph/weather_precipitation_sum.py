from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def weather_precipitation_sum(spark: SparkSession, in0: DataFrame):
    in0.write\
        .format("parquet")\
        .mode("overwrite")\
        .partitionBy("year", "month", "json_content_latitude", "json_content_longitude")\
        .save(f"{Config.storage_bucket}weather_precipitation_sum/")

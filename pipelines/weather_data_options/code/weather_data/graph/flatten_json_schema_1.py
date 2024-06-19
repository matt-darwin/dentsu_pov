from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def flatten_json_schema_1(spark: SparkSession, in0: DataFrame) -> DataFrame:
    flt_col = in0.withColumn("metrics", explode_outer("metrics")).columns
    selectCols = [col("json_content-latitude") if "json_content-latitude" in flt_col else col("json_content.latitude")\
                    .alias("json_content-latitude"),                   col("json_content-longitude") if "json_content-longitude" in flt_col else col("json_content.longitude")\
                    .alias("json_content-longitude"),                   col("metrics-time") if "metrics-time" in flt_col else col("metrics.time").alias("metrics-time"),                   col("metrics-precipitation_sum") if "metrics-precipitation_sum" in flt_col else col("metrics.precipitation_sum")\
                    .alias("metrics-precipitation_sum")]

    return in0.withColumn("metrics", explode_outer("metrics")).select(*selectCols)

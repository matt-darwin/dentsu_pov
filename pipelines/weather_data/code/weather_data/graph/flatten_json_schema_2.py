from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def flatten_json_schema_2(spark: SparkSession, in0: DataFrame) -> DataFrame:
    flt_col = in0.withColumn("metrics", explode_outer("metrics")).columns
    selectCols = [col("json_content_latitude") if "json_content_latitude" in flt_col else col("json_content.latitude")\
                    .alias("json_content_latitude"),                   col("json_content_longitude") if "json_content_longitude" in flt_col else col("json_content.longitude")\
                    .alias("json_content_longitude"),                   col("metrics_time") if "metrics_time" in flt_col else col("metrics.time").alias("metrics_time"),                   col("metrics_precipitation_sum") if "metrics_precipitation_sum" in flt_col else col("metrics.precipitation_sum")\
                    .alias("metrics_precipitation_sum")]

    return in0.withColumn("metrics", explode_outer("metrics")).select(*selectCols)

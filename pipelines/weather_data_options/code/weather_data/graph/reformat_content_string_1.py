from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def reformat_content_string_1(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(decode(col("content"), "utf-8").alias("json_content"))

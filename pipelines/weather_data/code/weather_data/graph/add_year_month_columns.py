from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def add_year_month_columns(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0\
        .withColumn("year", year(col("metrics_time")))\
        .withColumn("month", month(col("metrics_time")))\
        .withColumn("metrics_time", to_date(col("metrics_time")))

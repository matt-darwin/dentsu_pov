from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from yellow_taxi_raw.config.ConfigStore import *
from yellow_taxi_raw.udfs.UDFs import *

def combined_taxi_data(spark: SparkSession, in0: DataFrame):
    in0.write\
        .format("delta")\
        .option("overwriteSchema", True)\
        .mode("overwrite")\
        .partitionBy("taxi_type", "year", "month")\
        .saveAsTable("`dentsu_pov`.`dentsu_pov`.`combined_taxi_data`")

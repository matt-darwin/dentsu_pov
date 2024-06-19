from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from zones_load.config.ConfigStore import *
from zones_load.udfs.UDFs import *

def zones_load(spark: SparkSession) -> DataFrame:
    return spark.read\
        .schema(
          StructType([
            StructField("LocationID", DoubleType(), True), StructField("Borough", StringType(), True), StructField("Zone", StringType(), True), StructField("service_zone", StringType(), True)
        ])
        )\
        .option("header", True)\
        .option("sep", ",")\
        .csv(f"{Config.storage_location}taxi_zone_lookup.csv")

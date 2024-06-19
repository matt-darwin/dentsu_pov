from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from table_iterator_example.config.ConfigStore import *
from table_iterator_example.udfs.UDFs import *

def zones(spark: SparkSession) -> DataFrame:
    return spark.read.table("`nyc_taxi`.`field_nyc_taxi`.`zones`")

from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def SchemaTransform_1_1_1(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.withColumn(
        "metrics",
        arrays_zip(col("json_content.daily.time"), col("json_content.daily.precipitation_sum"))
    )

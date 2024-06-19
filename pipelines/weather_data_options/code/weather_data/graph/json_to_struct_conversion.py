from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def json_to_struct_conversion(spark: SparkSession, in0: DataFrame) -> DataFrame:
    schema = StructType([
        StructField("latitude", DecimalType(6, 4)),
            StructField("longitude", DecimalType(6, 4)),
            StructField("generationtime_ms", DecimalType(10, 4)),
            StructField("timezone", StringType()),
            StructField("timezone_abbreviation", StringType()),
            StructField("daily", StructType([
          StructField("time", ArrayType(StringType())),
                                              StructField("precipitation_sum", ArrayType(DecimalType(4, 1)))

        ])),
            StructField("daily_units", StringType()),
        
    ])
    out0 = in0.withColumn("json_content", from_json(decode(col("content"), 'utf-8'), schema))

    return out0

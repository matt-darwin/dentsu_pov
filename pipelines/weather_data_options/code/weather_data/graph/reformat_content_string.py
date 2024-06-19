from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def reformat_content_string(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        expr(
            "from_json(decode(content, 'utf-8'), 'STRUCT<latitude:DECIMAL(6,4),longitude:DECIMAL(6,4),generationtime_ms: DECIMAL(10,4),timezone:STRING,timezone_abbreviation:STRING,daily:STRUCT<time:ARRAY<STRING>,precipitation_sum:ARRAY<DECIMAL(4,1)>>,daily_units: STRING>')"
          )\
          .alias("json_content")
    )

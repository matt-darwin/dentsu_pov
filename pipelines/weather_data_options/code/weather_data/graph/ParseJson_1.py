from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def ParseJson_1(spark: SparkSession, in0: DataFrame) -> DataFrame:
    df1 = in0.select(regexp_replace("json_content", '\\\\', ""))
    df2 = df1.take(1)

    return in0.withColumn(
        "json_content",
        from_json(regexp_replace("json_content", '\\\\', ""), schema_of_json(df2[0][0]))
    )

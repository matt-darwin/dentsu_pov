from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def weather_data_source(spark: SparkSession) -> DataFrame:
    from spark_ai.webapps import WebUtils
    WebUtils().register_udfs(spark)
    df1 = spark.range(1)

    return df1\
        .withColumn(
          "url",
          lit(
            f"https://archive-api.open-meteo.com/v1/archive?latitude={Config.latitude}&longitude={Config.longitude}&start_date={Config.start_date}&end_date={Config.end_date}&daily=precipitation_sum"
          )
        )\
        .withColumn("content", expr("web_scrape(url)"))

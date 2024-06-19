from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *

def weather_data_get(spark: SparkSession) -> DataFrame:
    from typing import Optional, List, Dict
    from dataclasses import dataclass, field
    from abc import ABC
    
    from pyspark.sql.column import Column
    from pyspark.sql.functions import col
    from dataclasses import dataclass
    from typing import Optional, List, Dict
    from pyspark.sql.column import Column as sparkColumn


    @dataclass(frozen = True)
    class SColumn:
        expression: Optional[Column] = None

        @staticmethod
        def getSColumn(column: str):
            return SColumn(col(column))

        def column(self) -> sparkColumn:
            return self.expression

        def columnName(self) -> str:
            return self.expression._jc.toString()


    @dataclass(frozen = True)
    class SColumnExpression:
        target: str
        expression: SColumn
        description: str
        _row_id: Optional[str] = None

        @staticmethod
        def remove_backticks(s):
            if s.startswith("`") and s.endswith("`"):
                return s[1:- 1]
            else:
                return s

        @staticmethod
        def getColumnExpression(column: str):
            return SColumnExpression(column, SColumn.getSColumn(col(column)), "")

        @staticmethod
        def getColumnsFromColumnExpressionList(columnExpressions: list):
            columnList = []

            for expression in columnExpressions:
                columnList.append(expression.expression)

            return columnList

        def column(self) -> Column:

            if (self.expression.columnName() == SColumnExpression.remove_backticks(self.target)):
                return self.expression.expression

            return self.expression.expression.alias(self.target)


    @dataclass(frozen = True)
    class WeatherDataGetProperties():
        startdate: str = "2024-01-01"
        enddate: str = "2024-06-01"
        latitude: str = "0"
        longitude: str = "0"

    props = WeatherDataGetProperties(  #skiptraversal
        startdate = Config.start_date, 
        enddate = Config.end_date, 
        latitude = Config.latitude, 
        longitude = Config.longitude
    )
    from spark_ai.webapps import WebUtils
    WebUtils().register_udfs(spark)
    df1 = spark.range(1)
    latitude = props.latitude
    longitude = props.longitude
    startdate = props.startdate
    enddate = props.enddate
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={startdate}&end_date={enddate}&daily=precipitation_sum"
    api_data = df1.withColumn("url", lit(url)).withColumn("content", expr("web_scrape(url)"))
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
    out0 = api_data.withColumn("json_content", from_json(decode(col("content"), 'utf-8'), schema))

    return out0

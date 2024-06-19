from prophecy.cb.server.base.ComponentBuilderBase import *
from pyspark.sql import *
from pyspark.sql.functions import *

from prophecy.cb.server.base import WorkflowContext
from prophecy.cb.server.base.datatypes import SInt, SString, SFloat, SString
from prophecy.cb.ui.uispec import *


class WeatherDataGet(ComponentSpec):
    name: str = "WeatherDataGet"
    category: str = "Custom"

    def optimizeCode(self) -> bool:
        return False

    @dataclass(frozen=True)
    class WeatherDataGetProperties(ComponentProperties):
        startdate: SString = "2024-01-01"
        enddate: SString = "2024-06-01"
        latitude: SString = "0"
        longitude: SString = "0"

    def dialog(self) -> Dialog:
        return Dialog("WeatherDataGet").addElement(
            ColumnsLayout(gap="1rem", height="100%")
                .addColumn(PortSchemaTabs().importSchema(), "0.5fr")
                .addColumn(                   
                    StackLayout()
                        .addElement(ExpressionBox("Start Date")
                                    .bindPlaceholder("2024-01-01")
                                    .bindProperty("startdate"))
                        .addElement(ExpressionBox("End Date")
                                    .bindPlaceholder("2024-06-01")
                                    .bindProperty("enddate"))
                        .addElement(ExpressionBox("Latitude")
                                    .bindPlaceholder("0")
                                    .bindProperty("latitude"))
                        .addElement(ExpressionBox("Longitude")
                                    .bindPlaceholder("0")
                                    .bindProperty("longitude"))
                )
            )
        

    def validate(self, context: WorkflowContext, component: Component[WeatherDataGetProperties]) -> List[Diagnostic]:
        return []

    def onChange(self, context: WorkflowContext, oldState: Component[WeatherDataGetProperties], newState: Component[WeatherDataGetProperties]) -> Component[
    WeatherDataGetProperties]:
        return newState

    class WeatherDataGetCode(ComponentCode):
        def __init__(self, newProps):
            self.props: WeatherDataGet.WeatherDataGetProperties = newProps

        def apply(self, spark: SparkSession) -> DataFrame:
            
            from spark_ai.webapps import WebUtils
            WebUtils().register_udfs(spark)
            df1 = spark.range(1)

            latitude = self.props.latitude
            longitude = self.props.longitude
            startdate = self.props.startdate
            enddate = self.props.enddate

            url = f"https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={startdate}&end_date={enddate}&daily=precipitation_sum"

            api_data = df1\
                .withColumn(
                "url",
                lit(
                   url
                )
                )\
                .withColumn("content", expr("web_scrape(url)"))

            schema = StructType([StructField("latitude", DecimalType(6,4)),
                StructField("longitude", DecimalType(6,4)),
                StructField("generationtime_ms", DecimalType(10,4)),
                StructField("timezone", StringType()),
                StructField("timezone_abbreviation", StringType()),
                StructField("daily", StructType([StructField("time", ArrayType(StringType())),
                                                StructField("precipitation_sum", ArrayType(DecimalType(4,1)))
                                                ])
                            ),
                StructField("daily_units", StringType()),
                ])

            out0 = api_data.withColumn("json_content", from_json(decode(col("content"), 'utf-8'), schema))

            return out0




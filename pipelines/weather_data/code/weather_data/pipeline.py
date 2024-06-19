from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *
from prophecy.utils import *
from weather_data.graph import *

def pipeline(spark: SparkSession) -> None:
    df_weather_data_get = weather_data_get(spark)
    df_SchemaTransform_1_2 = SchemaTransform_1_2(spark, df_weather_data_get)
    df_flatten_json_schema_2 = flatten_json_schema_2(spark, df_SchemaTransform_1_2)
    df_add_year_month_columns = add_year_month_columns(spark, df_flatten_json_schema_2)
    weather_precipitation_sum_dbx(spark, df_add_year_month_columns)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/weather_data")
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/weather_data", config = Config)(pipeline)

if __name__ == "__main__":
    main()

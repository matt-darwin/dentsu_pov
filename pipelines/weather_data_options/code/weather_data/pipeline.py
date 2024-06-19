from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from weather_data.config.ConfigStore import *
from weather_data.udfs.UDFs import *
from prophecy.utils import *
from weather_data.graph import *

def pipeline(spark: SparkSession) -> None:
    df_weather_data_source = weather_data_source(spark)
    df_json_to_struct_conversion = json_to_struct_conversion(spark, df_weather_data_source)
    df_SchemaTransform_1 = SchemaTransform_1(spark, df_json_to_struct_conversion)
    df_reformat_content_string_1 = reformat_content_string_1(spark, df_weather_data_source)
    df_reformat_content_string = reformat_content_string(spark, df_weather_data_source)
    df_SchemaTransform_1_1 = SchemaTransform_1_1(spark, df_reformat_content_string)
    df_flatten_json_schema_1 = flatten_json_schema_1(spark, df_SchemaTransform_1_1)
    df_ParseJson_1 = ParseJson_1(spark, df_reformat_content_string_1)
    df_SchemaTransform_1_1_1 = SchemaTransform_1_1_1(spark, df_ParseJson_1)
    df_flatten_json_schema_1_1 = flatten_json_schema_1_1(spark, df_SchemaTransform_1_1_1)
    df_flatten_json_schema = flatten_json_schema(spark, df_SchemaTransform_1)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/weather_data_options")
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/weather_data_options", config = Config)(pipeline)

if __name__ == "__main__":
    main()

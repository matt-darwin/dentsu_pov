from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from green_taxi_raw.config.ConfigStore import *
from green_taxi_raw.udfs.UDFs import *
from prophecy.utils import *
from green_taxi_raw.graph import *

def pipeline(spark: SparkSession) -> None:
    df_green_taxi_raw = green_taxi_raw(spark)
    df_taxi_data_reformat = taxi_data_reformat(spark, df_green_taxi_raw)
    df_add_taxi_metadata = add_taxi_metadata(spark, df_taxi_data_reformat)

    if Config.provider == 'databricks':
        combined_taxi_data(spark, df_add_taxi_metadata)

    if Config.provider == 'gcp':
        combined_taxi_data_gcp(spark, df_add_taxi_metadata)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/green_taxi_raw")
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/green_taxi_raw", config = Config)(pipeline)

if __name__ == "__main__":
    main()

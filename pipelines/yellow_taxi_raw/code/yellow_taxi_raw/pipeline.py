from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from yellow_taxi_raw.config.ConfigStore import *
from yellow_taxi_raw.udfs.UDFs import *
from prophecy.utils import *
from yellow_taxi_raw.graph import *

def pipeline(spark: SparkSession) -> None:
    df_yellow_taxi_raw = yellow_taxi_raw(spark)
    df_taxi_data_reformatting = taxi_data_reformatting(spark, df_yellow_taxi_raw)
    df_add_taxi_type_year_month = add_taxi_type_year_month(spark, df_taxi_data_reformatting)
    combined_taxi_data(spark, df_add_taxi_type_year_month)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/yellow_taxi_raw")
    spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/yellow_taxi_raw", config = Config)(pipeline)

if __name__ == "__main__":
    main()

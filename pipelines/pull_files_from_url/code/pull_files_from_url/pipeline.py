from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pull_files_from_url.config.ConfigStore import *
from pull_files_from_url.udfs.UDFs import *
from prophecy.utils import *
from pull_files_from_url.graph import *

def pipeline(spark: SparkSession) -> None:
    get_zones_data(spark)
    get_yellow_data(spark)
    get_green_data(spark)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("pull_files_from_url")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/pull_files_from_url")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/pull_files_from_url", config = Config)(pipeline)

if __name__ == "__main__":
    main()

from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pull_files_from_url_dbx.config.ConfigStore import *
from pull_files_from_url_dbx.udfs.UDFs import *
from prophecy.utils import *
from pull_files_from_url_dbx.graph import *

def pipeline(spark: SparkSession) -> None:
    zones_download(spark)
    Yellow_Download(spark)
    Green_Download(spark)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("pull_files_from_url_dbx")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/pull_files_from_url_dbx")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/pull_files_from_url_dbx", config = Config)(pipeline)

if __name__ == "__main__":
    main()

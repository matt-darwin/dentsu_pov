from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from zones_load.config.ConfigStore import *
from zones_load.udfs.UDFs import *
from prophecy.utils import *
from zones_load.graph import *

def pipeline(spark: SparkSession) -> None:
    df_zones_load = zones_load(spark)
    zones(spark, df_zones_load)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/zones_load")
    spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/zones_load", config = Config)(pipeline)

if __name__ == "__main__":
    main()

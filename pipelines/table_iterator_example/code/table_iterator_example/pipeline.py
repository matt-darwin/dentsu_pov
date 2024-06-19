from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from table_iterator_example.config.ConfigStore import *
from table_iterator_example.udfs.UDFs import *
from prophecy.utils import *
from table_iterator_example.graph import *

def pipeline(spark: SparkSession) -> None:
    df_zones = zones(spark)
    Zone_Iterator(Config.Zone_Iterator).apply(spark, df_zones)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("table_iterator_example")\
                .getOrCreate()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/table_iterator_example")
    registerUDFs(spark)
    
    MetricsCollector.instrument(spark = spark, pipelineId = "pipelines/table_iterator_example", config = Config)(pipeline)

if __name__ == "__main__":
    main()

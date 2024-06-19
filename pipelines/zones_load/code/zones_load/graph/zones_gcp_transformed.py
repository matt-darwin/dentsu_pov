from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from zones_load.config.ConfigStore import *
from zones_load.udfs.UDFs import *

def zones_gcp_transformed(spark: SparkSession, in0: DataFrame):
    in0.write\
        .format("parquet")\
        .mode("overwrite")\
        .save("gs://md-demo-prophecy-demo-dataproc-config/nyc_taxi/transformed/zones/")

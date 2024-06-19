from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from zones_load.config.ConfigStore import *
from zones_load.udfs.UDFs import *

def zones(spark: SparkSession, in0: DataFrame):
    in0.write.format("delta").mode("overwrite").saveAsTable("`dentsu_pov`.`dentsu_pov`.`zones`")

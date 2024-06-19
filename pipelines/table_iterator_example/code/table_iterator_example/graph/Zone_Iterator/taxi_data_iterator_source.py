from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from .config import *
from table_iterator_example.udfs.UDFs import *

def taxi_data_iterator_source(spark: SparkSession) -> DataFrame:
    return spark.sql(
        f'SELECT * FROM `nyc_taxi`.`field_nyc_taxi`.`combined_taxi_data` WHERE PULocationId={Config.LocationID}'
    )

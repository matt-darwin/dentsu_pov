from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from .config import *
from table_iterator_example.udfs.UDFs import *

def fare_journeys_distance_by_location_date(spark: SparkSession, in0: DataFrame) -> DataFrame:
    df1 = in0.groupBy(col("PULocationID"), col("pickup_date"))

    return df1.agg(
        sum(col("total_amount")).alias("Total_Fare"), 
        count(lit(1)).alias("Total_Journeys"), 
        avg(col("trip_distance")).alias("Average_Distance")
    )

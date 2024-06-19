from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from table_iterator_example.udfs.UDFs import *
from . import *
from .config import *


class Zone_Iterator(MetaGemExec):

    def __init__(self, config):
        self.config = config
        super().__init__()

    def execute(self, spark: SparkSession, subgraph_config: SubgraphConfig) -> List[DataFrame]:
        Config.update(subgraph_config)
        df_taxi_data_iterator_source = taxi_data_iterator_source(spark)
        df_fare_journeys_distance_by_location_date = fare_journeys_distance_by_location_date(
            spark, 
            df_taxi_data_iterator_source
        )
        subgraph_config.update(Config)

    def apply(self, spark: SparkSession, in0: DataFrame, ) -> None:
        inDFs = []
        results = []
        conf_to_column = dict(
            [("LocationID", "LocationID"), ("Borough", "Borough"), ("Zone", "Zone"), ("service_zone", "service_zone")]
        )

        if in0.count() > 1000:
            raise Exception(f"Config DataFrame row count::{in0.count()} exceeds max run count")

        for row in in0.collect():
            update_config = self.config.update_from_row_map(row, conf_to_column)
            _inputs = inDFs
            results.append(self.__run__(spark, update_config, *_inputs))

        return do_union(results)

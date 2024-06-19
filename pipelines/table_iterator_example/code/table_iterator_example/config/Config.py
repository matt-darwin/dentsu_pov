from table_iterator_example.graph.Zone_Iterator.config.Config import SubgraphConfig as Zone_Iterator_Config
from prophecy.config import ConfigBase


class Config(ConfigBase):

    def __init__(self, Zone_Iterator: dict=None, **kwargs):
        self.spark = None
        self.update(Zone_Iterator)

    def update(self, Zone_Iterator: dict={}, **kwargs):
        prophecy_spark = self.spark
        self.Zone_Iterator = self.get_config_object(
            prophecy_spark, 
            Zone_Iterator_Config(prophecy_spark = prophecy_spark), 
            Zone_Iterator, 
            Zone_Iterator_Config
        )
        pass

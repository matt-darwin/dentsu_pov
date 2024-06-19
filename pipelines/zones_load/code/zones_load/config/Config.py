from prophecy.config import ConfigBase


class Config(ConfigBase):

    def __init__(self, storage_location: str=None, provider: str=None, **kwargs):
        self.spark = None
        self.update(storage_location, provider)

    def update(
            self,
            storage_location: str="gs://md-demo-prophecy-demo-dataproc-config/nyc_taxi/raw/",
            provider: str="gcp",
            **kwargs
    ):
        prophecy_spark = self.spark
        self.storage_location = storage_location
        self.provider = provider
        pass

from prophecy.config import ConfigBase


class Config(ConfigBase):

    def __init__(
            self,
            taxi_type: str=None,
            year: str=None,
            month: str=None,
            cloud_storage_path: str=None,
            provider: str=None,
            **kwargs
    ):
        self.spark = None
        self.update(taxi_type, year, month, cloud_storage_path, provider)

    def update(
            self,
            taxi_type: str="green_data",
            year: str="2024",
            month: str="01",
            cloud_storage_path: str="gs://md-demo-prophecy-demo-dataproc-config/nyc_taxi/raw/",
            provider: str="gcp",
            **kwargs
    ):
        prophecy_spark = self.spark
        self.taxi_type = taxi_type
        self.year = year
        self.month = month
        self.cloud_storage_path = cloud_storage_path
        self.provider = provider
        pass

from prophecy.config import ConfigBase


class Config(ConfigBase):

    def __init__(
            self,
            storage_bucket: str=None,
            year: str=None,
            month: str=None,
            file_path: str=None,
            gcp_project: str=None,
            **kwargs
    ):
        self.spark = None
        self.update(storage_bucket, year, month, file_path, gcp_project)

    def update(
            self,
            storage_bucket: str="md-demo-prophecy-demo-dataproc-config",
            year: str="2024",
            month: str="01",
            file_path: str="nyc_taxi/raw/",
            gcp_project: str="prophecy-field",
            **kwargs
    ):
        prophecy_spark = self.spark
        self.storage_bucket = storage_bucket
        self.year = year
        self.month = month
        self.file_path = file_path
        self.gcp_project = gcp_project
        pass

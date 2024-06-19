from prophecy.config import ConfigBase


class Config(ConfigBase):

    def __init__(
            self,
            latitude: str=None,
            longitude: str=None,
            start_date: str=None,
            end_date: str=None,
            json_schema: str=None,
            storage_bucket: str=None,
            provider: str=None,
            **kwargs
    ):
        self.spark = None
        self.update(latitude, longitude, start_date, end_date, json_schema, storage_bucket, provider)

    def update(
            self,
            latitude: str="74.0060",
            longitude: str="40.7128",
            start_date: str="2024-01-01",
            end_date: str="2024-01-31",
            json_schema: str="STRUCT<latitude:DECIMAL(6,4),longitude:DECIMAL(6,4),generationtime_ms: DECIMAL(10,4),timezone:STRING,timezone_abbreviation:STRING,daily:STRUCT<time:ARRAY<STRING>,precipitation_sum:ARRAY<DECIMAL(4,1)>>,daily_units: STRING>",
            storage_bucket: str="gs://md-demo-prophecy-demo-dataproc-config/nyc_taxi/transformed/",
            provider: str="gcp",
            **kwargs
    ):
        prophecy_spark = self.spark
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.json_schema = json_schema
        self.storage_bucket = storage_bucket
        self.provider = provider
        pass

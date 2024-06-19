from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from pull_files_from_url.config.ConfigStore import *
from pull_files_from_url.udfs.UDFs import *

def get_zones_data(spark: SparkSession):
    from typing import Optional, List, Dict
    from dataclasses import dataclass, field
    from abc import ABC
    
    from pyspark.sql.column import Column
    from pyspark.sql.functions import col
    from dataclasses import dataclass
    from typing import Optional, List, Dict
    from pyspark.sql.column import Column as sparkColumn


    @dataclass(frozen = True)
    class SColumn:
        expression: Optional[Column] = None

        @staticmethod
        def getSColumn(column: str):
            return SColumn(col(column))

        def column(self) -> sparkColumn:
            return self.expression

        def columnName(self) -> str:
            return self.expression._jc.toString()


    @dataclass(frozen = True)
    class SColumnExpression:
        target: str
        expression: SColumn
        description: str
        _row_id: Optional[str] = None

        @staticmethod
        def remove_backticks(s):
            if s.startswith("`") and s.endswith("`"):
                return s[1:- 1]
            else:
                return s

        @staticmethod
        def getColumnExpression(column: str):
            return SColumnExpression(column, SColumn.getSColumn(col(column)), "")

        @staticmethod
        def getColumnsFromColumnExpressionList(columnExpressions: list):
            columnList = []

            for expression in columnExpressions:
                columnList.append(expression.expression)

            return columnList

        def column(self) -> Column:

            if (self.expression.columnName() == SColumnExpression.remove_backticks(self.target)):
                return self.expression.expression

            return self.expression.expression.alias(self.target)


    @dataclass(frozen = True)
    class FileURLDownloadProperties():
        # properties for the component with default values
        file_url: str = str("")
        file_name: str = str("")
        target_bucket: str = str("")
        target_bucket_filepath: str = str("")
        gcp_project: str = str("")
        service_account_file_path: str = str("")
        platform: str = str("")
        dbfs_path: str = str("")

    props = FileURLDownloadProperties(  #skiptraversal
        file_url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv", 
        file_name = "taxi_zone_lookup.csv", 
        target_bucket = Config.storage_bucket, 
        target_bucket_filepath = Config.file_path, 
        gcp_project = Config.gcp_project, 
        service_account_file_path = "/tmp/creds.json", 
        platform = "Databricks", 
        dbfs_path = ""
    )
    # This method contains logic used to generate the spark code from the given inputs.
    import urllib.request
    urllib.request.urlretrieve(f"{props.file_url}", f"/tmp/{props.file_name}")

    if props.platform == "GCP":
        from google.cloud import storage
        from google.oauth2 import service_account
        credentials = service_account.Credentials.from_service_account_file(props.service_account_file_path)
        client = storage.Client(project = props.gcp_project, credentials = credentials)
        bucket = client.get_bucket(props.target_bucket)
        blob = bucket.blob(f"{props.target_bucket_filepath}{props.file_name}")
        blob.upload_from_filename(f"/tmp/{props.file_name}")
    elif props.platform == "Databricks":
        dbutils.fs.cp(f"file:/tmp/{props.file_name}", f"{props.dbfs_path}{props.file_name}")

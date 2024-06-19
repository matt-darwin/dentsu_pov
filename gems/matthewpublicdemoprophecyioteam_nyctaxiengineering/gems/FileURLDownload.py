from prophecy.cb.server.base.ComponentBuilderBase import *
from pyspark.sql import *
from pyspark.sql.functions import *

from prophecy.cb.server.base import WorkflowContext
from prophecy.cb.server.base.datatypes import SInt, SString
from prophecy.cb.ui.uispec import *


class FileURLDownload(ComponentSpec):
    name: str = "FileURLDownload"
    category: str = "Custom"

    def optimizeCode(self) -> bool:
        # Return whether code optimization is enabled for this component
        return False

    @dataclass(frozen=True)
    class FileURLDownloadProperties(ComponentProperties):
        # properties for the component with default values
        file_url: SString = SString("")
        file_name: SString = SString("")
        target_bucket: SString = SString("")
        target_bucket_filepath: SString = SString("")
        gcp_project: SString = SString("")
        service_account_file_path: SString = SString("")
        platform: SString = SString("")
        dbfs_path: SString = SString("")

    def dialog(self) -> Dialog:
        # Define the UI dialog structure for the component
        platform = StackLayout().addElement(SelectBox("Platform")
                     .addOption("GCP", "GCP")
                     .addOption("Databricks", "Databricks")
                     .bindProperty("platform")
            )
        
        upload_file = Condition() \
                .ifEqual(PropExpr("component.properties.platform"), StringExpr("GCP")) \
                .then(
                    StackLayout()
                        .addElement(ExpressionBox("GCP Project")
                                    .bindPlaceholder("your-gcp-project-id")
                                    .bindProperty("gcp_project"))
                        .addElement(ExpressionBox("Service Account Private Key Path")
                                    .bindPlaceholder("eg: /tmp/creds.json")
                                    .bindProperty("service_account_file_path"))
                        .addElement(ExpressionBox("Target Bucket")
                                    .bindPlaceholder("your-bucket-name")
                                    .bindProperty("target_bucket"))
                        .addElement(ExpressionBox("Target Bucket File Path")
                                    .bindPlaceholder("eg: nyc_taxi/raw/")
                                    .bindProperty("target_bucket_filepath"))
                ).otherwise(Condition() \
                    .ifEqual(PropExpr("component.properties.platform"), StringExpr("Databricks")) \
                    .then(
                        StackLayout()
                            .addElement(ExpressionBox("DBFS path")
                                .bindPlaceholder("eg: dbfs:/my_dir/")
                                .bindProperty("dbfs_path"))
                        )
                )

        return Dialog("FileURLDownload").addElement(
            ColumnsLayout(gap="1rem", height="100%")
                #.addColumn(Ports(defaultCustomOutputSchema = True), "0fr")
                .addColumn(   
                    StackLayout().addElement(ExpressionBox("File URL")
                                            .bindPlaceholder("https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv")
                                            .bindProperty("file_url"))
                                .addElement(ExpressionBox("File Name")
                                            .bindPlaceholder("taxi_zone_lookup.csv")
                                            .bindProperty("file_name"))

                    )
                .addColumn(StackLayout().addElement(platform)
                                        .addElement(upload_file)
                ).addElement(Ports(defaultCustomOutputSchema = True))

        )

    def validate(self, context: WorkflowContext, component: Component[FileURLDownloadProperties]) -> List[Diagnostic]:
        # Validate the component's state
        return []

    def onChange(self, context: WorkflowContext, oldState: Component[FileURLDownloadProperties], newState: Component[FileURLDownloadProperties]) -> Component[
    FileURLDownloadProperties]:
        # Handle changes in the component's state and return the new state
        return newState


    class FileURLDownloadCode(ComponentCode):
        def __init__(self, newProps):
            self.props: FileURLDownload.FileURLDownloadProperties = newProps
        
        def apply(self, spark: SparkSession):
            # This method contains logic used to generate the spark code from the given inputs.
            import urllib.request
            urllib.request.urlretrieve(f"{self.props.file_url}", f"/tmp/{self.props.file_name}")

            if self.props.platform == "GCP":
                
                from google.cloud import storage
                from google.oauth2 import service_account

                credentials = service_account.Credentials.from_service_account_file(self.props.service_account_file_path)

                client = storage.Client(project=self.props.gcp_project, credentials=credentials)
                bucket = client.get_bucket(self.props.target_bucket)
                blob = bucket.blob(f"{self.props.target_bucket_filepath}{self.props.file_name}")
                blob.upload_from_filename(f"/tmp/{self.props.file_name}")
            elif self.props.platform == "Databricks":
                dbutils.fs.cp(f"file:/tmp/{self.props.file_name}", f"{self.props.dbfs_path}{self.props.file_name}")




            
        




            

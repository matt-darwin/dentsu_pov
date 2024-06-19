from prophecy.config import ConfigBase


class SubgraphConfig(ConfigBase):

    def __init__(
            self,
            prophecy_spark=None,
            LocationID: float=0.0,
            Borough: str="",
            Zone: str="",
            service_zone: str="",
            **kwargs
    ):
        self.LocationID = LocationID
        self.Borough = Borough
        self.Zone = Zone
        self.service_zone = service_zone
        pass

    def update(self, updated_config):
        self.LocationID = updated_config.LocationID
        self.Borough = updated_config.Borough
        self.Zone = updated_config.Zone
        self.service_zone = updated_config.service_zone
        pass

Config = SubgraphConfig()

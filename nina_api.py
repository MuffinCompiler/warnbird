from deutschland import nina
from deutschland.nina.api import archive_api, covid_api, warnings_api, default_api


class Nina:

    # setup nina api
    def __init__(self, cfg):
        configuration = nina.Configuration(
            host=cfg.nina_api_endpoint
        )

        # Enter a context with an instance of the API client
        self.api_client = nina.ApiClient(configuration)

        # Create an instance of the API class
        self.archive_api_instance = archive_api.ArchiveApi(self.api_client)
        self.covid_api_instance = covid_api.CovidApi(self.api_client)
        self.warnings_api_instance = warnings_api.WarningsApi(self.api_client)
        self.default_api_instance = default_api.DefaultApi(self.api_client)

    def get_all_warning_snapshot(self):

        warns = dict()
        warns['dwd'] = self.get_dwd_warns()
        warns['katwarn'] = self.get_katwarn_warns()

        # TODO

        return warns


    def get_dwd_warns(self):
        return self.warnings_api_instance.get_dwd_map_data()

    def get_katwarn_warns(self):
        return self.warnings_api_instance.get_katwarn_map_data()
from deutschland import nina
from deutschland.nina.api import archive_api, covid_api, warnings_api, default_api
import json, requests
from nina_event import EventSource, NinaEvent


def get_history_if_present(event):
    print("NYI")
    exit(1)


class Nina:

    # setup nina api
    def __init__(self, bird_client):
        configuration = nina.Configuration(
            host=bird_client.cfg.nina.api_endpoint
        )

        self.bird_client = bird_client

        # Enter a context with an instance of the API client
        self.api_client = nina.ApiClient(configuration)

        # Create an instance of the API class
        # TODO dont use api at all???
        self.archive_api_instance = archive_api.ArchiveApi(self.api_client)
        self.covid_api_instance = covid_api.CovidApi(self.api_client)
        self.warnings_api_instance = warnings_api.WarningsApi(self.api_client)
        self.default_api_instance = default_api.DefaultApi(self.api_client)

    def get_warning_snapshot(self, sources=None):  # : list

        # TODO make these async?
        warns = dict()

        if sources is None:
            sources = [e for e in EventSource]

        for source in sources:
            warns[source] = self.get_warning_by_source(source)
            # warns[source] = self.call_dict[source]()

        return warns

    def poll_updates(self, sources=None):

        snap = self.get_warning_snapshot(sources)
        print(snap)

        for source_type, warns in snap.items():

            for warn in warns:
                # build event for warning

                warn_details = self.get_warning_info(warn['id'])
                warn_geojson = self.get_warning_info_geojson(warn['id'])

                # builder function TODO ?
                event = NinaEvent(EventSource[source_type], warn, warn_details, warn_geojson)
                self.bird_client.new_nina_event(event)

        # TODO filter for new ones (time? cache?)
        # TODO

    def request_json_from_url(self, url):
        response = requests.get(url)
        if not response.ok:
            print("Cant get " + url)
            return None

        return response.json()

    def get_warning_by_source(self, source: EventSource):

        base_url = self.bird_client.cfg.nina.api_endpoint
        call_url = base_url + source.value + '/mapData.json'

        return self.request_json_from_url(call_url)

    def get_warning_info(self, identifier):
        base_url = self.bird_client.cfg.nina.api_endpoint
        call_url = base_url + f'warnings/{identifier}.json'

        return self.request_json_from_url(call_url)

    def get_warning_info_geojson(self, identifier):
        base_url = self.bird_client.cfg.nina.api_endpoint
        call_url = base_url + f'warnings/{identifier}.geojson'

        return self.request_json_from_url(call_url)


class LocalNina(Nina):

    def __init__(self, client):
        super().__init__(client)

        self.local_base_path = 'test/'
        pass

    def get_warning_by_source(self, source):
        path = self.local_base_path + source.value + '/mapData.json'
        f = open(path)
        data = json.load(f)
        f.close()
        return data

from datetime import datetime, timedelta
import configparser, os
from warnexception import safe_read_cast

DEFAULT_CONFIG_PATH = 'client.cfg'

class GeneralConfig:

    def __init__(self, config_dict):
        self.debug_log = safe_read_cast(config_dict, 'general', 'debug_log', str)
        self.posting_log = safe_read_cast(config_dict, 'general', 'posting_log', str)

    def __repr__(self):
        return str(self.__dict__)
class NinaConfig:

    def __init__(self, config_dict):
        self.poll_rate = timedelta(seconds=safe_read_cast(config_dict, 'nina', 'poll_interval_s', float, 5.0))
        self.api_endpoint = safe_read_cast(config_dict, 'nina', 'nina_api_endpoint', str)
        self.test_mode = (safe_read_cast(config_dict, 'nina', 'test_mode', int, 0) == 1)

    def __repr__(self):
        return str(self.__dict__)


class MapConfig:

    def __init__(self, config_dict):
        self.api_endpoint = safe_read_cast(config_dict, 'mapbox', 'mapbox_api_endpoint', str)
        self.key_file = safe_read_cast(config_dict, 'mapbox', 'api_access_token_file', str)
        self.test_mode = (safe_read_cast(config_dict, 'mapbox', 'test_mode', int, 0) == 1)
        self.width = safe_read_cast(config_dict, 'mapbox', 'width', int, 500)
        self.height = safe_read_cast(config_dict, 'mapbox', 'height', int, 500)
        self.double_resolution = (safe_read_cast(config_dict, 'mapbox', 'double_resolution', int, 0) == 1)
        self.scale = safe_read_cast(config_dict, 'mapbox', 'map_scale_factor', float, 1.0)

    def __repr__(self):
        return str(self.__dict__)


class TwitterConfig:

    def __init__(self, config_dict):
        self.api_key_file = safe_read_cast(config_dict, 'twitter', 'api_key_file', str)
        self.api_key_secret_file = safe_read_cast(config_dict, 'twitter', 'api_key_secret_file', str)
        self.bearer_token_file = safe_read_cast(config_dict, 'twitter', 'bearer_token_file', str)
        self.access_token_file = safe_read_cast(config_dict, 'twitter', 'access_token_file', str)
        self.access_token_secret_file = safe_read_cast(config_dict, 'twitter', 'access_token_secret_file', str)

    def __repr__(self):
        return str(self.__dict__)


class WarnBirdClientConfig:

    def __init__(self, path=None):
        config_data_dict = WarnBirdClientConfig.load_config_file(path)

        self.general = GeneralConfig(config_data_dict)
        self.nina = NinaConfig(config_data_dict)
        self.map = MapConfig(config_data_dict)
        self.twitter = TwitterConfig(config_data_dict)

    def __repr__(self):
        return str(self.__dict__)

    def apply_args(self, args=None):
        pass  # TODO

    @staticmethod
    def load_config_file(path=None):  # returns dict of sections, with dict of items

        if path is None:
            path = DEFAULT_CONFIG_PATH

        config = configparser.ConfigParser()
        config.read(path)

        # convert to dict
        my_config_parser_dict = {s: dict(config.items(s)) for s in config.sections()}
        return my_config_parser_dict

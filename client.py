from datetime import timedelta
import configparser
from warnexception import safe_read_cast

from nina_api import Nina

DEFAULT_CONFIG_PATH = 'client.cfg'
class WarnBirdClientConfig:

    def __init__(self, path=None):
        config_data_dict = WarnBirdClientConfig.load_config_file(path)

        self.poll_rate = timedelta(seconds=safe_read_cast(config_data_dict, 'nina', 'poll_interval_s', float, 5.0))
        self.nina_api_endpoint = safe_read_cast(config_data_dict, 'nina', 'nina_api_endpoint', str)

    def __str__(self):
        return str(self.__dict__)

    def apply_args(self, args=None):
        pass # TODO

    @staticmethod
    def load_config_file(path=None): # returns dict of sections, with dict of items

        if path is None:
            path = DEFAULT_CONFIG_PATH

        config = configparser.ConfigParser()
        config.read(path)

        # convert to dict
        my_config_parser_dict = {s: dict(config.items(s)) for s in config.sections()}
        return my_config_parser_dict


class WarnBirdClient:

    def __init__(self, config_fp=None, args=None):
        self.cfg = WarnBirdClientConfig(config_fp)
        self.cfg.apply_args(args)

        # setup nina API
        self.nina = Nina(self.cfg)

        # setup twitter API
        # setup_twitter_api()

        # setup maps API
        # setup_maps_api()




    def start(self):
        print("Start Client with config")
        print(self.cfg)

        # TODO poll
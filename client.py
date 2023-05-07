from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from config import WarnBirdClientConfig
import pprint
import logging

from nina_api import Nina, LocalNina
from maps_api import MapBox
from twitter_api import Twitter, TwitterPostEvent
from nina_event import NinaEvent, EventSource
from posting_logger import PostingLogger


class WarnBirdClient:

    def __init__(self, config_fp=None, args=None):
        self.cfg = WarnBirdClientConfig(config_fp)
        self.cfg.apply_args(args)

        # setup logger for client
        logging.basicConfig(
            format='%(asctime)s %(levelname)s: %(message)s',
            level=logging.DEBUG,
            filename=self.cfg.general.debug_log,
        )
        debug_logger = logging.getLogger()
        debug_logger.addHandler(logging.StreamHandler())


        # TODO maybe singleton if necessary
        self.posting_logger = PostingLogger(self.cfg.general.posting_log)

        # setup nina API
        if self.cfg.nina.test_mode:
            self.nina = LocalNina(self) # TODO can we just put cfg.nina here instead of client?
        else:
            self.nina = Nina(self)

        # setup twitter API
        self.twitter = Twitter(self.cfg.twitter)

        # setup_twitter_api()

        # setup maps API
        self.mapbox = MapBox(self.cfg.map)
        # setup_maps_api()

        self.scheduler = BlockingScheduler()

    def start(self):
        print("Start Client with config")
        pprint.pprint(self.cfg)

        self.scheduler.add_job(self.update, 'interval', [None],  # TODO parse sources from config?
                               next_run_time=datetime.now(), seconds=self.cfg.nina.poll_rate.seconds)
        self.scheduler.start()

        # TODO

        # TODO poll

    def update(self, sources=None):

        self.nina.poll_updates(sources=sources)
        if self.cfg.nina.test_mode:
            self.scheduler.shutdown(wait=False)

    def new_nina_event(self, event: NinaEvent):
        # callback function for new events

        if self.posting_logger.already_posted(event):
            return

        # TODO
        # history = get_history_if_present(event)

        # TODO event class. maybe history etc.
        print(event.source)
        print(event.summary)
        print(event.details)
        print(event.geo_data)

        map_image = self.mapbox.get_map(event, self.cfg.map)
        print(map_image)
        # if map_image is not None:

        post = TwitterPostEvent(event, map_image)
        self.twitter.post(post)


        print("--------------------")


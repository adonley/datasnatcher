import logging

from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from poloniex import Poloniex
import pymongo

from .websocket_ticker import WAMPTicker


class PoloniexOperator(object):
    def __init__(self, api_key=None, api_secret=None):
        self._logger = logging.getLogger("PoloneixOperator")
        if api_key is None or api_key == "":
            self._logger.warn("apiKey was None or empty string")
        if api_secret is None or api_secret == "":
            self._logger.warn("apiKey was None or empty string")

        self._api_key = api_key
        self._api_secret = api_secret
        self._app_runner = ApplicationRunner(u"wss://api.poloniex.com:443", u"realm1")
        self._app_process = None
        self._db = pymongo.MongoClient().poloniex['ticker']
        self._poloniex = Poloniex(self._api_key, self._api_secret)
        self._running = False

    def __call__(self, market='USDT_BTC'):
        """ returns ticker from mongo """
        return self._db.find_one({'_id': market})

    def start(self):
        self._logger.info("Starting poloniex ticker subscription...")
        self._running = True
        self._app_runner.run(WAMPTicker)
        self._logger.info("Started poloniex ticker subscription")

    def stop(self):
        self._logger.info("Stopping poloniex ticker subscription")
        self._running = False


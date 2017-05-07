import logging

import asyncio
from autobahn.asyncio.wamp import ApplicationSession
# from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
# from twisted.internet.defer import inlineCallbacks
# from twisted.internet import reactor
from pymongo import MongoClient
from poloniex import Poloniex


class WAMPTicker(ApplicationSession):
    """ Subscribes to the 'ticker' push api and saves pushed data into a mongodb """

    async def onJoin(self, details):
        self._db = MongoClient().poloniex['ticker']
        # TODO: This is a drop --> prob don't want to do this going forward
        self._db.drop()
        # open/create poloniex database, ticker collection/table
        init_tick = Poloniex().returnTicker()
        for market in init_tick:
            init_tick[market]['_id'] = market
            self._db.insert_one(init_tick[market])
        await self.subscribe(self.on_tick, u'ticker')
        print("Subscribed to poloniex ticker")

    def on_tick(self, *data):
        self._db.insert_one(
            {
                'market': data[0],
                'last': data[1],
                'lowestAsk': data[2],
                'highestBid': data[3],
                'percentChange': data[4],
                'baseVolume': data[5],
                'quoteVolume': data[6],
                'isFrozen': data[7],
                'high24hr': data[8],
                'low24hr': data[9]
            }
        )
        print(data)

    def onDisconnect(self):
        pass

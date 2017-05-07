import json
import logging
from multiprocessing import Process
from time import sleep
import threading

import asyncio
from twisted.internet import reactor
import concurrent.futures
from poloniexlibs.poloniex_operator import PoloniexOperator

LOGGER = logging.getLogger('main')


def main():
    print("Hi there, I'm a python program which means I'm consensual. Just like Atari. Everything at Atari was 100% consensual.\n")
    config, error = read_config()
    if error:
        LOGGER.error("Couldn't parse the configuration file correctly. Exiting.\n")
        exit(-1)

    try:
        # Start poloniex ticker process if the configuration is present
        if config.get("poloniex"):
            run_poloniex(config["poloniex"]["apiKey"], config["poloniex"]["apiSecret"])
    except KeyboardInterrupt:
        pass
    exit(0)


def read_config(location=None):
    """
    Reads in the configuration file for
    :param location: location of the configuration file
    :return: (configData, error)
    """
    data_location = location if location else "config.json"
    data = None
    LOGGER.info("Attempting to open data config file: " + data_location)
    try:
        with open(data_location) as data_file:
            data = json.load(data_file)
    except Exception as e:
        print(e.message)
        return None, e
    return data, None


def run_poloniex(api_key, api_secret):
    LOGGER.info("Found poloniex configuration, running poloniex operator.")
    poloniex_operator = PoloniexOperator(api_key, api_secret)
    poloniex_operator.start()

if __name__ == "__main__":
    main()

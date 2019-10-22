import logging

from .api_test import api_test

logging.basicConfig(
    format='%(asctime)s (%(levelname)s): %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S',
    level=logging.INFO
)

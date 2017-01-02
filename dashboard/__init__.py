from main import *
import bottle
import logging
import os

bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'views'))
logging.info(bottle.TEMPLATE_PATH)

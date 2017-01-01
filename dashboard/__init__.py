from main import *
import bottle
import os

bottle.TEMPLATE_PATH.append(os.path.join(os.path.dirname(__file__), 'views'))

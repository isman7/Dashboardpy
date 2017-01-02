from __future__ import unicode_literals, print_function
from dashboard import Dashboard, page
import bottle
import os
import begin
import ConfigParser

cfg = ConfigParser.ConfigParser()

# The server routine starts here:
abspath = os.path.abspath(".")
print("The absolute path to server program is: {}".format(abspath))

board = Dashboard()


@board.route('/')
@board.route('/home/')
@board.route('/home', name="main_page")
@board.page('main_menu')
def index():
    pass


@board.route('/page/', name="example")
@board.page('example')
def do_stuff():
    pass


@begin.start(auto_convert=True)
@begin.logging
def main(host='localhost', port='10010', config_path="settings.ini"):

    cfg.read(config_path)
    board.set_config(cfg)

    board.main_menu.put("example", board.pages.get('example'))
    bottle.run(board, host=host, port=port, debug=True)



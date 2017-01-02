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
@board.route('/home/', name="home")
@bottle.view('dashboard')
def index():
    return board.render_dict(page="home")


@board.route('/facebook/', name="facebook")
@bottle.view('dashboard')
def facebook():
    return board.render_dict(page="social")


@begin.start(auto_convert=True)
@begin.logging
def main(host='localhost', port='10010', config_path="settings.ini"):

    cfg.read(config_path)
    board.set_config(cfg)

    board.pages.put("home", page(url="home",
                                 icon="fa fa-home",
                                 name="home",
                                 title="Home page",
                                 content="This is my main page."))
    board.pages.put("social", page(url="facebook",
                                   icon="fa fa-facebook",
                                   name="social",
                                   title="Facebook account",
                                   content="Link to Facebook maybe?"))
    board.pages.put("search_page", page(url="search",
                                        name="search",
                                        title="Search"))

    board.register_page(page_name="home")
    board.register_page(page_name="social")

    bottle.run(board, host=host, port=port, debug=True)



from __future__ import unicode_literals
import bottle
from collections import OrderedDict
import logging
import ConfigParser
import os


class Dashboard(bottle.Bottle):
    def __init__(self, *args, **kwargs):

        # Dashboard new configurations:
        self.main_menu = kwargs.pop("main_menu", menu())
        self.user_profile = kwargs.pop("user", None)
        self.pages = kwargs.pop("tree", tree())
        self._board_config = kwargs.pop("board_config", ConfigParser.ConfigParser())
        if not self._board_config.sections():
            self._board_config.read(kwargs.pop("config_file", "default_settings.ini"))

        # Here starts Bottle configuration:
        super(Dashboard, self).__init__(*args, **kwargs)

        def server_static(filepath):
            """
            Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
            :param filepath: a valid local path in server.
            :return: returns the file to bottle app.
            """
            return bottle.static_file(filepath, root=os.path.join(os.path.dirname(__file__), 'static'))

        self.route('/static/<filepath:path>', name="static", callback=server_static)

        def search_get():
            return bottle.template("dashboard", self.render_dict(page="search_page"))

        self.route('/search', name='search', callback=search_get)

        def search_post():
            """
            Do search stuff. In this example the query is rendered as plain text inside the page.
            """
            search_string = bottle.request.forms.get("s")
            search_page = self.pages.get("search_page", page(url="search"))
            search_page.content = search_string
            self.pages.put("search_page", search_page)
            return bottle.template("dashboard", self.render_dict(page="search_page"))

        self.route('/search', name='search', method='POST', callback=search_post)

    def set_config(self, new_config):
        logging.info(new_config)
        self._board_config = new_config

    def render_dict(self, **kwargs):
        the_page = kwargs.get("page", None)
        url = kwargs.pop("url", self.get_url)
        return {"url": url,
                "title": self._board_config.get("DEFAULT", "title"),
                "description": self._board_config.get("DEFAULT", "description"),
                "color": self._board_config.get("layout", "color"),
                "layout_options": self._board_config.get("layout", "options"),
                "sidebar_menu": self.main_menu.render(url=url, **kwargs),
                "page": self.pages.get(the_page, page()).render()}

    def register_page(self, **kwargs):
        the_page = self.pages.get(kwargs.get("page_name"))
        the_menu = kwargs.get("menu", self.main_menu)
        logging.info(page)
        the_menu.put(the_page.name, the_page)
        return the_menu


class page(object):
    def __init__(self, **kwargs):
        self.bottle = kwargs.pop("bottle", None)
        self.title = kwargs.pop("title", "Default page")
        self.description = kwargs.pop("description", "A single page")
        self.name = kwargs.pop("name", "default-page")
        self.icon = kwargs.pop("icon", "fa fa-link")
        self.url = kwargs.pop("url", "#")
        self.content = kwargs.pop("content", "The content")

    def render(self):
        return bottle.template("page",
                               title=self.title,
                               description=self.description,
                               page_content=self.content)


class tree(OrderedDict):
    def __init__(self, *args, **kwargs):
        super(tree, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)


class menu(OrderedDict):
    def __init__(self, *args, **kwargs):
        self.bottle = kwargs.pop("bottle", None)
        self.title = kwargs.pop("title", "Main menu")
        self.name = kwargs.pop("name", "main-menu")
        super(menu, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        self.__setitem__(key, item, **kwargs)

    def render(self, **kwargs):
        active = kwargs.pop("page", None)
        url = kwargs.pop("url")
        return bottle.template("menu",
                               url=url,
                               active_page=active,
                               title=self.title,
                               entries=self.items())

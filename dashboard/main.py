import bottle
from collections import OrderedDict
import logging
import configparser
import os


class Dashboard(bottle.Bottle):
    def __init__(self, *args, **kwargs):

        # Dashboard new configurations:
        self._board_config = kwargs.pop("board_config", configparser.ConfigParser())
        if not self._board_config.sections():
            self._board_config.read(kwargs.pop("config_file", "default_settings.ini"))

        super(Dashboard, self).__init__(*args, **kwargs)

        self.pages = kwargs.pop("tree", tree())
        self.main_menu = kwargs.pop("main_menu", menu())
        self.main_page = kwargs.pop("main_page", page(title="Home page",
                                                      name="main_page",
                                                      description="This is the main page.",
                                                      icon="fa fa-home",
                                                      content="This is the dashboard!"
                                                      ))

        self.register_page(self.main_page)
        self.main_menu.put(self.main_page.name, self.main_page)

        self.user_profile = kwargs.pop("user", None)

        @self.route('/static/<filepath:path>', name="static")
        def server_static(filepath):
            """
            Enables support to CSS, JS, images, etc. Links the public URL with the real server files and serve them.
            :param filepath: a valid local path in server.
            :return: returns the file to bottle app.
            """
            return bottle.static_file(filepath, root=os.path.join(os.path.dirname(__file__), 'static'))

        @self.route('/search', name='search')
        def search_get():
            return bottle.template("dashboard", self.render_dict(page="search_page"))

        @self.route('/search', name='search', method='POST')
        def search_post():
            """
            Do search stuff. In this example the query is rendered as plain text inside the page.
            """
            search_string = bottle.request.forms.get("s")
            search_page = self.pages.get("search_page", page(url="search"))
            search_page.content = search_string
            self.pages.put("search_page", search_page)
            return bottle.template("dashboard", self.render_dict(page="search_page"))

        @self.error(404)
        def error404(error):
            return 'Nothing here, sorry'

    def set_config(self, new_config):
        logging.info(new_config)
        self._board_config = new_config

    def render_dict(self, **kwargs):
        the_page = kwargs.get("page", None)
        url = kwargs.pop("url", self.get_url)
        return {"url": url,
                "title": self._board_config.get("DEFAULT", "title"),
                "description": self._board_config.get("DEFAULT", "description"),
                "color": self._board_config.get("DEFAULT", "color"),
                "layout_options": self._board_config.get("DEFAULT", "layout_options"),
                "main_page_name": self.main_page.name,
                "sidebar_menu": self.main_menu.render(url=url, **kwargs),
                "page": self.pages.get(the_page, page()).render()}

    def register_page(self, aPage, **kwargs):
        # the_page = self.pages.get(kwargs.get("page_name"))
        # the_menu = kwargs.get("menu", self.main_menu)
        # logging.info(page)
        # the_menu.put(the_page.name, the_page)
        if issubclass(aPage.__class__, page):
            self.pages.put(aPage.name, aPage)
        return self.pages

    def page(self, name='the_page'):
        if name not in self.pages:
            self.register_page(page(name=name))

        def decorator(func):
            @bottle.view('dashboard')
            def decorated():
                func()
                return self.render_dict(page=name)
            return decorated
        return decorator


class page(object):
    def __init__(self, **kwargs):
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
        self.title = kwargs.pop("title", "Main menu")
        self.name = kwargs.pop("name", "main-menu")
        super(menu, self).__init__(*args, **kwargs)

    def put(self, key, item, **kwargs):
        if issubclass(item.__class__, page):
            self.__setitem__(key, item, **kwargs)
        else:
            raise TypeError

    def render(self, **kwargs):
        active = kwargs.pop("page", None)
        url = kwargs.pop("url")
        return bottle.template("menu",
                               url=url,
                               active_page=active,
                               title=self.title,
                               entries=self.items())

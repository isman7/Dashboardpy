# Dashboard.py

Dashboard.py is Bootle-based Python module to provide Dashboard interfaces for web development using the [AdminLTE 
Dashboard](https://github.com/almasaeed2010/AdminLTE). Dashboard.py aims to integrate all  the Bootstrap, Font 
Awesome, JavaScript Charts (such as ChartJS or Morris Charts) that AdminLTE provides into an interactive API. 

## Installation

As it is not yet uploaded to PyPI (soon!), you must download from git and perform the installation *manually*, using 
the `setup.py` way: 

```
git clone https://github.com/isman7/Dashboardpy.git
cd Dashboardpy
pip install -r requirements.txt
pip install -e .
```

## Basic Usage

### Using CLI script (with begins)

Simply do, 

```
python scripts/cli.py
```

### Using the Bottle app API

A `dashboard()` instance is basically an extension of a `bottle()` application including several pre-defined `routes`,
and `views`. Also decorator-like syntax is provided to render the dashboard.

Start calling a the `Dashboard` class:

```
from dashboard import Dashboard

board = Dashboard()
```  
 
The `board` object is a subclass of `Bottle`  app (i. e. you can use `@board.route` decorators). By default, the 
`Dashboard` defines a main page of the dashboard, all the dashboard pages are stored in `Dashboard.pages` attribute, 
a subclass of `OrderedDict` object. The pages have to be routed with `bottle` syntax:
 
```
@board.route('/', name="main_page")
@board.page('main_menu')
def index():
    pass
```

Notice, that a new `@Dashboard.page` decorator has been added, it is an extension idea of the `@Bottle.view` decorator 
that correctly renders the dashboard page. This decorator is used also for defining new pages into the dashboard, as 
follows: 

```
@board.route('/page/', name="example")
@board.page('example')
def do_stuff():
    pass
```

The page `example` has beed added to the `board` app and also routed to `/page/`. Finally, new pages have to be added
 to the main menu:
 
```
board.main_menu.put("example", board.pages.get('example'))
``` 

And finally,

```
bottle.run(board, host=host, port=port, debug=True)
```



## TODO list

- Review `@Dashboard.page` decorator to accept the return of page content as valid html to render the template. Also,
 add support for authomatic insetion into the main menu if desired. 
- Try to subclass `main_menu` and `tree` from a `collections.deque` and not from `collections.OrderedDict`.  
- Add support for a grid system (that will compile as Bootstrap 3 grid). Must evaluate a proper syntax (i. e. 
`matplotlit.pyplot.subplot`).
- Add suport for a `widget` object to implement AdminLTE widgets inside the Dashboard pages.
- Some of the widget require the implementation of JavaScript, for example charts, automatically process the 
JavaScript dependencies inside the package (know all are imported). 
- Study the use of RapydScript to encode dynamically from Python-like source code additional JavaScript. 


## Disclaimer section:
> *Dashboard.py is almost in its initial development stage.*
> *Dashboard.py is being developed for fun, as a base for further own projects!*
> *I am not a software engineer, I came into Python from physics and telecommunications worlds.*


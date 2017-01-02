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


@board.route('/chart', name='chart')
@bottle.view('dashboard_test_chartjs')
def chart():
    return board.render_dict(page="chart")


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

    board.pages.put("chart", page(url="chart",
                                    icon="fa fa-pie-chart",
                                    name="chart",
                                    title="ChartJS"))

    board.register_page(page_name="home")
    board.register_page(page_name="social")
    board.register_page(page_name="chart")

    board.pages.get("chart").content = """
<div class="box box-danger">
    <div class="box-header with-border">
      <h3 class="box-title">Donut Chart</h3>

      <div class="box-tools pull-right">
        <button type="button" class="btn btn-box-tool" data-widget="collapse"><i class="fa fa-minus"></i>
        </button>
        <button type="button" class="btn btn-box-tool" data-widget="remove"><i class="fa fa-times"></i></button>
      </div>
    </div>
    <div class="box-body">
      <canvas id="pieChart" style="height:250px"></canvas>
    </div>
    <!-- /.box-body -->
</div>
    """

    bottle.run(board, host=host, port=port, debug=True)



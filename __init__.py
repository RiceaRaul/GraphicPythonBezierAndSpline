
from bokeh.server.server import Server
from .pages.bezier_curve import modify_doc


# Run the Bokeh server
server  = Server({'/': modify_doc}, port=5001, num_procs=1)
server.start()

server.show("/")
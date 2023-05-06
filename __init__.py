
from bokeh.server.server import Server
from .pages.bezier_curve import modify_doc


# Run the Bokeh server
server  = Server({'/': modify_doc}, port=5001, num_procs=1)
server.start()

# Open the plot in a browser window
server.io_loop.add_callback(server.show, "/")
server.io_loop.start()

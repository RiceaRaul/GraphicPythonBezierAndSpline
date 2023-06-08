from bokeh.embed import server_document
from bokeh.server.server import Server
from flask import Flask, render_template
from tornado.ioloop import IOLoop
from threading import Thread
from pages import bezier_curve, spline_curve

app = Flask(__name__)

routes = {
    "/app": bezier_curve.modify_doc,
    "/spline": spline_curve.modify_doc
}


@app.route("/", methods=["GET"])
def bkapp_page():
    script = server_document("http://127.0.0.1:5007/app")
    return render_template("template.html", script=script)


@app.route("/spline", methods=["GET"])
def bsplinekapp_page():
    script = server_document("http://127.0.0.1:5007/spline")
    return render_template("template.html", script=script)


def bk_worker():
    server = Server(
        routes,
        io_loop=IOLoop(),
        port=5007,
        allow_websocket_origin=["127.0.0.1:8001"],
    )
    server.start()
    server.io_loop.start()


if __name__ == "__main__":
    Thread(target=bk_worker).start()
    app.run(port=8001)

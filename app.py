from bokeh.embed import server_document
from bokeh.layouts import grid, column
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.server.server import Server
from flask import Flask, render_template
from tornado.ioloop import IOLoop
from threading import Thread
import pandas as pd
from  pages import modify_doc

app = Flask(__name__)


@app.route("/", methods=["GET"])
def bkapp_page():
    script = server_document("http://127.0.0.1:5007/app")
    return render_template("template.html", script=script)


def bk_worker():
    server = Server({'/app': modify_doc},
                    io_loop=IOLoop(),
                    port=5007,
                    allow_websocket_origin=["127.0.0.1:8001"])
    server.start()
    server.io_loop.start()


def generate_app(doc):
    df = pd.read_csv("example.csv", index_col=0)
    data_source = ColumnDataSource(df)
    line_plot1 = figure(sizing_mode="stretch_both")
    line_plot1.line(
        source=data_source,
        x="x",
        y="y",
    )
    line_plot2 = figure(sizing_mode="stretch_both")
    line_plot2.line(
        source=data_source,
        x="y",
        y="x",
    )
    sliders = [
        Slider(start=0, end=5, value=5, step=1, title="Max X"),
        Slider(start=0, end=25, value=25, step=1, title="Max Y"),
    ]

    def update_graph(attr, old, new):
        x_max = sliders[0].value
        y_max = sliders[1].value
        filtered_df = df[(df["x"] <= x_max) & (df["y"] <= y_max)]
        new_data = ColumnDataSource(filtered_df).data
        data_source.data = new_data

    for slider in sliders:
        slider.on_change("value", update_graph)

    layout = grid(
        [
            [
                line_plot1,
                column(sliders),
            ],
            line_plot2,
        ],
        sizing_mode="stretch_both",
    )

    doc.add_root(layout)


if __name__ == '__main__':
    Thread(target=bk_worker).start()
    app.run(port=8001)
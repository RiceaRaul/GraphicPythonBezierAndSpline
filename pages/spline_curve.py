from bokeh.plotting import figure
from bokeh.models import (
    ColumnDataSource,
    PointDrawTool,
    Slider,
    FileInput,
    Div
)
from bokeh.layouts import Column, Row
from bokeh.models.widgets import DataTable
import numpy as np
from logic.b_spline import BSplineCurve
from utils.tabledata import getCols
from utils.error_dialog import DialogModal
import io
from pybase64 import b64decode
import pandas as pd

def modify_doc(doc):
    # degree = 4
    # Create a new plot with the title and axis labels
    p = figure(
        title="Scatter Plot with B-spline Curve", x_axis_label="X", y_axis_label="Y"
    )

    degree = Slider(start=1, end=100, value=1, step=1, title="Degree")
    dialog = DialogModal("Error Modal")

    # Create the control points for the B-spline curve
    control_x = []
    control_y = []

    control_source = ColumnDataSource(data=dict(x=control_x, y=control_y))

    # Add the control points as scatter glyphs
    control_scatter = p.scatter("x", "y", source=control_source, size=10, color="blue")
    p.line("x", "y", source=control_source, line_width=2, color="gray")

    # Enable point drawing tool for control points
    control_draw_tool = PointDrawTool(renderers=[control_scatter], empty_value="purple")
    p.add_tools(control_draw_tool)
    p.toolbar.active_tap = control_draw_tool

    curve_source = ColumnDataSource(data=dict(x=[], y=[]))
    p.line("x", "y", source=curve_source, line_width=2, color="red")

    #callbacks
    def update_curve():
        currentDegree = degree.value
        control_x = [x for x in control_source.data["x"]]
        control_y = [y for y in control_source.data["y"]]
        control_points = np.column_stack((control_x, control_y))
        degree.end = len(control_points) - 1
        if len(control_points) > 0:
            print(control_points)
            p = BSplineCurve.bspline_basis(len(control_points), 100, currentDegree)
            points_basis = np.dot(p, control_points)
            x, y = points_basis.T
            curve_source.data = {"x": x, "y": y}

    def handle_file_upload(attr, old, new):
        degree.value = 1
        file = io.BytesIO(b64decode(new))
        data_frame = pd.read_csv(file, sep=",", header=0)
        data_source = data_frame.to_dict(orient="list")
        invalid_x_row = np.isnan(data_source["x"]).argmax()
        newFileInput = FileInput(accept=".csv")
        newFileInput.on_change("value", handle_file_upload)
        file_group.children[1] = newFileInput
        
        if invalid_x_row > -1:
            dialog.openDialog(f"Verifica valoare pentru x pe randul {invalid_x_row + 2}")
            return

        invalid_y_row = np.isnan(data_source["y"]).argmax()
        if invalid_y_row > -1:
            dialog.openDialog(f"Verifica valoare pentru y pe randul {invalid_y_row + 2}")
            return

        control_source.data = data_source
        update_curve()

    control_source.on_change("data", lambda attr, old, new: update_curve())
    degree.on_change("value", lambda attr, old, new: update_curve())
    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1
    p.x_range.start = 0
    p.x_range.end = 5
    p.y_range.start = 0
    p.y_range.end = 7

    update_curve()

    file_input_title = Div(text="<b>Choose an input file:</b>")
    file_input = FileInput(accept=".csv")
    file_input.on_change("value", handle_file_upload)
    file_group = Column(file_input_title,file_input)

    data_table = DataTable(
        source=control_source, columns=getCols(), height=300, editable=True
    )

    right_col_first_row = Row(degree,file_group)
    right_col = Column(right_col_first_row,data_table)
    row_buttons = Row(p, right_col)
    doc.add_root(row_buttons)
    doc.add_root(dialog.getDialog())

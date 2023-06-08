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
from utils.input_points import InputPoints
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


    def addPoint():
        x = input_group.get_x_value()
        y = input_group.get_y_value()
        if x.strip().replace('.', '', 1).isdigit():
            x_value = float(x.strip())
        else:
            dialog.openDialog("Adauga un numar valid pentru x! Ex: 1, 1.5.")
            return

        if y.strip().replace('.', '', 1).isdigit():
            y_value = float(y.strip())
        else:
            dialog.openDialog("Adauga un numar valid pentru y! Ex: 1, 1.5.")
            return

        control_source.stream({"x": [x_value], "y": [y_value]})
        update_curve()

    def handle_file_upload(attr, old, new):
        if file_group.children[1].value:
            extension = file_group.children[1].filename.split(".")[-1]
        if extension.lower() != "csv":
            dialog.openDialog("Trebuie urcat un fisier csv.")
        else:
            file = io.BytesIO(b64decode(file_group.children[1].value))
            data_frame = pd.read_csv(file, sep=",", header=0)
            data_source = data_frame.to_dict(orient="list")

            newFileInput = FileInput()
            newFileInput.on_change("filename", handle_file_upload)
            file_group.children[1] = newFileInput

            invalid_x_row = np.isnan(data_source["x"])
            if invalid_x_row[invalid_x_row.argmax()]:
                dialog.openDialog(f"Verifica valoare pentru x pe randul {invalid_x_row.argmax() + 2}")
                return

            invalid_y_row = np.isnan(data_source["y"])
            if invalid_y_row[invalid_y_row.argmax()]:
                dialog.openDialog(f"Verifica valoare pentru y pe randul {invalid_y_row.argmax() + 2}")
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
    file_group = Column(file_input_title,file_input)
    file_group.children[1].on_change("filename", handle_file_upload)

    data_table = DataTable(
        source=control_source, columns=getCols(), height=300, editable=True
    )
    input_group = InputPoints(addPoint)

    right_col_first_row = Row(degree,file_group)
    right_col = Column(right_col_first_row, input_group.get_input_group(), data_table)
    row_buttons = Row(p, right_col)
    doc.add_root(row_buttons)
    doc.add_root(dialog.getDialog())

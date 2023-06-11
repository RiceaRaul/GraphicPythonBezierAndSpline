from bokeh.plotting import figure
from bokeh.models import (
    ColumnDataSource,
    PointDrawTool,
    FileInput,
    Div,
    Button
)
from bokeh.layouts import Column, Row
from bokeh.models.widgets import DataTable
import numpy as np
from logic.bezier_curve import BezierCurve
import pandas as pd
from pybase64 import b64decode
import io
from utils.tabledata import getCols
from utils.error_dialog import DialogModal
from utils.input_points import InputPoints
def modify_doc(doc):
    # Create a new plot with the title and axis labels
    p = figure(
        title="Grafic  Bezier Curve", x_axis_label="X", y_axis_label="Y"
    )

    # Create the control points for the Bezier curve
    control_x = []
    control_y = []
    control_points = np.column_stack((control_x, control_y))
    dialog = DialogModal("Error Modal")
    control_source = ColumnDataSource(data=dict(x=control_x, y=control_y))
    if len(control_source.data["x"]) >= 3 and len(control_source.data["y"]) >= 3:
        t = np.linspace(0, 1, 101)
        D = control_points[0] + t[:, np.newaxis] * (
            control_points[1] - control_points[0]
        )
        E = control_points[1] + t[:, np.newaxis] * (
            control_points[2] - control_points[1]
        )
        F = D + t[:, np.newaxis] * (E - D)

        points_source = ColumnDataSource(
            data=dict(
                x=D[:, 0], y=D[:, 1], x2=E[:, 0], y2=E[:, 1], x3=F[:, 0], y3=F[:, 1]
            )
        )
    else:
        points_source = ColumnDataSource(
            data=dict(x=[], y=[], x2=[], y2=[], x3=[], y3=[])
        )

    # Add the control points as scatter glyphs
    control_scatter = p.scatter("x", "y", source=control_source, size=10, color="blue")
    p.line("x", "y", source=control_source, line_width=2, color="gray")

    # Enable point drawing tool for control points
    control_draw_tool = PointDrawTool(renderers=[control_scatter], empty_value="purple")
    p.add_tools(control_draw_tool)
    p.toolbar.active_tap = control_draw_tool

    # Create a Line glyph for the Bezier curve
    curve_source = ColumnDataSource(data=dict(x=[], y=[]))
    curve = p.line("x", "y", source=curve_source, line_width=2, color="red")

    bezier_curve = BezierCurve(control_points)

    data_table = DataTable(
        source=control_source, columns=getCols(), height=300, editable=True
    )

    # Python callback to update the data sources and redraw the curve

    def update_curve():
        control_x = [float(x) for x in control_source.data["x"]]
        control_y = [float(y) for y in control_source.data["y"]]
        control_points = np.column_stack((control_x, control_y))
        bezier_curve.control_points = control_points
        t = np.linspace(0, 1, 101)
        curve_points = bezier_curve.calculate_curve_points(t)

        if len(control_source.data["x"]) >= 3 and len(control_source.data["y"]) >= 3:
            D = control_points[0] + t[:, np.newaxis] * (
                control_points[1] - control_points[0]
            )
            E = control_points[1] + t[:, np.newaxis] * (
                control_points[2] - control_points[1]
            )
            F = D + t[:, np.newaxis] * (E - D)
            points_source.data = {
                "x": D[:, 0],
                "y": D[:, 1],
                "x2": E[:, 0],
                "y2": E[:, 1],
                "x3": F[:, 0],
                "y3": F[:, 1],
            }

        curve_source.data = {"x": curve_points[:, 0], "y": curve_points[:, 1]}

    file_input_title = Div(text="<b>Alege un fisier:</b>")

    file_input = FileInput()

    # Python callback to handle file selection
    def handle_file_upload(attr, old, new):
        print(attr)
        if row_buttons.children[0].value:
            extension = row_buttons.children[0].filename.split(".")[-1]
            print(extension)
            if extension.lower() != "csv":
                dialog.openDialog("Trebuie urcat un fisier csv.")
            else:
                file = io.BytesIO(b64decode(row_buttons.children[0].value))
                data_frame = pd.read_csv(file, sep=",", header=0)
                data_source = data_frame.to_dict(orient="list")

                newFileInput = FileInput()
                row_buttons.children[0] = newFileInput
                row_buttons.children[0].on_change("filename", handle_file_upload)

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
        
    control_source.on_change("data", lambda attr, old, new: update_curve())

    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1
    p.x_range.start = 0
    p.x_range.end = 5
    p.y_range.start = 0
    p.y_range.end = 7

    update_curve()
    # Create a curdoc and add the plot to it
    def add_point():
        new_x = 0
        new_y = 0
        new_data = dict(control_source.data)
        new_data["x"].append(new_x)
        new_data["y"].append(new_y)
        control_source.data = new_data

    def del_point():
        if(len(control_source.selected.indices)):
            new_data = dict(control_source.data)
            new_data['x'].pop(control_source.selected.indices[0])
            new_data['y'].pop(control_source.selected.indices[0])
            control_source.data = new_data
            control_source.selected.indices=[]
        else:
            dialog.openDialog("Nu este selectat niciun punct !")
        

    input_group = InputPoints(addPoint)
    button = Button(label="Adauga punct", button_type="success")
    button.on_click(add_point)
    del_button = Button(label="Sterge Punct", button_type="danger")
    del_button.on_click(del_point)
    button_reset = Button(label="Reseteaza Grafic", button_type="warning")
    button_reset.on_click(lambda: (control_source.data.update(dict(x=[], y=[])), curve_source.data.update(dict(x=[], y=[]))))

    row_buttons = Row(file_input, button , del_button,button_reset)
    file_input_box = Column(file_input_title, row_buttons, input_group.get_input_group())

    row_buttons.children[0].on_change("filename", handle_file_upload)
    table_column = Column(Div(text="<b>Tabel de coordonate:</b>"),data_table)
    row = Row(p, Column(file_input_box,table_column))
    doc.add_root(row)
    doc.add_root(dialog.getDialog())

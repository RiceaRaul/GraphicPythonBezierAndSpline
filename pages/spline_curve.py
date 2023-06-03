from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PointDrawTool, Slider,CustomJS,FileInput, Div, TableColumn, NumberFormatter, Button, IntEditor
from bokeh.layouts import Column, Row
from bokeh.models.widgets import DataTable
import numpy as np
from logic import BSplineCurve
import pandas as pd
from pybase64 import b64decode
import io

def modify_doc(doc):
    #degree = 4
    # Create a new plot with the title and axis labels
    p = figure(title="Scatter Plot with B-spline Curve", x_axis_label="X", y_axis_label="Y")
    degree = Slider(start=0, end=100, value=0, step=1, title="Degree")
    # Create the control points for the B-spline curve
    control_x = []
    control_y = []
    control_points = np.column_stack((control_x, control_y))
    
    control_source = ColumnDataSource(data=dict(x=control_x, y=control_y))
    points_source = ColumnDataSource(data=dict(x=[], y=[]))

    # Add the control points as scatter glyphs
    control_scatter = p.scatter('x', 'y', source=control_source, size=10, color='blue')
    p.line('x', 'y', source=control_source, line_width=2, color='gray')

    # Enable point drawing tool for control points
    control_draw_tool = PointDrawTool(renderers=[control_scatter], empty_value='purple')
    p.add_tools(control_draw_tool)
    p.toolbar.active_tap = control_draw_tool

    curve_source = ColumnDataSource(data=dict(x=[], y=[]))
    p.line('x', 'y', source=curve_source, line_width=2, color='red')

    bspline = BSplineCurve()
    def update_curve():
        
        currentDegree = degree.value
        control_x = [x for x in control_source.data['x']]
        control_y = [y for y in control_source.data['y']]
        control_points = np.column_stack((control_x, control_y))
        degree.end = len(control_points)
        if(len(control_points) > 0):
            print(control_points)          
            p = bspline.bspline_basis(len(control_points), 100, currentDegree)
            points_basis = np.dot(p, control_points)
            x,y = points_basis.T
            curve_source.data = {'x': x, 'y': y}

    # Add the callback to the control points data source
    control_source.on_change('data', lambda attr, old, new: update_curve())
    degree.on_change('value', lambda attr,old,new : update_curve())
    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1
    p.x_range.start = 0
    p.x_range.end = 5
    p.y_range.start = 0
    p.y_range.end = 7

    update_curve()

    js_code = """toastr.success("Hello from Toastr!");"""
    # Create a CustomJS callback
    callback = CustomJS(code=js_code)

    # Call the JavaScript function
    callback.execute(None)
    row_buttons = Row(p,degree)
    doc.add_root(row_buttons)

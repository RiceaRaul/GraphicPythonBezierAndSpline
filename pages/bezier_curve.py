from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PointDrawTool
import numpy as np
from logic import BezierCurve

def modify_doc(doc):
    # Create a new plot with the title and axis labels
    p = figure(title="Scatter Plot with Bezier Curve", x_axis_label="X", y_axis_label="Y")

    # Create the control points for the Bezier curve
    control_x = [2, 3, 4]
    control_y = [2, 6, 3]
    control_points = np.column_stack((control_x,control_y))

    # Create a ColumnDataSource for the control points
    control_source = ColumnDataSource(data=dict(x=control_x, y=control_y))

    # Add the control points as scatter glyphs
    control_scatter = p.scatter('x', 'y', source=control_source, size=10, color='blue')

    # Enable point drawing tool for control points
    control_draw_tool = PointDrawTool(renderers=[control_scatter], empty_value='purple')
    p.add_tools(control_draw_tool)
    p.toolbar.active_tap = control_draw_tool

    # Create a Line glyph for the Bezier curve
    curve_source = ColumnDataSource(data=dict(x=[], y=[]))
    curve = p.line('x', 'y', source=curve_source, line_width=2, color='green')

    bezier_curve = BezierCurve(control_points)

    # Python callback to update the data sources and redraw the curve
    def update_curve():
        control_x = control_source.data['x']
        control_y = control_source.data['y']
        control_points = np.column_stack((control_x,control_y))
        bezier_curve.control_points=control_points
        t=np.linspace(0,1,101)
        curve_points = bezier_curve.calculate_curve_points(t)

        curve_source.data = {'x': curve_points[:,0], 'y': curve_points[:,1]}


    # Add the callback to the control points data source
    control_source.on_change('data', lambda attr, old, new: update_curve())

    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1
    p.x_range.start = 0
    p.x_range.end = 5
    p.y_range.start = 0
    p.y_range.end = 7

    update_curve()
    # Create a curdoc and add the plot to it
    doc.add_root(p)
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PointDrawTool, CustomJS
from bokeh.io import curdoc
import numpy as np

def modify_doc(doc):
    # Create a new plot with the title and axis labels
    p = figure(title="Scatter Plot with Bezier Curve", x_axis_label="X", y_axis_label="Y")

    # Create the control points for the Bezier curve
    control_x = [2, 3, 4]
    control_y = [2, 6, 3]

    # Create a ColumnDataSource for the control points
    control_source = ColumnDataSource(data=dict(x=control_x, y=control_y))

    # Add the control points as scatter glyphs
    control_scatter = p.scatter('x', 'y', source=control_source, size=10, color='blue')

    # Enable point drawing tool for control points
    control_draw_tool = PointDrawTool(renderers=[control_scatter], empty_value='black')
    p.add_tools(control_draw_tool)
    p.toolbar.active_tap = control_draw_tool

    # Create a Line glyph for the Bezier curve
    curve_source = ColumnDataSource(data=dict(x=[], y=[]))
    curve = p.line('x', 'y', source=curve_source, line_width=2, color='green')

    # Python callback to update the data sources and redraw the curve
    def update_curve():
        control_x = control_source.data['x']
        control_y = control_source.data['y']

        nPoints = 100  # Number of points on the curve
        curveX = np.zeros(nPoints)
        curveY = np.zeros(nPoints)

        # Calculate the Bezier curve points
        for i in range(nPoints):
            t = i / (nPoints - 1)
            bx = 0
            by = 0

            for j in range(len(control_x)):
                binomial_coeff = np.math.factorial(len(control_x) - 1) / (np.math.factorial(j) * np.math.factorial(len(control_x) - 1 - j))
                factor1 = (1 - t) ** (len(control_x) - 1 - j)
                factor2 = t ** j
                bx += binomial_coeff * factor1 * factor2 * control_x[j]
                by += binomial_coeff * factor1 * factor2 * control_y[j]

            curveX[i] = bx
            curveY[i] = by

        # Update the curve data source
        curve_source.data = {'x': curveX, 'y': curveY}

    # Add the callback to the control points data source
    control_source.on_change('data', lambda attr, old, new: update_curve())

    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1
    p.x_range.start = 0
    p.x_range.end = 5
    p.y_range.start = 0
    p.y_range.end = 7

    # Create a curdoc and add the plot to it
    doc.add_root(p)
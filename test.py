import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PointDrawTool, CustomJS
from bokeh.io import curdoc


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

# JavaScript callback to update the data sources and redraw the curve
callback = CustomJS(args=dict(control_source=control_source, curve_source=curve_source), code="""
    const control_x = control_source.data['x'];
    const control_y = control_source.data['y'];

    const nPoints = 100;  // Number of points on the curve
    const curveX = new Array(nPoints);
    const curveY = new Array(nPoints);

    // Calculate the Bezier curve points
    for (let i = 0; i < nPoints; i++) {
        const t = i / (nPoints - 1);
        let bx = 0;
        let by = 0;

        for (let j = 0; j < control_x.length; j++) {
            const binomialCoeff = factorial(control_x.length - 1) / (factorial(j) * factorial(control_x.length - 1 - j));
            const factor1 = Math.pow(1 - t, control_x.length - 1 - j);
            const factor2 = Math.pow(t, j);
            bx += binomialCoeff * factor1 * factor2 * control_x[j];
            by += binomialCoeff * factor1 * factor2 * control_y[j];
        }

        curveX[i] = bx;
        curveY[i] = by;
    }

    // Update the curve data source
    curve_source.data = { 'x': curveX, 'y': curveY };

    // Helper function to calculate factorial
   
    function factorial(n) {
        if (n === 0 || n === 1) {
            return 1;
        } else {
            return n * factorial(n - 1);
        }
    }

    // Redraw the plot
    curve_source.change.emit();
""")

p.x_range.range_padding = 0.1
p.y_range.range_padding = 0.1
p.x_range.start = 0
p.x_range.end = 5
p.y_range.start = 0
p.y_range.end = 7

# Add the callback to the control points data source
control_source.js_on_change('data', callback)

chart_container = st.empty()

chart_container.bokeh_chart(p, use_container_width=False)



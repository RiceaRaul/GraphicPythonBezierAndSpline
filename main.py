# import streamlit as st
# from bokeh.plotting import figure
# from bokeh.models import ColumnDataSource, PointDrawTool
# from bokeh.models.callbacks import CustomJS
# from bokeh.io import curdoc

# # Prepare the data
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 2, 4, 5]

# # Create a new plot with the title and axis labels
# p = figure(title="Scatter Plot Example", x_axis_label="X", y_axis_label="Y")

# # Create a ColumnDataSource to hold the data
# source = ColumnDataSource(data=dict(x=x, y=y))

# # Add a scatter glyph
# scatter = p.scatter('x', 'y', source=source, size=10, color='red')

# # Enable point drawing tool
# draw_tool = PointDrawTool(renderers=[scatter], empty_value='black')
# p.add_tools(draw_tool)
# p.toolbar.active_tap = draw_tool

# # JavaScript callback to update the data source
# callback = CustomJS(args=dict(source=source), code="""
#     source.data = cb_data.renderer.data_source.data;
# """)

# # Update the data source whenever a point is moved
# scatter.data_source.js_on_change('data', callback)

# # Use Streamlit to display the plot
# st.bokeh_chart(p)

# # Run the Streamlit app
# curdoc().add_root(st)

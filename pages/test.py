from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row
from bokeh.models import Button, TextInput, Dropdown, Slider
from bokeh.models.sources import ColumnDataSource
from bokeh.themes import Theme

def test_doc(doc):
    # Create the figure for the graph
    graph = figure(plot_width=400, plot_height=400)

    # Create a data source for the points
    source = ColumnDataSource(data=dict(x=[], y=[]))

    # Create the dropdown fields
    dropdown_x = Dropdown(label="X Field", menu=[("Option 1", "option1"), ("Option 2", "option2")])
    dropdown_y = Dropdown(label="Y Field", menu=[("Option 1", "option1"), ("Option 2", "option2")])

    # Create the text input fields
    text_input_x = TextInput(title="X Value")
    text_input_y = TextInput(title="Y Value")

    # Create the slider
    slider = Slider(start=0, end=1, value=0.5, step=0.1, title="Slider")

    # Create the button
    button = Button(label="Add Point", button_type="success")

    def add_point():
        x_value = text_input_x.value
        y_value = text_input_y.value
        if x_value and y_value:
            x = float(x_value)
            y = float(y_value)
            source.stream(dict(x=[x], y=[y]))

    button.on_click(add_point)

    # Update the graph with the data from the source
    graph.circle(x='x', y='y', source=source)

    # Set the page background to dark
    dark_theme = Theme(json={
        "attrs": {
            "page": {"background_fill_color": "black"},
            "plot": {"background_fill_color": "black"},
            "axis": {"axis_line_color": "white", "axis_label_text_color": "white", "major_label_text_color": "white"},
            "toolbar": {"active_drag": {"line_color": "white"}, "active_scroll": {"line_color": "white"}},
        }
    })
    doc.theme = dark_theme

    # Create the layout
    sidebar = column(dropdown_x, dropdown_y, text_input_x, text_input_y, slider, button, width=200)
    layout = row(sidebar, graph, sizing_mode="scale_width")
    doc.add_root(layout)


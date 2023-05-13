from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, PointDrawTool,FileInput,Div, TableColumn, NumberFormatter,Button,IntEditor
from bokeh.layouts import widgetbox
from bokeh.models.widgets import DataTable
import numpy as np
from logic import BezierCurve
import pandas as pd
from pybase64 import b64decode
import io

def modify_doc(doc):
    # Create a new plot with the title and axis labels
    p = figure(title="Scatter Plot with Bezier Curve", x_axis_label="X", y_axis_label="Y")

    # Create the control points for the Bezier curve
    control_x = []
    control_y = []
    control_points = np.column_stack((control_x,control_y))

    control_source = ColumnDataSource(data=dict(x=control_x, y=control_y))
    if(len(control_source.data["x"]) >= 3 and len(control_source.data['y']) >= 3):
        t = np.linspace(0, 1, 101)
        D = control_points[0] + t[:, np.newaxis] * (control_points[1] - control_points[0])
        E = control_points[1] + t[:, np.newaxis] * (control_points[2] - control_points[1])
        F = D + t[:, np.newaxis] * (E - D)

        points_source = ColumnDataSource(data=dict(x=D[:, 0], y=D[:, 1], x2=E[:, 0], y2=E[:, 1], x3=F[:, 0], y3=F[:, 1]))
    else:
         points_source = ColumnDataSource(data=dict(x=[], y=[], x2 = [], y2=[], x3= [], y3=[]))

    # Add the control points as scatter glyphs
    control_scatter = p.scatter('x', 'y', source=control_source, size=10, color='blue')
    p.line('x', 'y', source=control_source, line_width=2, color='gray')

    # Enable point drawing tool for control points
    control_draw_tool = PointDrawTool(renderers=[control_scatter], empty_value='purple')
    p.add_tools(control_draw_tool)
    p.toolbar.active_tap = control_draw_tool

    # Create a Line glyph for the Bezier curve
    curve_source = ColumnDataSource(data=dict(x=[], y=[]))
    curve = p.line('x', 'y', source=curve_source, line_width=2, color='red')

    bezier_curve = BezierCurve(control_points)

    columns = [TableColumn(field='x', title='X', editor=IntEditor(), formatter=NumberFormatter(format='0.000')),    
               TableColumn(field='y', title='Y',  editor=IntEditor(),formatter=NumberFormatter(format='0.000')),]
    data_table = DataTable(source=control_source, columns=columns, height=300, editable=True)

    # Python callback to update the data sources and redraw the curve
    
    def update_curve():
        control_x = [float(x) for x in control_source.data['x']]
        control_y = [float(y) for y in control_source.data['y']]
        control_points = np.column_stack((control_x,control_y))
        bezier_curve.control_points=control_points
        t=np.linspace(0,1,101)
        curve_points = bezier_curve.calculate_curve_points(t)
            
        if(len(control_source.data["x"]) >= 3 and len(control_source.data['y']) >= 3):
            D = control_points[0] + t[:, np.newaxis] * (control_points[1] - control_points[0])
            E = control_points[1] + t[:, np.newaxis] * (control_points[2] - control_points[1])
            F = D + t[:, np.newaxis] * (E - D)
            points_source.data = {'x': D[:, 0], 'y': D[:, 1], 'x2': E[:, 0], 'y2': E[:, 1], 'x3': F[:, 0], 'y3': F[:, 1]}

        curve_source.data = {'x': curve_points[:,0], 'y': curve_points[:,1]}

    file_input_title = Div(text="<b>Choose an input file:</b>")

    file_input = FileInput(accept=".csv")

    

    # Python callback to handle file selection
    def handle_file_upload(attr, old, new):
        file = io.BytesIO(b64decode(new))
        data_frame = pd.read_csv(file, sep = ',', header = 0)
        data_source = data_frame.to_dict(orient='list')
        #print(data_source)
        if(not all([isinstance(item, int) for item in data_source["x"]])):
            print("Vezi coloana x")
            return
        elif(not all([isinstance(item, int) for item in data_source["y"]])):
            print("Vezi coloana y")
            return
            
        control_source.data = data_source
        update_curve()


    file_input_box = widgetbox(file_input_title, file_input)

    # Add the callback to the file input widget
    file_input.on_change('value', handle_file_upload)

    # Add the FileInput widget to the document
    doc.add_root(file_input_box)

    # Add the callback to the control points data source
    control_source.on_change('data', lambda attr, old, new: update_curve())

    def test(attr,old,new):
        print(attr)
    control_source.on_change('data', test)

    p.x_range.range_padding = 0.1
    p.y_range.range_padding = 0.1
    p.x_range.start = 0
    p.x_range.end = 5
    p.y_range.start = 0
    p.y_range.end = 7

    update_curve()
    # Create a curdoc and add the plot to it
    doc.add_root(p)

    def add_point():
        new_x = 0
        new_y = 0
        new_data = dict(control_source.data)
        new_data['x'].append(new_x)
        new_data['y'].append(new_y)
        control_source.data = new_data

    # create button and add callback function
    button = Button(label='Add Point', button_type='success')
    button.on_click(add_point)
    doc.add_root(button)

   
    doc.add_root(data_table)
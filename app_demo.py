import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from components.luacode import LuaCode
from components.seesoft import SeeSoft
from components.scatterplot import ScatterPlot
from components.tree import Tree
from dash.dependencies import Input, Output

path = os.path.dirname(os.path.realpath(__file__)) + '/data'
files = list()

# r=root, d=directories, f=files
# list all json files
for r, d, f in os.walk(path):
    for file in f:
        if '.json' in file:
            files.append(os.path.join(r, file))

file_left = files[0]
file_right = files[1]

seesoft_left = SeeSoft(file_left, comments=True)
seesoft_left.draw(img_path='assets/image_left.png')

seesoft_right = SeeSoft(file_right, comments=True)
seesoft_right.draw(img_path='assets/image_right.png')

luacode_left = LuaCode(file_left)
luacode_right = LuaCode(file_right)

scatterplot_left = ScatterPlot(file_left)
scatterplot_right = ScatterPlot(file_right)

tree_left = Tree(file_left)
tree_right = Tree(file_right)

# external_stylesheets = ['https://codepen.io/amyoshino/pen/jzXypZ.css']

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Tabs(
        children=[
            dcc.Tab(
                label='Source code visualization',
                children=[
                    html.Div(id='hidden-div-left',
                             style={'display': 'none'}),
                    html.Div(id='hidden-div-right',
                             style={'display': 'none'}),
                    html.Div(
                        children=[
                            luacode_left.view(dash_id='lua-code-left',
                                              columns='4'),
                            html.Div([
                                seesoft_left.view(dash_id='see-soft-left')
                            ],
                                style={'justify-content': 'center',
                                       'display': 'flex'},
                                className='two columns'
                            ),
                            html.Div([
                                seesoft_right.view(dash_id='see-soft-right')
                            ],
                                style={'justify-content': 'center',
                                       'display': 'flex'},
                                className='two columns'
                            ),
                            luacode_right.view(dash_id='lua-code-right',
                                               columns='4'),
                        ],
                        style={'padding': '3vh'},
                        className='row'
                    )
                ]
            ),
            dcc.Tab(
                label='Input visualization',
                children=[
                    html.Div(
                        children=[
                            scatterplot_left.view(
                                dash_id='scatter-plot-left',
                                columns='6', show_text=True),
                            scatterplot_right.view(
                                dash_id='scatter-plot-right',
                                columns='6',
                                show_legend=True,
                                show_text=True)
                        ],
                        style={'padding': '3vh'},
                        className='row'
                    ),
                    html.Div(
                        children=[
                            tree_left.view(dash_id='tree-left', columns='6'),
                            tree_right.view(dash_id='tree-right', columns='6')
                        ],
                        className='row'
                    )
                ]
            )
        ],
        style={'font-size': '1.9em'}
    )],
    className='ten columns offset-by-one'
)

# only works properly when seesoft is drawn with comments
# seesoft and luacode interaction for left part of the screen
app.clientside_callback(
    '''
    function scroll_lua_code_left(clickData) {
        if (clickData) {
            var element = document.getElementById("lua-code-left");
            var element_text_id = "lua-code-left" + clickData.points[0].text;
            var element_text = document.getElementById(element_text_id);
            var color = element_text.style.backgroundColor;
            var bounding = element.getBoundingClientRect();
            var text_bounding = element_text.getBoundingClientRect();

            // handle possible vertical scrolling
            if (text_bounding.top < bounding.top ||
                text_bounding.bottom > bounding.bottom) {
                element.scrollTop = clickData.points[0].customdata;
            }

            // handle highlighting
            if (color == "rgb(255, 173, 122)") {
                element_text.classList.remove("require_animate");
                void element_text.offsetWidth;
                element_text.classList.add("require_animate");
            }
            else if (color == "rgb(117, 235, 135)") {
                element_text.classList.remove("variable_animate");
                void element_text.offsetWidth;
                element_text.classList.add("variable_animate");
            }
            else if (color == "rgb(158, 203, 255)") {
                element_text.classList.remove("function_animate");
                void element_text.offsetWidth;
                element_text.classList.add("function_animate");
            }
            else if (color == "rgb(229, 141, 240)") {
                element_text.classList.remove("interface_animate");
                void element_text.offsetWidth;
                element_text.classList.add("interface_animate");
            }
            else if (color == "rgb(255, 236, 145)") {
                element_text.classList.remove("other_animate");
                void element_text.offsetWidth;
                element_text.classList.add("other_animate");
            }
            else {
                element_text.classList.remove("comment_animate");
                void element_text.offsetWidth;
                element_text.classList.add("comment_animate");
            }
        }
        return "";
    }
    ''',
    Output('hidden-div-left', 'children'),
    [Input('see-soft-left', 'clickData')]
)

# seesoft and luacode interaction for the right part of the screen
app.clientside_callback(
    '''
    function scroll_lua_code_right(clickData) {
        if (clickData) {
            var element = document.getElementById("lua-code-right");
            var element_text_id = "lua-code-right" + clickData.points[0].text;
            var element_text = document.getElementById(element_text_id);
            var color = element_text.style.backgroundColor;
            var bounding = element.getBoundingClientRect();
            var text_bounding = element_text.getBoundingClientRect();

            // handle possible vertical scrolling
            if (text_bounding.top < bounding.top ||
                text_bounding.bottom > bounding.bottom) {
                element.scrollTop = clickData.points[0].customdata;
            }

            // handle highlighting
            if (color == "rgb(255, 173, 122)") {
                element_text.classList.remove("require_animate");
                void element_text.offsetWidth;
                element_text.classList.add("require_animate");
            }
            else if (color == "rgb(117, 235, 135)") {
                element_text.classList.remove("variable_animate");
                void element_text.offsetWidth;
                element_text.classList.add("variable_animate");
            }
            else if (color == "rgb(158, 203, 255)") {
                element_text.classList.remove("function_animate");
                void element_text.offsetWidth;
                element_text.classList.add("function_animate");
            }
            else if (color == "rgb(229, 141, 240)") {
                element_text.classList.remove("interface_animate");
                void element_text.offsetWidth;
                element_text.classList.add("interface_animate");
            }
            else if (color == "rgb(255, 236, 145)") {
                element_text.classList.remove("other_animate");
                void element_text.offsetWidth;
                element_text.classList.add("other_animate");
            }
            else {
                element_text.classList.remove("comment_animate");
                void element_text.offsetWidth;
                element_text.classList.add("comment_animate");
            }
        }
        return "";
    }
    ''',
    Output('hidden-div-right', 'children'),
    [Input('see-soft-right', 'clickData')]
)

# maybe lua code sections and seesoft interaction could be fixed so that
# whole node text would be one section instead of one line or part of the line


if __name__ == '__main__':
    app.run_server(debug=True)

import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import components.layout as layout
from sample import Sample
from components.luacode import LuaCode
from components.seesoft import SeeSoft
from components.scatterplot import ScatterPlot
from components.tree import Tree
from components.clusters import Clusters
from keras.models import load_model
from network.clustering import ClusteringLayer


DIMENSIONS = 10

model_path = (os.path.dirname(os.path.realpath(__file__))
              + '/network/clustering_model_10.h5')
model = load_model(model_path,
                   custom_objects={'ClusteringLayer': ClusteringLayer})

luacode = None
seesoft = None
scatterplot = None
tree = None
sample = None
sample_path = None
clusters = Clusters()


app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H3(
            children='CodeNNVis',
            className='ten columns'
        )],
        className="row"
    ),
    html.Div([
        'Module sample to be analyzed: '],
        style={'margin-bottom': '10px'},
        className='row'
    ),
    html.Div([
        dcc.Input(
            id='module-input',
            value='data/...',
            style={'width': '300px'}
        ),
        html.Button(
            'Submit',
            id='module-input-button',
            n_clicks=0,
            style={'margin-left': '10px'},
            className='button-primary'
        )],
        className='row'
    ),
    html.Div(id='hidden-div',
             style={'display': 'none'}),
    html.Div([
        html.H5('Source code')],
        style={'margin-top': '20px'},
        className='row'
    ),
    html.Div(
        children=[
            html.Div(
                id='input-luacode',
                children=[
                    layout.get_empty_div(height=750)
                ],
                style={
                    'height': '800px',
                    'float': 'left',
                    'width': '520px',
                    'padding-left': '10px',
                    'padding-right': '10px',
                }
            ),
            dcc.Graph(
                id='seesoft-content',
                figure=layout.get_empty_figure(height=750),
                config={
                    'displayModeBar': False
                },
                style={
                    'max-height': '750px',
                    'float': 'left',
                    'width': '200px',
                    'padding': '10px',
                }
            ),
            html.Div(
                id='input-diagrams',
                children=[
                    html.H6('AST nodes order'),
                    dcc.Graph(
                        id='scatterplot-content',
                        figure=layout.get_empty_figure(height=200),
                        config={
                            'displayModeBar': False
                        },
                        style={
                            'height': '200px',
                        }
                    ),
                    html.H6('Input AST structure'),
                    dcc.Graph(
                        id='tree-content',
                        figure=layout.get_empty_figure(height=300),
                        config={
                            'displayModeBar': False
                        },
                        style={
                            'height': '300px',
                        }
                    ),
                    html.H6('Cluster diagram'),
                    dcc.RadioItems(
                        id='cluster-radio',
                        options=[
                            {'label': 'PCA', 'value': 'pca'},
                            {'label': 'T-SNE', 'value': 'tsne'}
                        ],
                        value='pca',
                        labelStyle={'display': 'inline-block'}
                    ),
                    dcc.Graph(
                        id='clusters-content',
                        figure=layout.get_empty_figure(height=500),
                        config={
                            'displayModeBar': False
                        },
                        style={
                            'height': '500px',
                        }
                    ),
                ],
                style={
                    'float': 'left',
                    'width': '720px',
                    'padding-left': '10px',
                    'padding-right': '10px',
                    'padding-bottom': '10px',
                }
            ),
        ],
        className='row'
    ),
],
    className='ten columns offset-by-one'
)


@app.callback(
    Output('input-luacode', 'children'),
    [Input('module-input-button', 'n_clicks')],
    [State('module-input', 'value')]
)
def update_input_luacode(n_clicks, value):
    global luacode

    if n_clicks > 0:
        luacode = LuaCode(path=value)
        return luacode.view(dash_id='lua-code-content')

    else:
        return layout.get_empty_div(750)


@app.callback(
    Output('seesoft-content', 'figure'),
    [Input('module-input-button', 'n_clicks')],
    [State('module-input', 'value')]
)
def update_input_seesoft(n_clicks, value):
    global seesoft

    if n_clicks > 0:
        seesoft = SeeSoft(path=value, comments=True)
        seesoft.draw()
        return seesoft.get_figure()

    else:
        return layout.get_empty_figure(height=750)


@app.callback(
    Output('scatterplot-content', 'figure'),
    [Input('module-input-button', 'n_clicks')],
    [State('module-input', 'value')]
)
def update_input_scatterplot(n_clicks, value):
    global scatterplot

    if n_clicks > 0:
        scatterplot = ScatterPlot(path=value)
        return scatterplot.get_figure(show_legend=True, show_text=True)

    else:
        return layout.get_empty_figure(height=200)


@app.callback(
    Output('tree-content', 'figure'),
    [Input('module-input-button', 'n_clicks')],
    [State('module-input', 'value')]
)
def update_input_tree(n_clicks, value):
    global tree

    if n_clicks > 0:
        tree = Tree(path=value)
        return tree.get_figure(horizontal=True)

    else:
        return layout.get_empty_figure(height=300)


@app.callback(
    Output('clusters-content', 'figure'),
    [Input('module-input-button', 'n_clicks')],
    [State('module-input', 'value')]
)
def update_clusters(n_clicks, value):
    global sample
    global clusters

    if n_clicks > 0:
        sample = Sample(path=value, model=model)
        clusters.add_sample(sample)
        return clusters.get_figure(algorithm='PCA')

    else:
        return layout.get_empty_figure(height=500)


app.clientside_callback(
    '''
    function scroll_lua_code_left(clickData) {
        if (clickData) {
            var element = document.getElementById("lua-code-content");
            var element_text_id = "lua-code-content" + clickData.points[0].text;
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
            if (color == "rgb(248, 172, 97)") {
                element_text.classList.remove("require_animate");
                void element_text.offsetWidth;
                element_text.classList.add("require_animate");
            }
            else if (color == "rgb(169, 208, 165)") {
                element_text.classList.remove("variable_animate");
                void element_text.offsetWidth;
                element_text.classList.add("variable_animate");
            }
            else if (color == "rgb(178, 198, 220)") {
                element_text.classList.remove("function_animate");
                void element_text.offsetWidth;
                element_text.classList.add("function_animate");
            }
            else if (color == "rgb(201, 161, 189)") {
                element_text.classList.remove("interface_animate");
                void element_text.offsetWidth;
                element_text.classList.add("interface_animate");
            }
            else if (color == "rgb(244, 223, 137)") {
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
    Output('hidden-div', 'children'),
    [Input('seesoft-content', 'clickData')]
)

if __name__ == '__main__':
    app.run_server(debug=True)

import os
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from keras.models import load_model
from network.clustering import ClusteringLayer
import components.layout as layout
from sample import Sample
from components.luacode import LuaCode
from components.seesoft import SeeSoft
from components.scatterplot import ScatterPlot
from components.tree import Tree
from components.clusters import Clusters
from components.prediction import Prediction
import time

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
click_counter = 0
clusters = Clusters()
prediction = None

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
        'Source code sample to be analyzed: '],
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
        html.H4('Source code visualization')],
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
            html.H6(
                'Prediction',
                style={
                    'position': 'absolute',
                    'top': '1050px',
                    'margin-left': '10px'
                }
            ),
            dcc.Graph(
                id='prediction-content',
                figure=layout.get_empty_figure(height=200),
                config={
                    'displayModeBar': False
                },
                style={
                    'height': '120px',
                    'width': '520px',
                    'position': 'absolute',
                    'top': '1100px',
                    'margin-left': '10px'
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
                        figure=layout.get_empty_figure(height=250),
                        config={
                            'displayModeBar': False
                        },
                        style={
                            'height': '250px',
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
    html.Div([
        html.H4('Data comparing')],
        style={'margin-top': '20px'},
        className='row'
    ),
    dcc.RadioItems(
        id='compare-radio',
        options=[
            {'label': 'AST', 'value': 'ast'},
            {'label': 'Coloured code', 'value': 'code'}
        ],
        value='ast',
        labelStyle={'display': 'inline-block'}
    ),
    html.Div(
        children=[
            html.Div('Analyzed sample', style={'width': '230px',
                                               'float': 'left',
                                               'margin': '10px'}),
            html.Div('Train sample #1', style={'width': '230px',
                                               'float': 'left',
                                               'margin': '10px'}),
            html.Div('Train sample #2', style={'width': '230px',
                                               'float': 'left',
                                               'margin': '10px'}),
            html.Div('Train sample #3', style={'width': '230px',
                                               'float': 'left',
                                               'margin': '10px'}),
            html.Div('Train sample #4', style={'width': '230px',
                                               'float': 'left',
                                               'margin': '10px'}),
            html.Div('Train sample #5', style={'width': '230px',
                                               'float': 'left',
                                               'margin': '10px'})
        ],
        className='row'
    ),
    html.Div(
        children=[
            html.Pre(
                [],
                style={'width': '230px', 'float': 'left',
                       'margin-right': '20px'}
            ),
            dcc.Dropdown(
                id='train1-dropdown',
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                style={'width': '230px', 'float': 'left',
                       'margin-right': '20px'}
            ),
            dcc.Dropdown(
                id='train2-dropdown',
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                style={'width': '230px', 'float': 'left',
                       'margin-right': '20px'}
            ),
            dcc.Dropdown(
                id='train3-dropdown',
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                style={'width': '230px', 'float': 'left',
                       'margin-right': '20px'}
            ),
            dcc.Dropdown(
                id='train4-dropdown',
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                style={'width': '230px', 'float': 'left',
                       'margin-right': '20px'}
            ),
            dcc.Dropdown(
                id='train5-dropdown',
                options=[
                    {'label': 'New York City', 'value': 'NYC'},
                    {'label': 'Montreal', 'value': 'MTL'},
                    {'label': 'San Francisco', 'value': 'SF'}
                ],
                style={'width': '230px', 'float': 'left',
                       'margin-right': '20px'}
            ),
        ],
        className='row'
    ),
    html.Div(
        children=[],
        className='row'
    )
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
        return layout.get_empty_figure(height=250)


@app.callback(
    Output('clusters-content', 'figure'),
    [Input('module-input-button', 'n_clicks'),
     Input('cluster-radio', 'value')],
    [State('module-input', 'value')]
)
def update_clusters(n_clicks, value1, value2):
    global click_counter
    global sample
    global clusters

    if n_clicks > 0:
        if n_clicks == click_counter:
            return clusters.get_figure(algorithm=value1)

        click_counter = n_clicks
        print(value2, value2)
        sample = Sample(path=value2, model=model)
        clusters.add_sample(sample)
        return clusters.get_figure(algorithm=value1)

    else:
        return layout.get_empty_figure(height=500)


@app.callback(
    Output('prediction-content', 'figure'),
    [Input('module-input-button', 'n_clicks')],
    [State('module-input', 'value')]
)
def update_input_tree(n_clicks, value):
    global prediction
    global sample

    if n_clicks > 0:
        while not sample:
            time.sleep(1.)

        prediction = Prediction(sample=sample)
        return prediction.get_figure()

    else:
        return layout.get_empty_figure(height=120)


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

import dash_core_components as dcc
import dash_html_components as html
from twitter_package import *
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import json
import dash
from dash.dependencies import Input, Output, State
from sklearn.externals import joblib
import pandas as pd
from twitter_package.charts import *
import base64
import warnings

with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=UserWarning)
    warnings.filterwarnings("ignore", category=DeprecationWarning) 
    nb = joblib.load('models/nb.pkl')
    log = joblib.load('models/log.pkl')
    forest = joblib.load('models/forest.pkl')
    gradboost = joblib.load('models/gradboost.pkl')
    adaboost = joblib.load('models/adaboost.pkl')
    svm = joblib.load('models/svm.pkl')

# load training and test sets
test_data = pd.read_csv('train_test_data/test_data.csv')
train_data = pd.read_csv('train_test_data/train_data.csv')
y_test = pd.read_csv('train_test_data/y_test.csv')
y_train = pd.read_csv('train_test_data/y_train.csv')

process_diagram = 'images/process_diagram.png'
encoded_process_image = base64.b64encode(open(process_diagram, 'rb').read())
sarima_diagram = 'images/sarima_process.png'
encoded_sarima_image = base64.b64encode(open(sarima_diagram, 'rb').read())

app.layout = html.Div(style={'fontFamily': 'Sans-Serif'}, children=[
    html.H1('Tracking Flu Outbreaks with Twitter', style={'textAlign': 'center', 'margin': '48px 0', 'fontFamily': 'Sans-Serif'}),
    dcc.Tabs(id="tabs", children=[
        dcc.Tab(label='Framework Overview', children=[
            html.Div([
                html.H1('Project Process Overview'),
                dcc.Markdown('The project was defined by two phases: (1) training machine learning classification models to identify flu-related tweets and (2) conducting time-series analyses with identified tweets and CDC data.'),
                html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_process_image.decode()))])
                        ])
                        ]),
        # dcc.Tab(label='Vectorization Overview', children=[
        #     html.Div([
        #         html.H1('Vectorization metrics overview here')
        #                 ])
        #                 ]),
        dcc.Tab(label='Natural Language Processing', children=[
            html.Div([
                html.H1('Chi-square values and features here'),
                html.H1('PCA plot here')
                        ])
                        ]),
        dcc.Tab(label='Models Overview', children=[
                dcc.Dropdown(
                id='select-model',
                options=[{'label': 'Naive Bayes', 'value': 'nb'},
                {'label': 'Logistic Regression', 'value': 'log'},
                {'label': 'Random Forest Classifier', 'value': 'forest'},
                {'label': 'Gradient Boosted Trees', 'value': 'gradboost'},
                {'label': 'AdaBoost', 'value': 'adaboost'},
                {'label': 'Support Vector Machine', 'value': 'svm'}
                        ],
                placeholder="Select a Model", value ='Model'),
                # dcc.Graph(id='map',figure=generate_all_roc_curves()),
                # html.Div(id='cm-container'),
                        ]),
        dcc.Tab(label='Time Series Analysis', children=[
            html.Div([
                html.H1('Time Series Analysis Overview'),
                html.Div([html.Img(src='data:image/png;base64,{}'.format(encoded_sarima_image.decode()))]),
                html.H1('SARIMAX metrics here'),
                dcc.Dropdown(
                id='select-model-metrics',
                options=[{'label': 'Visualizations', 'value': 'visual'},
                {'label': 'Stationarity', "value": 'stationarity'},
                {'label': 'ACF & PACF Plots', 'value': 'acf_pacf'},
                {'label': 'Diagnostic Plots', 'value': 'diagnostics'},
                {'label': 'Forecasting', 'value': 'forecasting'},
                        ],
                placeholder="Select Model Metrics", value ='Metric'),
                        ])
                        ]),
        dcc.Tab(label='Conclusions', children=[
            html.Div([
                html.H1('Conclusions'),
                html.H1('Limitations'),
                html.H1('Next Steps'),
                        ])
                        ]),
                        ])
                        ])

# @app.callback(Output(component_id = 'cm-container', component_property ='children'),
# [Input(component_id = 'select-model',component_property = 'value')])
def generate_confusion_matrix(input_value):
    model = check_model(input_value)
    predictions = model.predict(x_test)
    cm = confusion_matrix(y_test, predictions)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    return go.Heatmap(x=['POS', 'NEG'], y=['POS', 'NEG'], z=cm)

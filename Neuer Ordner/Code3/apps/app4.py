import numpy as np
import pandas as pd
import pymssql

import dash
import plotly.graph_objects as go
import plotly.offline as py

import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from datetime import datetime
from plotly.subplots import make_subplots
import dash_table
import math

from io import StringIO
from html.parser import HTMLParser

from app import app

import json

# HTML tag remover for cause and comment
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

# filter for table
operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

PAGE_SIZE = 15

# chain callback for plots
all_options = {
    'alltime': ['by WPS', 'by FA', 'by Device Group', 'by Wire', 'by Class', 'by Package'],
    'year': ['2018', '2019', '2020']
    # 'monthly': ['??', '?!?!', '###']
}

# second chain callback for plots
all_options2 = {
    'by WPS': ['None'],
    'by FA': ['None'],
    'by Device Group': ['None'],
    'by Wire': ['None'],
    'by Class': ['None'],
    'by Package': ['None'],
    '2018': ['by WPS', 'by FA', 'by Package', 'by Wire', 'by Class'],
    '2019': ['by WPS', 'by FA', 'by Package', 'by Wire', 'by Class'],
    '2020': ['by WPS', 'by FA', 'by Package', 'by Wire', 'by Class']
}


layout = html.Div(id = 'body-container', children = [
                    html.Div(className="links", children=[
                    html.Div(className="linkdiv",  children= [dcc.Link('AZQ List', href='/apps/app1')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'text-align': 'center', 'marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'}),
                    html.Div(className="linkdiv",  children= [dcc.Link('Endmessungstats.', href='/apps/app2')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '4%', 'text-align': 'center','marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'}),
                    html.Div(className="linkdiv",  children= [dcc.Link('Endmessunginfo.', href='/apps/app3')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '4%', 'text-align': 'center','marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'}),
                    html.Div(className="linkdiv",  children= [dcc.Link('Qualitätsinfo.', href='/apps/app4')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '4%', 'text-align': 'center','marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'})
                                                ],
                                        style = {'width': '100%','paddingRight': '7%', 'paddingLeft': '7%'}),
                    html.Br(),
                    html.Br(),
                    html.Div(className="content-container", children=[ # content container opener
                    html.H1(className= 'app_title', children='Qualitätstabelle'),
                    html.Div(children=[
                    dcc.RadioItems(id='whatdata2',
                                    options=[
                                        {'label': 'Verkürzte Info.', 'value': 'short'},
                                        {'label': 'Kommentar', 'value': 'comment'},
                                        {'label': 'Lagerinfo.', 'value': 'storage'}],
                                    value='short',
                                    labelStyle={'display': 'inline-block', 'marginRight': '2%'}
                                )],
                                    style = {'marginTop': '3.5%','paddingLeft': '5%'}),
                    html.Div(className= 'small-content-container', children=[ # small content container opener
                            html.Div(
                                    [dash_table.DataTable(
                                        id='q-list-table',
                                         page_current=0,
                                         page_size=PAGE_SIZE,
                                         page_action='custom',

                                         filter_action='custom',
                                         filter_query='',

                                         sort_action='custom',
                                         sort_mode='multi',
                                         sort_by=[],

                                         style_header={'backgroundColor': '#6983aa', 'fontWeight': 'bold'},
                                         style_cell={'backgroundColor': '#e4e4e4',
                                                    'color': 'black',
                                                    'textAlign': 'left',
                                                    'font-family': 'Overpass',
                                                    'font-size': '0.95rem'},
                                         style_table={
                                                    'title': 'Datatable',
                                                    'maxWidth': '100%',
                                                    'maxHeight': '800px',
                                                    'overflowX': 'scroll',
                                                    'textOverflow': 'ellipsis'},
                                        style_data_conditional=[
                                                        {
                                                            'if': {
                                                                'column_id': 'fa',
                                                                'filter_query': '{fa} = O'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#1089ff'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'fa',
                                                                'filter_query': '{fa} = X'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#d92027'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'wps',
                                                                'filter_query': '{wps} = O'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#1089ff'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'wps',
                                                                'filter_query': '{wps} = X'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#d92027'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'release',
                                                                'filter_query': '{release} = O'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#1089ff'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'release',
                                                                'filter_query': '{release} = X'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#d92027'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'scrapped',
                                                                'filter_query': '{scrapped} = O'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#1089ff'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'scrapped',
                                                                'filter_query': '{scrapped}  = X'
                                                            },
                                                            # 'backgroundColor': 'white',
                                                            'color': '#d92027'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'rejected',
                                                                'filter_query': '{rejected} >= 5000 && {rejected}  < 10000'
                                                            },
                                                            'backgroundColor': '#f17808',
                                                            'color': 'white'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'rejected',
                                                                'filter_query': '{rejected} >= 10000 && {rejected}  < 9999999999'
                                                            },
                                                            'backgroundColor': '#d92027',
                                                            'color': 'white'
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'final_test_yield',
                                                                'filter_query': '{final_test_yield} <= 98 && {final_test_yield} > 95'
                                                            },
                                                            'backgroundColor': '#f17808',
                                                            'color': 'white',
                                                        },
                                                        {
                                                            'if': {
                                                                'column_id': 'final_test_yield',
                                                                'filter_query': '{final_test_yield} <= 95'
                                                            },
                                                            'backgroundColor': '#d92027',
                                                            'color': 'white',
                                                        }]
                                                        )],
                                            style = {'height': '550px', 'paddingLeft': '0.7%', 'paddingRight': '0.7%','paddingTop' : '0.7%'})],
                                            style={'marginLeft': '3%','marginTop': '1%', 'marginRight': '3%',  'paddingBottom': '3.7%', 'paddingTop': '3.7%', 'marginBottom': '40px'}), # small content container closer
                    html.H1(className= 'app_title', children='Qualitätsstatistik'),
                    html.Div(
                            dcc.RadioItems(id='Q-plot-time-period',
                                            options=[
                                                {'label': 'Jährlich', 'value':'year'},
                                                {'label': 'Alle Zeit', 'value':'alltime'}
                                                    ],
                                            value='year',
                                            labelStyle={'display': 'inline-block', 'marginRight': '2%'}
                                        ),
                                            style={'marginTop': '3.5%','paddingLeft': '5%'}),
                    html.Div(
                            dcc.Dropdown(id='Q-plot-second-radio-item'
                                        ),
                                            style={'marginTop': '15px','paddingLeft': '5%', 'display': 'inline-block', 'width': '30%'}),
                    html.Div(
                            dcc.Dropdown(id='Q-plot-third-radio-item'
                                        ),
                                            style={'marginTop': '15px','paddingLeft': '10px', 'display': 'inline-block', 'width': '30%'}),
                    html.Div(className= 'small-content-container', children=[
                            dcc.Graph(id='Q-plot')
                                                                            ],
                                            style={'height':'500px','width': '718px','marginLeft': '15px','marginTop': '15px', 'paddingBottom': '25px', 'paddingTop': '25px', 'display': 'inline-block'}),
                    html.Div(className= 'small-content-container', children=[
                            dash_table.DataTable(id='q_table',
                                                 columns =[
                                                            {'name': 'Charge', 'id': 'a_lot'},
                                                            {'name': 'Typ', 'id': 'device'},
                                                            {'name': 'Q-ID', 'id': 'quality_id'},
                                                            {'name': 'Class', 'id': 'class_name'}
                                                            ],
                                                page_current=0,
                                                page_size=13,
                                                page_action='custom'
                                                )],
                                            style={'height':'500px','width': '560px','marginLeft': '15px','marginTop': '15px',  'paddingBottom': '25px', 'paddingTop': '25px', 'display': 'inline-block'})
                    ], style = {'width': '1325px', 'marginLeft': '15px', 'marginTop': '50px', 'marginBottom': '35px', 'paddingBottom': '35px'}) # content container closer
                        ])

# callback for table
@app.callback(
            [Output('q-list-table', 'data'),
            Output('q-list-table', 'columns'),
            Output('q-list-table', 'page_count')],
            [Input('whatdata2', 'value'),
            Input('q-list-table', "page_current"),
            Input('q-list-table', "page_size"),
            Input('q-list-table', "sort_by"),
            Input('q-list-table', "filter_query")]
            )
def render_content(what_data2, page_current, page_size, sort_by, filter):

    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")
    print("           DASHBOARD (Q)       ")
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")

    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                       user='WebServer',
                       password='W3bS3rv3r',
                       database='ZNGFinalTest')

    if what_data2 == "short":
        df_a4 = pd.read_csv('a4_short.txt')
        # fill empty cells in wafer info
        df_a4['wafer_info'].fillna("Unbekannt", inplace=True)

        # for total rejection
        df_a4['rejected'] = df_a4['final_test_para_fails'] + df_a4['final_test_gross_fails']

        df_a4['final_test_yield'] = round(100*df_a4['final_test_yield'],2)

        # NaN or NaT data sorting
        df_a4['delivery_date'] = df_a4['delivery_date'].astype(str)
        df_a4['delivery_date'].replace({'NaT': 'Vor Auslieferung'}, inplace=True)


        # Q date sorting
        df_a4['edit_date'] = df_a4['edit_date'].astype(str)
        df_a4['edit_date'] = df_a4['edit_date'].str.split('\s+').str[0]
        df_a4['edit_date'].replace({'NaT': ' '}, inplace=True)
        df_a4['edit_user'] = df_a4['edit_user'].str.split('-').str[0].str.capitalize()
        df_a4['create_date'] = df_a4['create_date'].astype(str)
        df_a4['create_date'] = df_a4['create_date'].str.split('\s+').str[0]
        df_a4['create_user'] = df_a4['create_user'].str.split('-').str[0].str.capitalize()
        df_a4['create_date'].replace({'NaT': ' '}, inplace=True)

        df_a4['comment'].fillna('<p>', inplace=True)
        df_a4['comment'] = df_a4['comment'].map(strip_tags)

        df_a4['cause'].fillna("-", inplace=True)
        df_a4['cause'] = df_a4['cause'].map(strip_tags)

        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
        for column in df_a4[['wps', 'fa', 'release', 'scrapped']]:
            df_a4[column] = df_a4[column].map(booleanDictionary)

        filtering_expressions = filter.split(' && ')

        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                df_a4 = df_a4.loc[getattr(df_a4[col_name], operator)(filter_value)]
            elif operator == 'contains':
                df_a4 = df_a4.loc[df_a4[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                df_a4 = df_a4.loc[df_a4[col_name].str.startswith(filter_value)]

        if len(sort_by):
            df_a4 = df_a4.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        # pagination
        page_count = math.ceil(len(df_a4['a_lot'])/page_size)

        columns_s=[
                    {'name': 'Q-ID', 'id': 'quality_id'},
                    {'name': 'Charge', 'id': 'a_lot'},
                    {'name': 'LS #', 'id': 'ba'},
                    {'name': 'Typ', 'id': 'device'},
                    {'name': 'WPS', 'id': 'wps'},
                    {'name': 'FA', 'id': 'fa'},
                    {'name': 'Lieferung', 'id': 'release'},
                    {'name': 'Schrott', 'id': 'scrapped'},
                    {'name': 'Rejected', 'id': 'rejected'},
                    {'name': 'Output', 'id': 'final_test_output'},
                    {'name': 'Ausbeute', 'id': 'final_test_yield'},
                    {'name': 'Class', 'id': 'class_name'},
                    {'name': 'Ursache', 'id': 'cause'},
                    {'name': 'Erstellungsdatum', 'id': 'create_date'},
                    {'name': 'Editdatum', 'id': 'edit_date'},
                    {'name': 'Editer', 'id': 'edit_user'},
                    {'name': 'Wafer: Menge(probed/unprobed))', 'id': 'wafer_info'}]

        return df_a4.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'),columns_s, page_count


    elif what_data2 == "comment":
        df_a4 = pd.read_csv('a4_comment.txt')
        # fill empty cells in wafer info
        df_a4['wafer_info'].fillna("Unbekannt", inplace=True)

        # for total rejection
        df_a4['rejected'] = df_a4['final_test_para_fails'] + df_a4['final_test_gross_fails']

        df_a4['final_test_yield'] = round(100*df_a4['final_test_yield'],2)

        # NaN or NaT data sorting
        df_a4['delivery_date'] = df_a4['delivery_date'].astype(str)
        df_a4['delivery_date'].replace({'NaT': 'Vor Auslieferung'}, inplace=True)
        # df_a4['delivery_date'].fillna('Not_yet_delivered x', inplace=True)
        # df_a4['day'].fillna('Not_delivered', inplace=True)

        # Q date sorting
        df_a4['edit_date'] = df_a4['edit_date'].astype(str)
        df_a4['edit_date'] = df_a4['edit_date'].str.split('\s+').str[0]
        df_a4['edit_date'].replace({'NaT': ' '}, inplace=True)
        df_a4['edit_user'] = df_a4['edit_user'].str.split('-').str[0].str.capitalize()
        df_a4['create_date'] = df_a4['create_date'].astype(str)
        df_a4['create_date'] = df_a4['create_date'].str.split('\s+').str[0]
        df_a4['create_user'] = df_a4['create_user'].str.split('-').str[0].str.capitalize()
        df_a4['create_date'].replace({'NaT': ' '}, inplace=True)

        df_a4['comment'].fillna('<p>', inplace=True)
        df_a4['comment'] = df_a4['comment'].map(strip_tags)
        # df_a4['transistor_type'].fillna("-", inplace=True)
        # df_a4['ship_package'].fillna("-", inplace=True)
        # df_a4['lead_frame'].fillna("-", inplace=True)
        df_a4['cause'].fillna("-", inplace=True)
        df_a4['cause'] = df_a4['cause'].map(strip_tags)

        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
        for column in df_a4[['wps', 'fa', 'release', 'scrapped']]:
            df_a4[column] = df_a4[column].map(booleanDictionary)

        filtering_expressions = filter.split(' && ')

        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                df_a4 = df_a4.loc[getattr(df_a4[col_name], operator)(filter_value)]
            elif operator == 'contains':
                df_a4 = df_a4.loc[df_a4[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                df_a4 = df_a4.loc[df_a4[col_name].str.startswith(filter_value)]

        if len(sort_by):
            df_a4 = df_a4.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        # pagination
        page_count = math.ceil(len(df_a4['a_lot'])/page_size)

        columns_s=[
                    {'name': 'Q-ID', 'id': 'quality_id'},
                    {'name': 'Charge', 'id': 'a_lot'},
                    {'name': 'LS #', 'id': 'ba'},
                    {'name': 'Typ', 'id': 'device'},
                    {'name': 'Wire', 'id': 'bond_wire'},
                    {'name': 'Kommentar', 'id': 'comment'},
                    {'name': 'WPS', 'id': 'wps'},
                    {'name': 'FA', 'id': 'fa'},
                    {'name': 'Lieferung', 'id': 'release'},
                    {'name': 'Schrott', 'id': 'scrapped'},
                    {'name': 'Rejected', 'id': 'rejected'},
                    {'name': 'Output', 'id': 'final_test_output'},
                    {'name': 'Ausbeute', 'id': 'final_test_yield'},
                    {'name': 'Class', 'id': 'class_name'},
                    {'name': 'Ursache', 'id': 'cause'},
                    {'name': 'Ersteller', 'id': 'create_user'},
                    {'name': 'Erstellungsdatum', 'id': 'create_date'},
                    {'name': 'Editer', 'id': 'edit_user'},
                    {'name': 'Editdatum', 'id': 'edit_date'}
                    ]

        return df_a4.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'),columns_s, page_count
    elif what_data2 == "storage":
        df_a4 = pd.read_csv('a4_storage.txt')
        # fill empty cells in wafer info
        df_a4['wafer_info'].fillna("Unbekannt", inplace=True)

        # for total rejection
        df_a4['rejected'] = df_a4['final_test_para_fails'] + df_a4['final_test_gross_fails']

        df_a4['final_test_yield'] = round(100*df_a4['final_test_yield'],2)

        # NaN or NaT data sorting
        df_a4['delivery_date'] = df_a4['delivery_date'].astype(str)
        df_a4['delivery_date'].replace({'NaT': 'Vor Auslieferung'}, inplace=True)
        # df_a4['delivery_date'].fillna('Not_yet_delivered x', inplace=True)
        # df_a4['day'].fillna('Not_delivered', inplace=True)
        df_a4['box_class'].fillna("-", inplace=True)

        # Q date sorting
        df_a4['edit_date'] = df_a4['edit_date'].astype(str)
        df_a4['edit_date'] = df_a4['edit_date'].str.split('\s+').str[0]
        df_a4['edit_date'].replace({'NaT': ' '}, inplace=True)
        df_a4['edit_user'] = df_a4['edit_user'].str.split('-').str[0].str.capitalize()
        df_a4['create_date'] = df_a4['create_date'].astype(str)
        df_a4['create_date'] = df_a4['create_date'].str.split('\s+').str[0]
        df_a4['create_user'] = df_a4['create_user'].str.split('-').str[0].str.capitalize()
        df_a4['create_date'].replace({'NaT': ' '}, inplace=True)

        df_a4['cause'].fillna("-", inplace=True)
        df_a4['cause'] = df_a4['cause'].map(strip_tags)

        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
        for column in df_a4[['wps', 'fa', 'release', 'scrapped']]:
            df_a4[column] = df_a4[column].map(booleanDictionary)

        filtering_expressions = filter.split(' && ')

        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                df_a4 = df_a4.loc[getattr(df_a4[col_name], operator)(filter_value)]
            elif operator == 'contains':
                df_a4 = df_a4.loc[df_a4[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                df_a4 = df_a4.loc[df_a4[col_name].str.startswith(filter_value)]

        if len(sort_by):
            df_a4 = df_a4.sort_values(
                [col['column_id'] for col in sort_by],
                ascending=[
                    col['direction'] == 'asc'
                    for col in sort_by
                ],
                inplace=False
            )

        # pagination
        page_count = math.ceil(len(df_a4['a_lot'])/page_size)

        columns_l=[
                    {'name': 'Q-ID', 'id': 'quality_id'},
                    {'name': 'Charge', 'id': 'a_lot'},
                    {'name': 'LS #', 'id': 'ba'},
                    {'name': 'Typ', 'id': 'device'},
                    {'name': 'Storage', 'id': 'box_class'},
                    {'name': 'WPS', 'id': 'wps'},
                    {'name': 'FA', 'id': 'fa'},
                    {'name': 'Lieferung', 'id': 'release'},
                    {'name': 'Schrott', 'id': 'scrapped'},
                    {'name': 'Rejected', 'id': 'rejected'},
                    {'name': 'Output', 'id': 'final_test_output'},
                    {'name': 'Ausbeute', 'id': 'final_test_yield'},
                    {'name': 'Class', 'id': 'class_name'},
                    {'name': 'Ursache', 'id': 'cause'}
                    ]

        return df_a4.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'), columns_l, page_count

# call back for Time period (chain for fisrt and second)
@app.callback(
            Output('Q-plot-second-radio-item', 'options'),
            [Input('Q-plot-time-period', 'value')]
            )
def set_cities_options(selected_time_period):
    return [{'label': i, 'value': i} for i in all_options[selected_time_period]]

# call back for second option (chain for fisrt and second)
@app.callback(
    Output('Q-plot-second-radio-item', 'value'),
    [Input('Q-plot-second-radio-item', 'options')])
def set_cities_value(available_options):
    return available_options[-1]['value']

# call back for chain call back above (chain for second and third)
@app.callback(
            Output('Q-plot-third-radio-item', 'options'),
            [Input('Q-plot-second-radio-item', 'value')]
            )
def set_cities_options(selected_option):
    return [{'label': i, 'value': i} for i in all_options2[selected_option]]

# call back for chain call back above (chain for second and third)
@app.callback(
    Output('Q-plot-third-radio-item', 'value'),
    [Input('Q-plot-third-radio-item', 'options')])
def set_cities_value(available_options2):
    return available_options2[-1]['value']

# call back for plot
@app.callback(
            Output('Q-plot', 'figure'),
            [Input('Q-plot-time-period', 'value'),
             Input('Q-plot-second-radio-item', 'value'),
             Input('Q-plot-third-radio-item', 'value')]
             )
def q_plot_generator(time_period, second_value, third_value):
    df_Q_plot = pd.read_csv("q_plot.txt")
    df_Q_plot['create_date'] = pd.to_datetime(df_Q_plot['create_date'])
    df_Q_plot['year'] =  df_Q_plot['create_date'].dt.year
    df_Q_plot['month'] = df_Q_plot['create_date'].dt.month
    df_Q_plot['week'] = df_Q_plot['create_date'].dt.week
    df_Q_plot['day'] = df_Q_plot['create_date'].dt.day

    df_Q_plot['cause'].fillna('<p>', inplace=True)
    df_Q_plot['cause'] = df_Q_plot['cause'].map(strip_tags)

    # replace wps boolean
    booleanDictionary = {True: 'O', False: 'X'}

    #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
    for column in df_Q_plot[['wps', 'fa']]:
        df_Q_plot[column] = df_Q_plot[column].map(booleanDictionary)

    if time_period == 'alltime':
        if second_value == 'by WPS':
            # replace wps boolean
            booleanDictionary = {'O': 'WPS', 'X': 'Kein WPS'}
            #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
            for column in df_Q_plot[['wps', 'fa']]:
                df_Q_plot[column] = df_Q_plot[column].map(booleanDictionary)

            fig_Q_1 = go.Figure(
                            data = go.Pie(
                                            labels = df_Q_plot.groupby('wps')['a_lot'].count().index,
                                            values= df_Q_plot.groupby('wps')['a_lot'].count().values,
                                            name='piechart'
                                            ),
                            layout = go.Layout(
                                        title = 'All time Q IDs by WPS',
                                        # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                        paper_bgcolor='white',
                                        plot_bgcolor='white',
                                        legend_orientation="h",
                                        legend=dict(xanchor="left", yanchor="top", y=-0.3),
                                        ))

            return fig_Q_1
        elif second_value ==  'by FA':
            # replace wps boolean
            booleanDictionary = {'O': 'FA', 'X': 'Kein FA'}
            #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
            for column in df_Q_plot[['wps', 'fa']]:
                df_Q_plot[column] = df_Q_plot[column].map(booleanDictionary)
            fig_Q_1 = go.Figure(
                            data = go.Pie(
                                            labels = df_Q_plot.groupby('fa')['a_lot'].count().index,
                                            values= df_Q_plot.groupby('fa')['a_lot'].count().values,
                                            name='piechart'
                                            ),
                            layout = go.Layout(
                                        title = 'All time Q IDs by FA',
                                        # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                        paper_bgcolor='white',
                                        plot_bgcolor='white',
                                        legend_orientation="h",
                                        legend=dict(xanchor="left", yanchor="top", y=-0.3),
                                        ))

            return fig_Q_1
        elif second_value ==  'by Package':
                fig_Q_1 = go.Figure(
                                data = go.Pie(
                                                labels = df_Q_plot.groupby('package')['a_lot'].count().index,
                                                values= df_Q_plot.groupby('package')['a_lot'].count().values,
                                                name='piechart'
                                                ),
                                layout = go.Layout(
                                            title = 'All time Q IDs by Package',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            paper_bgcolor='white',
                                            plot_bgcolor='white',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top", y=-0.3),
                                            ))

                return fig_Q_1
        elif second_value ==  'by Wire':
            fig_Q_1 = go.Figure(
                            data = go.Pie(
                                            labels = df_Q_plot.groupby('bond_wire')['a_lot'].count().index,
                                            values= df_Q_plot.groupby('bond_wire')['a_lot'].count().values,
                                            name='piechart'
                                            ),
                            layout = go.Layout(
                                        title = 'All time Q IDs by Wire',
                                        # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                        paper_bgcolor='white',
                                        plot_bgcolor='white',
                                        legend_orientation="h",
                                        legend=dict(xanchor="left", yanchor="top", y=-0.3),
                                        ))

            return fig_Q_1
        elif second_value ==  'by Class':
            fig_Q_1 = go.Figure(
                            data = go.Pie(
                                            labels = df_Q_plot.groupby('class_name')['a_lot'].count().index,
                                            values= df_Q_plot.groupby('class_name')['a_lot'].count().values,
                                            name='piechart'
                                            ),
                            layout = go.Layout(
                                        title = 'All time Q IDs by Class',
                                        # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                        paper_bgcolor='white',
                                        plot_bgcolor='white',
                                        legend_orientation="h",
                                        legend=dict(xanchor="left", yanchor="top", y=-0.3),
                                        ))

            return fig_Q_1
        elif second_value == 'by Device Group':
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x = df_Q_plot.groupby('device_group')['a_lot'].count().sort_values(ascending=False).index,
                                            y = df_Q_plot.groupby('device_group')['a_lot'].count().sort_values(ascending=False).values,
                                            # y = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].diff().values,
                                            # name = 'Output diff.',
                                            # hoverinfo = 'x+y+name',
                                            # marker = dict(color=color1.tolist()),
                                            # showlegend=False
                                            )],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                return fig_Q_1
    elif time_period == 'year':
        if second_value == '2018':
            if third_value == 'by Class':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['class_name'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Class',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by Wire':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['bond_wire'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Wire',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            showlegend=True,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))

                return fig_Q_1
            elif third_value == 'by Package':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['package'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Package',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            showlegend=True,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by WPS':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['wps'] == 'O'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['wps'] == 'O'].groupby('month')['a_lot'].count().values,
                                            name = 'WPS'),
                                        go.Bar(
                                            x=df_Q_plot[df_Q_plot['wps'] == 'X'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['wps'] == 'X'].groupby('month')['a_lot'].count().values,
                                            name = 'Kein WPS')
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by WPS',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            showlegend=True,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by FA':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['fa'] == 'O'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['fa'] == 'O'].groupby('month')['a_lot'].count().values,
                                            name = 'FA'),
                                        go.Bar(
                                            x=df_Q_plot[df_Q_plot['fa'] == 'X'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['fa'] == 'X'].groupby('month')['a_lot'].count().values,
                                            name = 'Kein FA')
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by FA',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            showlegend=True,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
        elif second_value == '2019':
            if third_value == 'by Class':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['class_name'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Class',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by Wire':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['bond_wire'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Wire',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by Package':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['package'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Package',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by WPS':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['wps'] == 'O'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['wps'] == 'O'].groupby('month')['a_lot'].count().values,
                                            name = 'WPS'),
                                        go.Bar(
                                            x=df_Q_plot[df_Q_plot['wps'] == 'X'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['wps'] == 'X'].groupby('month')['a_lot'].count().values,
                                            name = 'Kein WPS')
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by WPS',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by FA':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['fa'] == 'O'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['fa'] == 'O'].groupby('month')['a_lot'].count().values,
                                            name = 'FA'),
                                        go.Bar(
                                            x=df_Q_plot[df_Q_plot['fa'] == 'X'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['fa'] == 'X'].groupby('month')['a_lot'].count().values,
                                            name = 'Kein FA')
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by FA',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
        elif second_value == '2020':
            if third_value == 'by Class':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['class_name'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Class',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by Wire':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['bond_wire'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Wire',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by Package':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['package'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by Package',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by WPS':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['wps'] == 'O'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['wps'] == 'O'].groupby('month')['a_lot'].count().values,
                                            name = 'WPS'),
                                        go.Bar(
                                            x=df_Q_plot[df_Q_plot['wps'] == 'X'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['wps'] == 'X'].groupby('month')['a_lot'].count().values,
                                            name = 'Kein WPS')
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by WPS',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1
            elif third_value == 'by FA':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]
                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['fa'] == 'O'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['fa'] == 'O'].groupby('month')['a_lot'].count().values,
                                            name = 'FA'),
                                        go.Bar(
                                            x=df_Q_plot[df_Q_plot['fa'] == 'X'].groupby('month')['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['fa'] == 'X'].groupby('month')['a_lot'].count().values,
                                            name = 'Kein FA')
                                        ],
                                layout = go.Layout(
                                            title = 'Q-ID by FA',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(xanchor="left", yanchor="top"),
                                            xaxis = {
                                                    'autorange' : True,
                                                    'type' : 'category',
                                                    'categoryarray' : [i for i in range(1,13)],
                                                    'tickfont' : dict(color= 'black', size=16, family = 'Overpass')
                                                    },
                                            yaxis = {
                                                    'title' : 'Count',
                                                    'titlefont': dict(color= 'black', size=16, family = 'Overpass'),
                                                    'showgrid' : True
                                                    }
                                                ))
                return fig_Q_1

@app.callback(
    [Output('q_table', 'data'),
    Output('q_table','columns')],
    [Input('Q-plot-time-period', 'value'),
     Input('Q-plot-second-radio-item', 'value'),
     Input('Q-plot-third-radio-item', 'value'),
     Input('Q-plot', 'clickData'),
     Input('q_table', "page_current"),
     Input('q_table', "page_size")])
def callback_image(time_period, second_value, third_value, clicked_bar, page_current2, page_size2):
    if clicked_bar is None:
        clicked_data_month = datetime.today().month
    else:
        clicked_data_month = clicked_bar['points'][0]['label']

    df_Q_table = pd.read_csv("q_table.txt")
    df_Q_table['create_date'] = pd.to_datetime(df_Q_table['create_date'])
    df_Q_table['year'] =  df_Q_table['create_date'].dt.year
    df_Q_table['month'] = df_Q_table['create_date'].dt.month
    df_Q_table['week'] = df_Q_table['create_date'].dt.week
    df_Q_table['day'] = df_Q_table['create_date'].dt.day

    df_Q_table['cause'].fillna('<p>', inplace=True)
    df_Q_table['cause'] = df_Q_table['cause'].map(strip_tags)

    if time_period == 'alltime':
        pass
    elif time_period == 'year':
        if second_value == '2018':
            if third_value == 'by Class':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2018) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Class', 'id': 'class_name'},
                           ]
            elif third_value == 'by Wire':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2018) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Wire', 'id': 'bond_wire'},
                           ]
            elif third_value == 'by Package':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2018) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Package', 'id': 'package'},
                           ]
            elif third_value == 'by WPS':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2018) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'WPS', 'id': 'wps'},
                           ]
            elif third_value == 'by FA':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2018) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'FA', 'id': 'fa'},
                           ]
        elif second_value == '2019':
            if third_value == 'by Class':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2019) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Class', 'id': 'class_name'},
                           ]
            elif third_value == 'by Wire':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2019) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Wire', 'id': 'bond_wire'},
                           ]
            elif third_value == 'by Package':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2019) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Package', 'id': 'package'},
                           ]
            elif third_value == 'by WPS':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2019) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'WPS', 'id': 'wps'},
                           ]
            elif third_value == 'by FA':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2019) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'FA', 'id': 'fa'},
                           ]
        elif second_value == '2020':
            if third_value == 'by Class':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2020) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Class', 'id': 'class_name'},
                           ]
            elif third_value == 'by Wire':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2020) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Wire', 'id': 'bond_wire'},
                           ]
            elif third_value == 'by Package':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2020) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'Package', 'id': 'package'},
                           ]
            elif third_value == 'by WPS':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2020) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'WPS', 'id': 'wps'},
                           ]
            elif third_value == 'by FA':
                df_Q_table = df_Q_table[(df_Q_table['year'] == 2020) & (df_Q_table['month'] == int(clicked_data_month))]
                columns =[
                           {'name': 'Charge', 'id': 'a_lot'},
                           {'name': 'Typ', 'id': 'device'},
                           {'name': 'Q-ID', 'id': 'quality_id'},
                           {'name': 'FA', 'id': 'fa'},
                           ]

    # replace wps boolean
    booleanDictionary = {True: 'O', False: 'X'}

    #loop by df_a4 is loop by columns, same as for column in booleandf_a4.columns:
    for column in df_Q_table[['wps', 'fa']]:
        df_Q_table[column] = df_Q_table[column].map(booleanDictionary)

    return df_Q_table.sort_values('a_lot', ascending=False).iloc[page_current2*page_size2:(page_current2+ 1)*page_size2].to_dict('records'), columns

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
    'alltime': ['Die Anzahl', 'Package', 'Device Grop'],
    'year': ['2018', '2019', '2020']
    # 'monthly': ['??', '?!?!', '###']
}

# second chain callback for plots
all_options2 = {
    'Die Anzahl': ['aaaa', 'bbb', 'ccc cc'],
    'Package': ['ffsd', 'vxcv', 'xv'],
    'Device Grop': ['sad', 'bcvb', 'dsadsa'],
    '2018': ['per Package', 'per Wire', 'per Class'],
    '2019': ['per Package', 'per Wire', 'per Class'],
    '2020': ['per Package', 'per Wire', 'per Class']
}


layout = html.Div([
                    html.Div(className="links", children=[
                    html.Div(className="linkdiv",  children= [dcc.Link('AZQ List', href='/apps/app1')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'text-align': 'center', 'marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'}),
                    html.Div(className="linkdiv",  children= [dcc.Link('F.T. Stats', href='/apps/app2')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '4%', 'text-align': 'center','marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'}),
                    html.Div(className="linkdiv",  children= [dcc.Link('F.T. Lot Info.', href='/apps/app3')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '4%', 'text-align': 'center','marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'}),
                    html.Div(className="linkdiv",  children= [dcc.Link('Quality Info.', href='/apps/app4')],
                                        style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '4%', 'text-align': 'center','marginTop':'20px',
                                                'font-size': '2em', 'font-family': 'Overpass'})
                                                ],
                                        style = {'width': '100%','paddingRight': '7%', 'paddingLeft': '7%'}),
                    html.Br(),
                    html.Br(),
                    html.Div(className="content-container", children=[ # content container opener
                    html.H1(className= 'app_title', children='Quality Information'),
                    html.Div(children=[
                    dcc.RadioItems(id='whatdata2',
                                    options=[
                                        {'label': 'Verkürzte Info.', 'value': 'short'},
                                        {'label': 'Comment', 'value': 'comment'},
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
                    html.H1(className= 'app_title', children='Quality Statistics'),
                    html.Div(
                            dcc.RadioItems(id='Q-plot-time-period',
                                            options=[
                                                {'label': 'Yearly', 'value':'year'},
                                                {'label': 'All time', 'value':'alltime'}
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
                                            style={'marginLeft': '3%','marginTop': '1%', 'marginRight': '3%',  'paddingBottom': '3.7%', 'paddingTop': '3.7%'})
                    ], style = {'width': '86%', 'marginLeft': '7%', 'marginRight': '7%', 'marginTop': '50px', 'marginBottom': '50px', 'paddingBottom': '50px'}) # content container closer
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
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                       user='WebServer',
                       password='W3bS3rv3r',
                       database='ZNGFinalTest')

    if what_data2 == "short":
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, ZNGProduction.catuno.tbl_lots.ba, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, ZNGProduction.catuno.tbl_products.article \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
        ), \
        tbl2 AS ( \
        SELECT lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), '; ') AS wafer_info \
        FROM \
        ( \
        SELECT lot, wafer_lot + ': ' + CAST(wafer_quantity as VARCHAR(100))  + '(' + probed + ')' AS wafer_info \
        FROM ZNGProduction.catuno.tbl_wafers \
        WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' \
        ) tbl0 \
        GROUP BY lot \
        ), \
        tbl3 AS ( \
        SELECT ZNGFinalTest.quality.vw_lots.release, ZNGFinalTest.quality.vw_lots.scrapped, ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ), \
        tbl4 AS ( \
        SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator \
        FROM ZNGFinalTest.final_test3.tbl_summaries \
        GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
        ) \
        SELECT tbl1.a_lot, tbl1.ba, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.department, tbl1.package, tbl1.bond_wire, tbl3.release, tbl3.scrapped, tbl1.ship_package, tbl1.uk_input, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.comment, '<div>',''), '</div>', '.'), '<br>','; '), '</font>',''), '&gt;', '<'), '-&lt;','>') AS comment,  REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END + '// '+ REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', ''), '<font color=black>',''), '</font>', ''), '<br>', '') AS cause_ex, REPLACE(REPLACE(tbl3.create_user, 'EU\\', ''), '_', '-') AS create_user, tbl3.create_date, tbl4.operator, tbl4.tester, tbl4.workplace, tbl1.transistor_type, tbl1.chip_configuration, tbl1.lead_frame, tbl1.soft_solder, tbl1.bond_wire2, tbl1.article \
        FROM tbl1 \
        LEFT JOIN tbl2 \
        ON tbl2.lot = tbl1.a_lot \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot \
        LEFT JOIN tbl4 \
        ON tbl4.lot = tbl1.a_lot \
        WHERE quality_id <> 0 \
        ORDER BY quality_id DESC"

        df_a4 = pd.read_sql(query, conn)

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
        df_a4['transistor_type'].fillna("-", inplace=True)
        df_a4['ship_package'].fillna("-", inplace=True)
        df_a4['lead_frame'].fillna("-", inplace=True)
        df_a4['cause_ex'].fillna("-", inplace=True)

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
                    {'name': 'LS Nummber', 'id': 'ba'},
                    {'name': 'Typ', 'id': 'device'},
                    {'name': 'WPS', 'id': 'wps'},
                    {'name': 'FA', 'id': 'fa'},
                    {'name': 'Lieferung', 'id': 'release'},
                    {'name': 'Schrott', 'id': 'scrapped'},
                    {'name': 'Rejected', 'id': 'rejected'},
                    {'name': 'Output', 'id': 'final_test_output'},
                    {'name': 'Auebeute', 'id': 'final_test_yield'},
                    {'name': 'Ursache', 'id': 'cause_ex'},
                    {'name': 'Erstellungsdatum', 'id': 'create_date'},
                    {'name': 'Editdatum', 'id': 'edit_date'},
                    {'name': 'Editer', 'id': 'edit_user'},
                    {'name': 'Wafer (Menge(probed/unprobed))', 'id': 'wafer_info'}]

        return df_a4.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'),columns_s, page_count


    elif what_data2 == "comment":
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, ZNGProduction.catuno.tbl_lots.ba, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, ZNGProduction.catuno.tbl_products.article \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
        ), \
        tbl2 AS ( \
        SELECT lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), '; ') AS wafer_info \
        FROM \
        ( \
        SELECT lot, wafer_lot + ': ' + CAST(wafer_quantity as VARCHAR(100))  + '(' + probed + ')' AS wafer_info \
        FROM ZNGProduction.catuno.tbl_wafers \
        WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' \
        ) tbl0 \
        GROUP BY lot \
        ), \
        tbl3 AS ( \
        SELECT ZNGFinalTest.quality.vw_lots.release, ZNGFinalTest.quality.vw_lots.scrapped, ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ), \
        tbl4 AS ( \
        SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator \
        FROM ZNGFinalTest.final_test3.tbl_summaries \
        GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
        ) \
        SELECT tbl1.a_lot, tbl1.ba, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.department, tbl1.package, tbl1.bond_wire, tbl3.release, tbl3.scrapped, tbl1.ship_package, tbl1.uk_input, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.comment, '<div>',''), '</div>', '.'), '<br>','; '), '</font>',''), '&gt;', '<'), '-&lt;','>') AS comment,  REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END + '// '+ REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', ''), '<font color=black>',''), '</font>', ''), '<br>', '') AS cause_ex, REPLACE(REPLACE(tbl3.create_user, 'EU\\', ''), '_', '-') AS create_user, tbl3.create_date, tbl4.operator, tbl4.tester, tbl4.workplace, tbl1.transistor_type, tbl1.chip_configuration, tbl1.lead_frame, tbl1.soft_solder, tbl1.bond_wire2, tbl1.article \
        FROM tbl1 \
        LEFT JOIN tbl2 \
        ON tbl2.lot = tbl1.a_lot \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot \
        LEFT JOIN tbl4 \
        ON tbl4.lot = tbl1.a_lot \
        WHERE quality_id <> 0 \
        ORDER BY quality_id DESC"

        df_a4 = pd.read_sql(query, conn)

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
        df_a4['transistor_type'].fillna("-", inplace=True)
        df_a4['ship_package'].fillna("-", inplace=True)
        df_a4['lead_frame'].fillna("-", inplace=True)
        df_a4['cause_ex'].fillna("-", inplace=True)

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
                    {'name': 'LS Nummber', 'id': 'ba'},
                    {'name': 'Typ', 'id': 'device'},
                    {'name': 'Wire1', 'id': 'bond_wire'},
                    {'name': 'WPS', 'id': 'wps'},
                    {'name': 'FA', 'id': 'fa'},
                    {'name': 'Lieferung', 'id': 'release'},
                    {'name': 'Schrott', 'id': 'scrapped'},
                    {'name': 'Rejected', 'id': 'rejected'},
                    {'name': 'Output', 'id': 'final_test_output'},
                    {'name': 'Auebeute', 'id': 'final_test_yield'},
                    {'name': 'Ursache', 'id': 'cause_ex'},
                    {'name': 'Ersteller', 'id': 'create_user'},
                    {'name': 'Erstellungsdatum', 'id': 'create_date'},
                    {'name': 'Editer', 'id': 'edit_user'},
                    {'name': 'Editdatum', 'id': 'edit_date'},
                    {'name': 'Comment', 'id': 'comment'}
                    ]

        return df_a4.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'),columns_s, page_count

    elif what_data2 == "storage":
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, ZNGProduction.catuno.tbl_lots.ba, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, ZNGProduction.catuno.tbl_products.article \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
        ), \
        tbl2 AS ( \
        SELECT lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), '; ') AS wafer_info \
        FROM \
        ( \
        SELECT lot, wafer_lot + ': ' + CAST(wafer_quantity as VARCHAR(100))  + '(' + probed + ')' AS wafer_info \
        FROM ZNGProduction.catuno.tbl_wafers \
        WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' \
        ) tbl0 \
        GROUP BY lot \
        ), \
        tbl3 AS ( \
        SELECT ZNGFinalTest.quality.vw_lots.release, ZNGFinalTest.quality.vw_lots.scrapped, ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ), \
        tbl4 AS ( \
        SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator \
        FROM ZNGFinalTest.final_test3.tbl_summaries \
        GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
        ), \
        tbl5 AS ( \
        SELECT lot, STRING_AGG(CAST(box_class AS NVARCHAR(MAX)), '; ') AS box_class \
        FROM ( \
        SELECT lot, STR(box_number)+ ': ' + class AS box_class \
        FROM ( \
        SELECT DISTINCT lot, CASE WHEN container_object_id = 2000001 THEN 0 WHEN container_object_id IS NULL THEN 0 ELSE container_object_id END AS box_number, class \
        FROM ZNGFinalTest.final_test3.tbl_samples \
        WHERE lot NOT LIKE '1%' AND lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' AND (container_object_id <> 2000015) \
        ) tbl000 \
        WHERE box_number <> 0 \
        ) tlb001 \
        GROUP BY lot \
        )  \
        SELECT tbl1.a_lot, tbl1.ba, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.department, tbl1.package, tbl1.bond_wire, tbl3.release, tbl3.scrapped, tbl1.ship_package, tbl1.uk_input, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.comment, '<div>',''), '</div>', '.'), '<br>','; '), '</font>',''), '&gt;', '<'), '-&lt;','>') AS comment,  REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END + '// '+ REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', ''), '<font color=black>',''), '</font>', ''), '<br>', '') AS cause_ex, REPLACE(REPLACE(tbl3.create_user, 'EU\\', ''), '_', '-') AS create_user, tbl3.create_date, tbl4.operator, tbl4.tester, tbl4.workplace, tbl1.transistor_type, tbl1.chip_configuration, tbl1.lead_frame, tbl1.soft_solder, tbl1.bond_wire2, tbl1.article, tbl5.box_class \
        FROM tbl1 \
        LEFT JOIN tbl2 \
        ON tbl2.lot = tbl1.a_lot \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot \
        LEFT JOIN tbl4 \
        ON tbl4.lot = tbl1.a_lot \
        LEFT JOIN tbl5 \
        ON tbl5.lot = tbl1.a_lot \
        WHERE quality_id <> 0 \
        ORDER BY quality_id DESC"

        df_a4 = pd.read_sql(query, conn)

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

        df_a4['comment'].fillna('<p>', inplace=True)
        df_a4['comment'] = df_a4['comment'].map(strip_tags)
        df_a4['transistor_type'].fillna("-", inplace=True)
        df_a4['ship_package'].fillna("-", inplace=True)
        df_a4['lead_frame'].fillna("-", inplace=True)
        df_a4['cause_ex'].fillna("-", inplace=True)

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
                    {'name': 'LS Nummber', 'id': 'ba'},
                    {'name': 'Typ', 'id': 'device'},
                    {'name': 'WPS', 'id': 'wps'},
                    {'name': 'FA', 'id': 'fa'},
                    {'name': 'Lieferung', 'id': 'release'},
                    {'name': 'Schrott', 'id': 'scrapped'},
                    {'name': 'Rejected', 'id': 'rejected'},
                    {'name': 'Output', 'id': 'final_test_output'},
                    {'name': 'Auebeute', 'id': 'final_test_yield'},
                    {'name': 'Ursache', 'id': 'cause_ex'},
                    {'name': 'Storage', 'id': 'box_class'}]


                #     {'name': '-', 'id': 'index'},
                # {'name': 'Q-ID', 'id': 'quality_id'},
                # {'name': 'Charge', 'id': 'a_lot'},
                # {'name': 'LS Nummber', 'id': 'ba'},
                # {'name': 'Typ', 'id': 'device'},
                # {'name': 'WPS', 'id': 'wps'},
                # {'name': 'FA', 'id': 'fa'},
                # {'name': 'Lieferung', 'id': 'release'},
                # {'name': 'Schrott', 'id': 'scrapped'},
                # {'name': 'Ursache', 'id': 'cause_ex'},
                # {'name': 'Ersteller', 'id': 'create_user'},
                # {'name': 'Erstellungsdatum', 'id': 'create_date'},
                # {'name': 'Editer', 'id': 'edit_user'},
                # {'name': 'Editdatum', 'id': 'edit_date'},
                # {'name': 'Comment', 'id': 'comment'},
                # {'name': 'GW', 'id': 'final_test_para_fails'},
                # {'name': 'TA', 'id': 'final_test_gross_fails'},
                # {'name': 'Rejected', 'id': 'rejected'},
                # {'name': 'Output', 'id': 'final_test_output'},
                # {'name': 'Auebeute', 'id': 'final_test_yield'},
                # {'name': 'LieferD.', 'id': 'delivery_date'},
                # {'name': 'Transistor', 'id': 'transistor_type'},
                # {'name': 'Gurt', 'id': 'ship_package'},
                # {'name': 'Package', 'id': 'package'},
                # {'name': 'Group', 'id': 'device_group'},
                # {'name': 'Leadframe', 'id': 'lead_frame'},
                # {'name': 'Wire1', 'id': 'bond_wire'},
                # {'name': 'Wire2', 'id': 'bond_wire2'},
                # {'name': 'Soft Solder', 'id': 'soft_solder'},
                # {'name': 'Article', 'id': 'article'},
                # {'name': 'Storage', 'id': 'box_class'},
                # {'name': 'Wafer (Menge(probed/unprobed))', 'id': 'wafer_info'}]

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
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                           user='WebServer',
                           password='W3bS3rv3r',
                           database='ZNGFinalTest')
    query_Q_plot = "WITH tbl1 AS ( \
    SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, ZNGProduction.catuno.tbl_lots.ba, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, ZNGProduction.catuno.tbl_products.article \
    FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
    LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
    ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
    LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
    ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
    WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
    ), \
    tbl2 AS ( \
    SELECT lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), '; ') AS wafer_info \
    FROM \
    ( \
    SELECT lot, wafer_lot + ': ' + CAST(wafer_quantity as VARCHAR(100))  + '(' + probed + ')' AS wafer_info \
    FROM ZNGProduction.catuno.tbl_wafers \
    WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' \
    ) tbl0 \
    GROUP BY lot \
    ), \
    tbl3 AS ( \
    SELECT ZNGFinalTest.quality.vw_lots.release, ZNGFinalTest.quality.vw_lots.scrapped, ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
    FROM ZNGFinalTest.quality.vw_last_comments \
    JOIN ZNGFinalTest.quality.vw_lots \
    ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
    JOIN ZNGFinalTest.quality.tbl_classes \
    ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
    ), \
    tbl4 AS ( \
    SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator \
    FROM ZNGFinalTest.final_test3.tbl_summaries \
    GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
    ) \
    SELECT tbl1.a_lot, tbl1.ba, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.department, tbl1.package, tbl1.bond_wire, tbl3.release, tbl3.scrapped, tbl1.ship_package, tbl1.uk_input, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.comment, '<div>',''), '</div>', '.'), '<br>','; '), '</font>',''), '&gt;', '<'), '-&lt;','>') AS comment,  REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END + '// '+ REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', ''), '<font color=black>',''), '</font>', ''), '<br>', '') AS cause_ex, REPLACE(REPLACE(tbl3.create_user, 'EU\\', ''), '_', '-') AS create_user, tbl3.create_date, tbl4.operator, tbl4.tester, tbl4.workplace, tbl1.transistor_type, tbl1.chip_configuration, tbl1.lead_frame, tbl1.soft_solder, tbl1.bond_wire2, tbl1.article \
    FROM tbl1 \
    LEFT JOIN tbl2 \
    ON tbl2.lot = tbl1.a_lot \
    LEFT JOIN tbl3 \
    ON tbl3.lot = tbl1.a_lot \
    LEFT JOIN tbl4 \
    ON tbl4.lot = tbl1.a_lot \
    WHERE quality_id <> 0 \
    ORDER BY quality_id DESC"

    df_Q_plot = pd.read_sql(query_Q_plot, conn)

    df_Q_plot['year'] =  df_Q_plot['create_date'].dt.year
    df_Q_plot['month'] = df_Q_plot['create_date'].dt.month
    df_Q_plot['week'] = df_Q_plot['create_date'].dt.week
    df_Q_plot['day'] = df_Q_plot['create_date'].dt.day

    df_Q_plot['cause'].fillna('<p>', inplace=True)
    df_Q_plot['cause'] = df_Q_plot['cause'].map(strip_tags)


    if time_period == 'alltime':
        if second_value == 'Die Anzahl':
            lst = []
            for i, j in df_Q_plot.groupby(['year', 'month'])['a_lot'].count().index:
                 lst.append(str(i) + '_' + str(j))

            fig_Q_1 = go.Figure(
                            data = [go.Bar(
                                        x = lst,
                                        y = df_Q_plot.groupby(['year', 'month'])['a_lot'].count().values,
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

            fig_Q_1.layout.yaxis.update(title = 'title axis',
                                    # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                    # showgrid =True
                                    )

            return fig_Q_1
        elif second_value == 'Package':
            fig_Q_1 = go.Figure(
                            data = [go.Bar(
                                        x = df_Q_plot.groupby('package')['a_lot'].count().sort_values(ascending=False).index,
                                        y = df_Q_plot.groupby('package')['a_lot'].count().sort_values(ascending=False).values,
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

            fig_Q_1.layout.yaxis.update(title = 'title axis',
                                    # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                    # showgrid =True
                                    )

            return fig_Q_1
        elif second_value == 'Device Grop':
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

            fig_Q_1.layout.yaxis.update(title = 'title axis',
                                    # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                    # showgrid =True
                                    )

            return fig_Q_1
    elif time_period == 'year':
        if second_value == '2018':
            if third_value == 'per Class':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['class_name'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
            elif third_value == 'per Wire':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['bond_wire'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
            elif third_value == 'per Package':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2018]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['package'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
        elif second_value == '2019':
            if third_value == 'per Class':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['class_name'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
            elif third_value == 'per Wire':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['bond_wire'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
            elif third_value == 'per Package':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2019]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['package'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
        elif second_value == '2020':
            if third_value == 'per Class':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['class_name'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['class_name'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
            elif third_value == 'per Wire':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['bond_wire'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['bond_wire'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1
            elif third_value == 'per Package':
                df_Q_plot = df_Q_plot[df_Q_plot['year'] == 2020]

                fig_Q_1 = go.Figure(
                                data = [go.Bar(
                                            x=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().index,
                                            y=df_Q_plot[df_Q_plot['package'] == i].groupby(['month'])['a_lot'].count().values,
                                            name = i) for i in list(df_Q_plot['package'].unique())
                                        ],
                                layout = go.Layout(
                                            title = 'title',
                                            # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                            # paper_bgcolor='white',
                                            # plot_bgcolor= '#d6e5fa',
                                            # autosize = False,
                                            # width = 1500,
                                            # height = 380,
                                            barmode='stack',
                                            hovermode = 'x',
                                            # legend_orientation="h",
                                            # legend=dict(x=0.1, y=1.0)
                                                ))

                fig_Q_1.layout.yaxis.update(title = 'title axis',
                                        # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                        # showgrid =True
                                        )

                return fig_Q_1

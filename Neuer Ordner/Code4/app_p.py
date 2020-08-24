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
# import json
import math

sort_dict = { 'SÄGEN': 1,
              'BONDEN': 2,
              'BESCHN.OBERER PERF.RAND': 3,
              'VERPLASTEN': 4,
              'DEFLASHEN': 5,
              'VERZINNEN': 6,
              'QC NACH AF':7,
              'LASERCODIEREN':8,
              'VEREINZELN':9,
              'ENDMESSEN':10,
              'GURTEN':11,
              'QC':12,
              'AUSLIEFERN':13,
              'WASCHEN/KONTROLLE':14,
              'AUSGANGSKONTROLLE VZ':15,
              'MAGNETISIEREN':16,
              'DICHTSTEG AUSSCHNEIDEN':17}

bar_colour_dict = {'Erledigt':'#53d397', 'Läuft':'#ff7a5c', 'Vor dem Beginn des Schritts':'#79b8d1', 'Qualitätsproblem':'#d1478c'}

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

PAGE_SIZE = 10


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(id = 'body-container' ,children=[
                                html.Div(children=html.H5(children='Production Dashboard'), style={'marginLeft': '10px', 'marginTop':'15px', 'marginBottom': '0px'}),
                                html.Div(className= 'content-box1', children=[html.Label(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Lot amount</strong>')),
                                        dcc.Slider(id='lot-slider',min=150, max=1500, step=1,
                                            marks={
                                                    150: '150',
                                                    250: '250',
                                                    500: '500',
                                                    750: '750',
                                                    1000: '1000',
                                                    1250: '1250',
                                                    1500: '1500'
                                            },
                                            value=500)],
                                            style = {'position':'relative', 'width': '400px', 'height': '80px', 'display': 'inline-block', 'float': 'left', 'padding': '8px', 'marginLeft': '10px','marginTop': '10px'}),
                                html.Div(className= 'content-box2', id='slider-number-displayer',
                                            style = { 'position':'relative', 'left':'4px', 'width': '140px', 'height': '80px', 'display': 'inline-block', 'float': 'left', 'padding': '8px', 'paddingTop':'15px','marginLeft': '10px','marginTop': '10px'}),
                                html.Div(className= 'content-box2', id='lot-ratio-calculator',
                                            style = { 'position':'relative', 'left':'8px', 'width': '580px', 'height': '80px', 'display': 'inline-block', 'float': 'left', 'padding': '8px', 'paddingTop':'15px','marginLeft': '10px','marginTop': '10px'}),
                                html.Div(className= 'content-box3', id='lot-container_e',
                                            style = { 'position':'relative', 'left':'8px', 'width': '190px', 'height': '80px', 'display': 'inline-block', 'float': 'left', 'padding': '8px', 'paddingTop':'5px','marginLeft': '10px','marginTop': '10px'}),
                                html.Div(className="graph-container-1", children=[
                                        dcc.Graph(id='pie-chart')],
                                                style = {'position':'relative', 'width': '600px', 'height': '460px', 'marginLeft': '8px', 'marginTop': '13px', 'display': 'inline-block', 'float':'left'}),
                                html.Div(className="graph-container-2", children=[
                                        dcc.Graph(id='bar-chart')],
                                                style = {'position':'relative', 'left': '8px','width': '735px', 'height': '460px', 'marginLeft': '8px', 'marginTop': '13px', 'display': 'inline-block', 'float':'left'}),
                                html.Div(className="graph-container-3", children=[
                                        dcc.Graph(id='box-plot')],
                                                style = {'position':'relative', 'width': '1352px', 'height': '470px', 'marginLeft': '8px', 'marginTop': '13px', 'display': 'inline-block', 'float':'left'}),
                                html.Br(),
                                html.Div(className="table-container", children=[
                                        dash_table.DataTable(id='pdata-table',
                                         page_current=0,
                                         page_size=PAGE_SIZE,
                                         page_action='custom',

                                         filter_action='custom',
                                         filter_query='',

                                         sort_action='custom',
                                         sort_mode='multi',
                                         sort_by=[],
                                         row_selectable='single',
                                         selected_rows=[],
                                         columns =[
                                                     # {'name': '-', 'id': 'index'},
                                                     {'name': 'Charge', 'id': 'a_lot'},
                                                     {'name': 'Tpy', 'id': 'device'},
                                                     {'name': 'Tpy Grouppe', 'id': 'device_group'},
                                                     {'name': 'Shritt', 'id': 'current_step'},
                                                     {'name': 'Step Progress', 'id': 'progress2_comment_2'},
                                                     {'name': 'Total Progress (%)', 'id': 'progress2'},
                                                     {'name': 'Progress comment', 'id': 'comment_for_lot_step'},
                                                     {'name': 'Editdatum', 'id': 'ongoing_done_date'},
                                                     {'name': 'Q-ID', 'id': 'quality_id'}
                                                     ],

                                         style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
                                         style_cell={'backgroundColor': 'white',
                                                    'color': 'black',
                                                    'textAlign': 'center',
                                                    'font-family': 'Overpass',
                                                    'font-size': '0.95rem'},
                                         style_table={
                                                    # 'title': 'Datatable',
                                                    # 'maxWidth': '100%',
                                                    # 'maxHeight': '800px',
                                                    'overflowX': 'scroll',
                                                    'textOverflow': 'auto'},
                                                    )
                                                        ], style = {'position':'relative', 'width': '1352px', 'height': '430px', 'marginLeft': '8px', 'marginTop': '13px', 'display': 'inline-block', 'float':'left'}),
                                html.Br(),
                                html.Div(className="selected-lot-displayer", id='selected-lot-container-id', children=[
                                            dash_table.DataTable(id='p-s-data-table',

                                             page_action='native',

                                             columns =[
                                                         {'name': 'LS #', 'id': 'ba'},
                                                         {'name': 'Charge', 'id': 'a_lot'},
                                                         {'name': 'Tpy', 'id': 'device'},
                                                         {'name': 'Workstep#', 'id': 'workstep_id'},
                                                         {'name': 'Workstep', 'id': 'workstep_name'},
                                                         {'name': 'Input', 'id': 'input'},
                                                         {'name': 'Reject', 'id': 'reject'},
                                                         {'name': 'Output', 'id': 'output'},
                                                         {'name': 'Datum', 'id': 'done_date'}
                                                         ],

                                             style_header={'backgroundColor': 'white', 'fontWeight': 'bold'},
                                             style_cell={'backgroundColor': 'white',
                                                        'color': 'black',
                                                        'textAlign': 'center',
                                                        'font-family': 'Overpass',
                                                        'font-size': '0.95rem'},
                                             style_table={
                                                        # 'title': 'Datatable',
                                                        # 'maxWidth': '100%',
                                                        # 'maxHeight': '800px',
                                                        'overflowX': 'scroll',
                                                        'textOverflow': 'auto'},
                                                        )
                                        ], style = {'position':'relative', 'width': '1352px', 'height': '500px', 'marginLeft': '8px', 'marginTop': '13px', 'marginBottom': '75px','display': 'inline-block', 'float':'left'}),
                                html.Br()
                                        ])

@app.callback(
            [Output('slider-number-displayer', 'children'),
            Output('lot-ratio-calculator', 'children'),
            Output('lot-container_e', 'children'),
            Output('pie-chart', 'figure'),
            Output('bar-chart', 'figure'),
            Output('box-plot', 'figure'),
            Output('pdata-table','data'),
            # Output('pdata-table','columns'),
            Output('pdata-table', 'page_count')],
            [Input('lot-slider', 'value'),
            Input('pdata-table', "page_current"),
            Input('pdata-table', "page_size"),
            Input('pdata-table', "sort_by"),
            Input('pdata-table', "filter_query")])
def update_output(lot_slider,page_current, page_size, sort_by, filter):
    # load data
    df_app5 = pd.read_csv("output2.txt")

    # data cleaning for sen and slider
    df_app5 =df_app5[df_app5['package'] != 'SEN']
    df_app5.reset_index(inplace=True, drop=True)

    # date time
    df_app5['beginning_done_date'] = pd.to_datetime(df_app5['beginning_done_date'], errors='coerce')
    df_app5['ongoing_done_date'] = pd.to_datetime(df_app5['ongoing_done_date'], errors='coerce')

    # sub dataset for display
    df_app5_sub = df_app5[:int(lot_slider)]
    df_app5_sub.reset_index(inplace=True, drop=True)

    # released lot amount
    ###released_lot_amount = str(df_app5_sub['current_step'].value_counts()['AUSLIEFERN'])
    released_lot_amount = str(df_app5_sub['comment_for_lot_step'].value_counts()['Ausgeliefert'])

    #released lot percentage
    ###released_percent = str(round(100*df_app5_sub['current_step'].value_counts()['AUSLIEFERN']/lot_slider, 2))
    released_percent = str(round(100*df_app5_sub['comment_for_lot_step'].value_counts()['Ausgeliefert']/lot_slider, 2))

    # released lot total yield
    df_app5_yield = df_app5_sub[(df_app5_sub['progress'] !=0) & (df_app5_sub['progress'] != np.inf)]
    released_lot_total_yield = str(round(100*df_app5_yield[df_app5_yield['comment_for_lot_step'] == 'Ausgeliefert']['progress'].mean(),2))

    # all time yield and released lot yield comparison
    all_released_lot_yield_mean =  round(100*df_app5[df_app5['package'] != 'SEN'][df_app5['comment_for_lot_step'] == 'Ausgeliefert'][(df_app5['progress'] != 0) & (df_app5['progress'] != np.inf)]['progress'].mean(), 2)

    if float(all_released_lot_yield_mean) > float(released_lot_total_yield):
        yield_diff = float(released_lot_total_yield) - float(all_released_lot_yield_mean)
        released_lot_total_yield = '<font color="red">' +  released_lot_total_yield + '</font>' + '% (<font color="red">' + str(round(yield_diff,2)) + '↓</font>)'
    elif float(all_released_lot_yield_mean) < float(released_lot_total_yield):
        yield_diff = float(released_lot_total_yield) - float(all_released_lot_yield_mean)
        released_lot_total_yield = '<font color="green">' +  released_lot_total_yield  + '</font>' + '% (<font color="green">+' + str(round(yield_diff,2)) + '↑</font>)'
    else:
        released_lot_total_yield = released_lot_total_yield  + '% (-)'

    # ready lot amount
    ready_lots = str(len(df_app5_sub[df_app5_sub['comment_for_lot_step'] == 'Vorbereitungen für den Start']))
    problem_lots = str(len(df_app5_sub[(df_app5_sub['comment_for_lot_step'] == 'Verschotten') | (df_app5_sub['comment_for_lot_step'] == 'Gesperrt') | (df_app5_sub['comment_for_lot_step'] == 'Qualitätsproblem')]))

    # df_for_duration
    df_for_duration = df_app5_sub[(df_app5_sub['comment_for_lot_step'] == 'Ausgeliefert') & (df_app5_sub['beginning_done_date'].notnull()) & (df_app5_sub['ongoing_done_date'].notnull())]
    duration_for_production = (df_for_duration['ongoing_done_date']  - df_for_duration['beginning_done_date']).mean()

    # process duration compariosn
    all_released_lot_duration =  df_app5[(df_app5['comment_for_lot_step'] == 'Ausgeliefert') & (df_app5['beginning_done_date'].notnull()) & (df_app5['ongoing_done_date'].notnull())]
    duration_for_all_production = (all_released_lot_duration['ongoing_done_date']  - all_released_lot_duration['beginning_done_date']).mean()

    duration_diff = duration_for_all_production.days - duration_for_production.days

    if duration_for_all_production.days > duration_for_production.days:
        duration_for_production = '<font color="green">' + str(duration_for_production.days) + '</font>' + ' (<font color="green">-' + str(duration_diff) + '</font>)'
    elif duration_for_all_production.days < duration_for_production.days:
        duration_for_production = '<font color="red">' + str(duration_for_production.days) + '</font>' + ' (<font color="red">+' + str(abs(duration_diff)) +'</font>)'
    else:
        duration_for_production = '<font color="black">' + str(duration_for_production.days) + '</font>' + ' (<font color="black">+' + str(duration_diff) +'</font>)'

    ####### chart data #######
    chart_df = df_app5_sub[(df_app5_sub['comment_for_lot_step'] != 'Ausgeliefert') & (df_app5_sub['comment_for_lot_step'] != 'Verschotten') & (df_app5_sub['comment_for_lot_step'] != 'Gesperrt') & (df_app5_sub['progress'] != -0.01)]

    ####### piechart #######
    pie_plot = chart_df['current_step'].value_counts()

    layout_pie = go.Layout(
                        title='Running lots',
                        legend=dict(x=1.3, y=0.95)
                          )
    fig_pie = go.Figure(
                    data=[
                        go.Pie
                            (labels=pie_plot.index,
                            values=pie_plot.values)
                            ],
                    layout = layout_pie
                        )
    # fig_pie.update_layout(
    #                     yaxis_title="Day"
    #                         )

    ####### stacked barchart #######
    bar_pre_data = chart_df.pivot_table(index='current_step', columns='progress2_comment_2',  values='a_lot',aggfunc= lambda x: len(x))

    oder_index = bar_pre_data.reset_index()['current_step'].replace({'SÄGEN': 1,
                                                                    'BONDEN': 2,
                                                                    'BESCHN.OBERER PERF.RAND': 3,
                                                                    'VERPLASTEN': 4,
                                                                    'DICHTSTEG AUSSCHNEIDEN':5,
                                                                    'DEFLASHEN': 6,
                                                                    'AUSGANGSKONTROLLE VZ':7,
                                                                    'VERZINNEN': 8,
                                                                    'QC NACH AF':9,
                                                                    'VEREINZELN':10,
                                                                    'WASCHEN/KONTROLLE':11,
                                                                    'ENDMESSEN':12,
                                                                    'LASERCODIEREN':13,
                                                                    'GURTEN':14,
                                                                    'QC':15,
                                                                    'AUSLIEFERN':16,
                                                                    'MAGNETISIEREN':17})
    bar_pre_data['order_index'] = oder_index.values
    # list for bar data
    data_bar_list = list(bar_pre_data)
    data_bar_list.remove('order_index')
    data_bar = [go.Bar(x=bar_pre_data.sort_values('order_index')[progress].index,
                       y=bar_pre_data.sort_values('order_index')[progress].values,
                       name=progress,
                       marker=dict(color=bar_colour_dict[progress])) for progress in data_bar_list]

    layout_bar = go.Layout(
                            title='Process information for each step',
                            barmode='stack',
                            yaxis_title='Number of lots',
                            legend=dict(
                                        x=0,
                                        y=-0.5,
                                        orientation="h")
                                        )

    fig_bar = go.Figure(data=data_bar, layout=layout_bar)

    ####### box plot #######
    chart_df['duration'] = chart_df['ongoing_done_date'] - chart_df['beginning_done_date']
    chart_df['duration'] = chart_df['duration'].dt.days

    box_df = chart_df[chart_df['progress2_comment_2'] == 'Erledigt']

    data_box = [go.Box(y=box_df[box_df['current_step'] == step]['duration'], name= step, boxpoints='all') for step in ['SÄGEN', 'BONDEN', 'BESCHN.OBERER PERF.RAND', 'VERPLASTEN', 'DICHTSTEG AUSSCHNEIDEN','DEFLASHEN',\
    'AUSGANGSKONTROLLE VZ','VERZINNEN','QC NACH AF','VEREINZELN', 'WASCHEN/KONTROLLE', \
    'ENDMESSEN', 'LASERCODIEREN','GURTEN', 'QC', 'AUSLIEFERN', 'MAGNETISIEREN']]

    layout_box = go.Layout(
        title='Time taken to each process from the beginning (completed lots)',
        yaxis_title='Time taken (day)',
        legend=dict())
    fig_box = go.Figure(data=data_box, layout=layout_box)


    ####### data table #######
    # reset index only for data table
    table_data = chart_df.reset_index(drop=False)

    # progress over 1 to 1
    for i in table_data.index:
        if table_data['progress2'].iloc[i] > 1:
            table_data['progress2'].iloc[i] = 1
        else:
            pass
    # progress percentage
    table_data['progress2'] = (table_data['progress2']*100).round()

    #date time to str
    table_data['ongoing_done_date'] = table_data['ongoing_done_date'].astype(str)

    ################# filter code #################
    filtering_expressions = filter.split(' && ')

    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            table_data = table_data.loc[getattr(table_data[col_name], operator)(filter_value)]
        elif operator == 'contains':
            table_data = table_data.loc[table_data[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            table_data = table_data.loc[table_data[col_name].str.startswith(filter_value)]

    if len(sort_by):
        table_data = table_data.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    # pagination
    page_count = math.ceil(len(table_data['a_lot'])/page_size)
    ################# #################

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("          PRODUCTION           ")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>{}</strong> lots'.format(lot_slider)), dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>{}</strong> lots (<strong>{}%</strong>) released <span id = "yield_span">avg. yield: <strong>{}</strong></span>'.format(released_lot_amount, released_percent, released_lot_total_yield)), \
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML('Avg. Period : <strong>{}</strong> days <br><font color="orange"><strong>{}</strong></font> lots blocked or Q-issue <br> <font color="blue"><strong>{}</strong></font> lots before start'.format(duration_for_production, problem_lots, ready_lots)), \
    fig_pie, fig_bar, fig_box, table_data.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'), page_count

@app.callback(
    Output('p-s-data-table', "data"),
    [Input('pdata-table', "derived_virtual_data"),
    Input('pdata-table', "derived_virtual_selected_rows")])
def update_selected_row(rows, derived_virtual_data):
    # if derived_virtual_selected_rows is None:
    #     derived_virtual_selected_rows = []
    dff = pd.DataFrame.from_dict({'a_lot':[1,2,3], 'aaa': [4,5,6]}) if rows is None else pd.DataFrame(rows)
    # print(dff)
    # print(dff.iloc[derived_virtual_data]['a_lot'])
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                           user='WebServer',
                           password='W3bS3rv3r',
                           database='ZNGFinalTest')
    query_selected = "WITH tbl1 AS ( \
    SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration, ZNGProduction.catuno.tbl_products.soft_solder, ZNGProduction.catuno.tbl_products.bond_wire2, \
    ZNGProduction.catuno.tbl_products.article \
    FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
    LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
    ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
    LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
    ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
    WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
    ), \
    tbl5 AS ( \
    SELECT DISTINCT ZNGProduction.catuno.tbl_lots.ba, ZNGProduction.catuno.tbl_lots.lot, ZNGProduction.catuno.tbl_manufacture.workstep_id, ZNGProduction.catuno.tbl_manufacture.workstep_name, ZNGProduction.catuno.tbl_manufacture.input, ZNGProduction.catuno.tbl_manufacture.reject, ZNGProduction.catuno.tbl_manufacture.output, ZNGProduction.catuno.tbl_manufacture.date AS done_date \
    FROM ZNGProduction.catuno.tbl_manufacture \
    FULL JOIN ZNGProduction.catuno.tbl_lots \
    ON ZNGProduction.catuno.tbl_lots.ba = ZNGProduction.catuno.tbl_manufacture.ba \
    ) \
    SELECT DISTINCT tbl1.a_lot, tbl5.ba, tbl1.device, tbl5.workstep_id, tbl5.workstep_name, tbl5.input, tbl5.reject, tbl5.output, tbl5.done_date \
    FROM tbl1 \
    JOIN tbl5 \
    ON tbl5.lot = tbl1.a_lot \
    WHERE device <> 'FMMT614' AND workstep_id IS NOT NULL AND a_lot NOT LIKE 'Z%' AND a_lot = '{}'\
    ORDER BY a_lot DESC, workstep_id, input DESC".format(dff.iloc[derived_virtual_data]['a_lot'].values[0])

    selected_lot_process = pd.read_sql(query_selected, conn)
    # data cleaning
    ## datetime to StringIO
    selected_lot_process['done_date'] = selected_lot_process['done_date'].astype(str)

    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("          PRODUCTION           ")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

    return selected_lot_process.to_dict('records')

if __name__ == '__main__':
    # app.run_server(debug=False, port=8050, host='0.0.0.0')
    app.run_server(debug=False)

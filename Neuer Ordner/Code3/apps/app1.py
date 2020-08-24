import numpy as np
import pandas as pd
# import pyodbc
import pymssql
from datetime import date


import dash
import plotly.graph_objects as go
import dash_core_components as dcc
import plotly.offline as py
import dash_dangerously_set_inner_html
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

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
    html.Div(className="content-container", children=[
    html.H1(id = 'today-update', className= 'app_title'),
    html.Div(id='table-update',style = {'paddingRight': '5%', 'paddingLeft': '5%', 'paddingTop' : '1%'}), html.P(id = 'last-update'),
    html.P(),
    html.Br()
                ], style = {'width': '1325px', 'marginLeft': '15px', 'marginTop': '50px', 'marginBottom': '35px', 'paddingBottom': '35px'}),
    dcc.Interval(
        id='interval-component',
        interval=1*3600000, # in milliseconds
        n_intervals=0)
])

@app.callback(Output('today-update', 'children'),
                [Input('interval-component', 'n_intervals')])
def today(n):
    return 'AZQ List am {}'.format(date.today().strftime("%d/%h/%Y"))


@app.callback([Output('table-update', 'children'),
               Output('last-update', 'children')],
              [Input('interval-component', 'n_intervals')])
def generate_table(n,max_rows=30):
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                       user='WebServer',
                       password='W3bS3rv3r',
                       database='ZNGFinalTest')

    query = "WITH tbl3 AS (SELECT '<strong>' + product + '</strong>'+ '<br><br>Q-ID: ' + '<strong>'+str(quality_id) + '</strong>' + '<br>' + 'FA: ' + CASE WHEN fa = 0 THEN 'X' ELSE 'O' END + ' \ WPS: ' + CASE WHEN wps = 0 THEN 'X' ELSE 'O' END AS Typ, lot AS Lot, '<p>' + TRIM(REPLACE(wafers, '&#x0D;', '<br>')) + '</p>'  AS Wafers, FORMAT(affected, '0, k') AS affected, FORMAT(bonding_goods, '0,k ') AS bonding_goods, CONCAT(class, ': ' , cause) AS Ausfallursache, create_date,  REPLACE(REPLACE(create_user,'EU\',''),'_',' ') AS create_user, comment AS [Status], edit_date, REPLACE(REPLACE(edit_user,'EU\',''),'_',' ') AS edit_user \
    FROM ( \
    SELECT ZNGFinalTest.quality.tbl_lots.quality_id, ZNGFinalTest.quality.tbl_lots.ba, quality.tbl_lots.lot, ZNGFinalTest.quality.tbl_lots.product, ZNGFinalTest.quality.tbl_states.state_name AS state, ZNGFinalTest.quality.tbl_classes.class_name AS class, ZNGFinalTest.catuno.vw_wafers_list.wafers, ZNGFinalTest.quality.tbl_lots.affected,  \
    tbl1.output AS bonding_goods, ZNGFinalTest.quality.vw_last_comments.comment, ZNGFinalTest.quality.tbl_lots.cause, ZNGFinalTest.quality.tbl_lots.release, ZNGFinalTest.quality.tbl_lots.scrapped, ZNGFinalTest.quality.tbl_lots.wps, USER_NAME(ZNGFinalTest.quality.tbl_lots.create_user_id) AS create_user, \
    ZNGFinalTest.quality.tbl_lots.create_date, USER_NAME(ZNGFinalTest.quality.tbl_lots.edit_user_id) AS edit_user, ZNGFinalTest.quality.tbl_lots.edit_date, ZNGFinalTest.quality.tbl_lots.fa \
    FROM            ( \
    SELECT ba, output \
    FROM ZNGFinalTest.catuno2.vw_manufacture \
    WHERE (workstep_name = 'BONDEN')) AS tbl1 \
    RIGHT OUTER JOIN ZNGFinalTest.quality.tbl_lots \
    INNER JOIN ZNGFinalTest.quality.tbl_states \
    ON ZNGFinalTest.quality.tbl_lots.state_id = ZNGFinalTest.quality.tbl_states.state_id \
    INNER JOIN ZNGFinalTest.quality.tbl_classes \
    ON ZNGFinalTest.quality.tbl_lots.class_id = ZNGFinalTest.quality.tbl_classes.class_id \
    LEFT OUTER JOIN ZNGFinalTest.quality.vw_last_comments \
    ON ZNGFinalTest.quality.tbl_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id ON tbl1.ba = quality.tbl_lots.ba \
    LEFT OUTER JOIN catuno.vw_wafers_list \
    ON ZNGFinalTest.quality.tbl_lots.lot = ZNGFinalTest.catuno.vw_wafers_list.lot \
    WHERE (ZNGFinalTest.quality.tbl_lots.visible = 1) AND (ZNGFinalTest.quality.tbl_lots.state_id = 2) \
    ) tbl2 \
    ), \
    tbl4 AS ( \
    SELECT ZNGProduction.catuno.tbl_wafers.lot, ZNGProduction.catuno.tbl_wafers.wafer_lot + ': <br>' + CAST(ZNGProduction.catuno.tbl_wafers.wafer_quantity as VARCHAR(100))  + '(' + ZNGProduction.catuno.tbl_wafers.probed + ')' + '<br>' AS wafer_info \
    FROM ZNGProduction.catuno.tbl_wafers \
    WHERE lot NOT LIKE '2%' AND lot NOT LIKE '3%' AND lot NOT LIKE '40%' AND lot NOT LIKE '41%' AND lot NOT LIKE '42%' AND lot NOT LIKE '43%' \
    ) \
    SELECT DISTINCT Typ, tbl3.Lot + ';' AS Lot, STRING_AGG(CAST(wafer_info AS NVARCHAR(MAX)), ', ') AS Waferinformation, affected, bonding_goods, Ausfallursache, create_date, create_user, Status, edit_date, edit_user \
    FROM tbl3 \
    JOIN tbl4 \
    ON tbl4.lot = tbl3.Lot \
    GROUP BY Typ, tbl3.Lot, affected, bonding_goods, Ausfallursache, create_date, create_user, Status, edit_date, edit_user \
    ORDER BY tbl3.create_date"
    df_azq = pd.read_sql(query, conn)

    last_edited = sorted(df_azq['edit_date'].astype('datetime64[s]').astype('str'))[-1]

    df_azq.insert(4, 'Betroffen', df_azq['affected'] + ' / ' + df_azq['bonding_goods'])
    df_azq.drop(['affected', 'bonding_goods'], axis=1, inplace =True)

    df_azq['create_date'] = df_azq['create_date'].astype('datetime64[s]')
    df_azq['create_date'] = df_azq['create_date'].astype('str')
    df_azq['edit_date'] = df_azq['edit_date'].astype('datetime64[s]')
    df_azq['edit_date'] = df_azq['edit_date'].astype('str')
    df_azq['create_user'] = df_azq['create_user'].str[1:]
    df_azq['create_user'] = df_azq['create_user'].str.title()
    df_azq['edit_user'] = df_azq['edit_user'].str[1:]
    df_azq['edit_user'] = df_azq['edit_user'].str.title()

    df_azq.insert(6, 'Startdatum', df_azq['create_date'] + '<br>' + df_azq['create_user'])
    df_azq.insert(9, 'Statusdatum', df_azq['edit_date'] + '<br>' + df_azq['edit_user'])
    df_azq.drop(['create_date', 'create_user','edit_date', 'edit_user'], axis=1, inplace =True)

    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")
    print("           DASHBOARD (AZQ)     ")
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df_azq.columns]) ] +
        # Body
        [html.Tr([
            html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''{}'''.format(df_azq.iloc[i][col]))) for col in df_azq.columns
        ]) for i in range(min(len(df_azq), max_rows))]
    ), 'zuletzt bearbeitet: {}'.format(last_edited)

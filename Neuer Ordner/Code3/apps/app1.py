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

    # df_azq.to_csv("problem_list.txt", index=False)
    df_azq = pd.read_csv("problem_list.txt")
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

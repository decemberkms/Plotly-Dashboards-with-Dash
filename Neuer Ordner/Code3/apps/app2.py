import numpy as np
import pandas as pd
# import pyodbc
import pymssql

import dash
import plotly.graph_objects as go
import plotly.offline as py

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from plotly.subplots import make_subplots
from datetime import datetime

from app import app

df_yield_app = pd.read_csv('initial_statistics.txt')
df_package = [i for i in df_yield_app['package'].unique()]

# query for plot
def package_list(df, package_):
    if len(package_) == 1:
        return (df['package'] == package_[0])
    elif len(package_) == 2:
        return (df['package'] == package_[0]) | (df['package'] == package_[1])
    elif len(package_) == 3:
        return (df['package'] == package_[0]) | (df['package'] == package_[1]) | (df['package'] == package_[2])
    elif len(package_) == 4:
        return (df['package'] == package_[0]) | (df['package'] == package_[1]) | (df['package'] == package_[2]) | (df['package'] == package_[3])
    elif len(package_) == 5:
        return (df['package'] == package_[0]) | (df['package'] == package_[1]) | (df['package'] == package_[2]) | (df['package'] == package_[3]) | (df['package'] == package_[4])
    elif len(package_) == 6:
        return (df['package'] == package_[0]) | (df['package'] == package_[1]) | (df['package'] == package_[2]) | (df['package'] == package_[3]) | (df['package'] == package_[4]) | (df['package'] == package_[5])
    elif len(package_) == 7:
        return (df['package'] == package_[0]) | (df['package'] == package_[1]) | (df['package'] == package_[2]) | (df['package'] == package_[3]) | (df['package'] == package_[4]) | (df['package'] == package_[5]) | (df['package'] == package_[6])

# query2 for plot
def de_gr_list(df, device_group_):
    if len(device_group_) == 1:
        return (df['device_group'] == device_group_[0])
    elif len(device_group_) == 2:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1])
    elif len(device_group_) == 3:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2])
    elif len(device_group_) == 4:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3])
    elif len(device_group_) == 5:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4])
    elif len(device_group_) == 6:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5])
    elif len(device_group_) == 7:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6])
    elif len(device_group_) == 8:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7])
    elif len(device_group_) == 9:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])
    elif len(device_group_) == 10:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9])
    elif len(device_group_) == 11:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10])
    elif len(device_group_) == 12:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11])
    elif len(device_group_) == 13:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12])
    elif len(device_group_) == 14:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13])
    elif len(device_group_) == 15:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14])
    elif len(device_group_) == 16:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[16])
    elif len(device_group_) == 17:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16])
    elif len(device_group_) == 18:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17])
    elif len(device_group_) == 19:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18])
    elif len(device_group_) == 20:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19])
    elif len(device_group_) == 21:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20])
    elif len(device_group_) == 22:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20]) | (df['device_group'] == device_group_[21])
    elif len(device_group_) == 23:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20]) | (df['device_group'] == device_group_[21]) | (df['device_group'] == device_group_[22])
    elif len(device_group_) == 24:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20]) | (df['device_group'] == device_group_[21]) | (df['device_group'] == device_group_[22]) | (df['device_group'] == device_group_[23])
    elif len(device_group_) == 25:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20]) | (df['device_group'] == device_group_[21]) | (df['device_group'] == device_group_[22]) | (df['device_group'] == device_group_[23]) | (df['device_group'] == device_group_[24])
    elif len(device_group_) == 26:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20]) | (df['device_group'] == device_group_[21]) | (df['device_group'] == device_group_[22]) | (df['device_group'] == device_group_[23]) | (df['device_group'] == device_group_[24]) | (df['device_group'] == device_group_[25])
    elif len(device_group_) == 27:
        return (df['device_group'] == device_group_[0]) | (df['device_group'] == device_group_[1]) | (df['device_group'] == device_group_[2]) | (df['device_group'] == device_group_[3]) | (df['device_group'] == device_group_[4]) | (df['device_group'] == device_group_[5]) | (df['device_group'] == device_group_[6]) | (df['device_group'] == device_group_[7]) | (df['device_group'] == device_group_[8])  | (df['device_group'] == device_group_[9]) | (df['device_group'] == device_group_[10]) | (df['device_group'] == device_group_[11]) | (df['device_group'] == device_group_[12]) | (df['device_group'] == device_group_[13]) | (df['device_group'] == device_group_[14]) | (df['device_group'] == device_group_[15]) | (df['device_group'] == device_group_[16]) | (df['device_group'] == device_group_[17]) | (df['device_group'] == device_group_[18]) | (df['device_group'] == device_group_[19]) | (df['device_group'] == device_group_[20]) | (df['device_group'] == device_group_[21]) | (df['device_group'] == device_group_[22]) | (df['device_group'] == device_group_[23]) | (df['device_group'] == device_group_[24]) | (df['device_group'] == device_group_[25]) | (df['device_group'] == device_group_[26])

# difference
def diff_call(n):
    if n == 2018.0:
        return 2019.0
    else:
        return n

# fill na
def na_filter(year__):
    if year__ == 2020:
        return 'bfill'
    else:
        return 'ffill'

# tickmode
def tick_mode(time_type):
    if time_type == 'month':
        return 'linear'
    else:
        return 'auto'

# app layout
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
                    html.Div(className="content-container", children=[
                    html.H1(id = 'header1', className= 'app_title', children='Finaltest Statistics',
                                        style= {'text-align': 'center', 'font-family': 'Overpass'}),
                    # html.H2(id='header2', children='Yield & output by package'),
                    html.Div([html.Label('Year'),
                            dcc.Dropdown(
                                id='year_',
                                options=[{'label': str(i).split('.')[0], 'value':i} for i in sorted(df_yield_app['year'].dropna().unique())],
                                value= datetime.today().year
                                )],
                                    style={'width':'20%',  'display': 'inline-block', 'float':'left', 'paddingLeft': '5%'}),
                    html.Div([html.Label('Package'),
                            dcc.Dropdown(
                                id='package_',
                                options=[{'label': i, 'value':i} for i in sorted(df_package)],
                                value= sorted(df_package),
                                multi=True)],
                                    style={'width':'50%', 'display': 'inline-block', 'float':'left'}),
                    html.Div([html.Label('Time period'),
                            dcc.Dropdown(
                                id='time_type',
                                options=[{'label': i.capitalize(), 'value':i} for i in ['week', 'month']],
                                value= 'week')],
                                    style={'width':'14%', 'display': 'inline-block', 'float':'left'}),
                    html.Div([html.Button(
                                id='yield-button',
                                n_clicks=0,
                                children='Click',
                                className='myButton')],
                                    style={'width': '10%', 'display': 'inline-block', 'float': 'left', 'paddingLeft': '1%', 'marginTop': '1.3%'}),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph1-update')],
                                    style = {'marginLeft': '1.5%', 'marginRight': '1.5%', 'marginTop':'25px', 'paddingBottom': '25px'}),
                            ],
                            style = {'width': '86%', 'marginLeft': '7%', 'marginRight': '7%', 'marginTop': '50px', 'paddingBottom': '1.5%'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph2-update')],
                                    style = {'width': '42.25%', 'marginLeft': '7%', 'marginTop': '1.5%', 'display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph3-update')],
                                    style = {'width': '42.25%', 'marginLeft': '1.5%', 'marginTop': '1.5%', 'display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph4-update')],
                                    style = {'width': '42.25%','marginLeft': '7%', 'marginTop': '1.5%', 'display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph5-update')],
                                    style = {'width': '42.25%', 'marginLeft': '1.5%', 'marginTop': '1.5%', 'display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph6-update')],
                                    style = {'width': '42.25%', 'marginLeft': '7%', 'marginTop': '1.5%', 'display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph7-update')],
                                    style = {'width': '42.25%', 'marginLeft': '1.5%', 'marginTop': '1.5%', 'display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph8-update')],
                                    style = {'width': '42.25%',  'marginLeft': '7%', 'marginTop': '1.5%', 'marginBottom': '50px','display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph9-update')],
                                    style = {'width': '42.25%',  'marginLeft': '1.5%', 'marginTop': '1.5%', 'marginBottom': '50px','display': 'inline-block', 'float':'left'})

                    ])

@app.callback(
            [Output('graph1-update', 'figure'),
            Output('graph2-update', 'figure'),
            Output('graph3-update', 'figure'),
            Output('graph4-update', 'figure'),
            Output('graph5-update', 'figure'),
            Output('graph6-update', 'figure'),
            Output('graph7-update', 'figure'),
            Output('graph8-update', 'figure'),
            Output('graph9-update', 'figure')],
            [Input('yield-button', 'n_clicks')],
            [State('package_', 'value'),
             State('time_type', 'value'),
             State('year_', 'value')])

def update_graph(n_clicks,package_, time_type, year__):
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                           user='WebServer',
                           password='W3bS3rv3r',
                           database='ZNGFinalTest')

    query = "SELECT lot AS a_lot, device, device_group, department, CASE WHEN package = 'ELineX' THEN package + ' ('+ ship_package + ')' ELSE package END as package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date \
    FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
    LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
    ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
    LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
    ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
    WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (package <> 'SEN') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') AND (final_test_yield > 0) \
    ORDER BY a_lot DESC"

    # starting data for beginning
    df_yield_app = pd.read_sql(query, conn)

    # fill before delivery lots << -- do not use: due to old lots
    # i = 0
    # while i < 200:
    #     if pd.isnull(df_yield_app['delivery_date'].iloc[i]):
    #         df_yield_app['delivery_date'].iloc[i] = datetime.today()
    #         i += 1
    #     else:
    #         i +=1

    df_yield_app['year'] =  df_yield_app['delivery_date'].dt.year
    df_yield_app['month'] = df_yield_app['delivery_date'].dt.month
    df_yield_app['week'] = df_yield_app['delivery_date'].dt.week
    df_yield_app['day'] = df_yield_app['delivery_date'].dt.day

    # df_yield_app.to_csv("initial_statistics.txt",index=False)

    # pd.DataFrame.from_dict({1:[1,2,3],2:[1,2,3],3:[1,2,3]}).to_csv("update_tester.txt")

    # color1 for bar
    m_w_diff = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].diff().values
    color1=np.array(['orange']*m_w_diff.shape[0])
    color1[m_w_diff<0]='red'
    color1[m_w_diff>=0]='blue'

    # color1_yield for bar
    m_w_diff_yield = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year__].diff().values
    color1_yield=np.array(['orange']*m_w_diff_yield.shape[0])
    color1_yield[m_w_diff_yield<0]='red'
    color1_yield[m_w_diff_yield>=0]='blue'

    # color2 for bar
    year_diff = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].values - df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[diff_call(year__) - 1].values
    color2=np.array(['orange']*year_diff.shape[0])
    color2[year_diff<0]='red'
    color2[year_diff>=0]='blue'

    # color2_yield for bar
    year_diff_yield = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year__].values - df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[diff_call(year__) - 1].values
    color2_yield=np.array(['orange']*year_diff_yield.shape[0])
    color2_yield[year_diff_yield<0]='red'
    color2_yield[year_diff_yield>=0]='blue'

    # color3 for bar
    cum_diff = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].cumsum().fillna(method='{}'.format(na_filter(year__))) - df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[diff_call(year__) - 1].cumsum().fillna(method='{}'.format(na_filter(year__)))
    color3=np.array(['orange']*cum_diff.shape[0])
    color3[cum_diff<0]='red'
    color3[cum_diff>=0]='blue'

    # color3_yield for bar
    cum_diff_yield = np.round((df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year__] * df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year__]).cumsum()/df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year__].cumsum(),4) - np.round((df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[diff_call(year__) - 1] * df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year__) - 1]).cumsum()/df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year__) - 1].cumsum(),4)
    color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
    color3_yield[cum_diff_yield<0]='red'
    color3_yield[cum_diff_yield>=0]='blue'

    fig1 = make_subplots(rows=1,
                        cols=2,
                        print_grid=True,
                        specs=[
                                [{"secondary_y": True, "colspan": 2}, None],
                                ]);

    trace0 = go.Bar(x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                    y = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].values,
                    name = 'Output',
                    opacity = 0.9,
                    hoverinfo = 'x+y+name',
                    width = 0.8,
                    #legendgroup ="group",
                    marker = dict(color='#0779e4'),
                    showlegend = True)

    trace1 = go.Scatter(x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                        y = 100*np.round(df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year__].values, 4),
                        name = 'Yield(%)',
                        opacity = 0.75,
                        hoverinfo = 'x+y+name',
                        marker = dict(line = dict(width = 1), size = 8),
                        line = dict(color = '#c70039', width = 1.5),
                        showlegend = True)

    fig1.add_trace(trace0, 1, 1, secondary_y = False)
    fig1.add_trace(trace1, 1, 1, secondary_y = True)

    fig1.layout.update(title = 'Yield & output in {}'.format(year__),
                      titlefont=dict(color= 'black', size=21, family = 'inherit'),
                      paper_bgcolor='white',
                      plot_bgcolor= '#d6e5fa',
                      autosize = False,
                      # width = 1500,
                      # height = 1300,
                      hovermode = 'x',
                      legend_orientation="v",
                      legend=dict(x=1.0, y=1.0))

    fig1.update_xaxes(autorange = True,
                     type = 'category',
                     tickfont=dict(color= 'black', size=16, family = 'inherit'));

    fig1.layout.yaxis.update(title = "Output",
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            # range = [15000000, 28000000],
                            showgrid =True)

    fig1.layout.yaxis2.update(title = "Yield (%)",
                             titlefont=dict(color= 'black', size=16, family = 'inherit'),
                             # range = [95,98],
                             showgrid=False)

    fig2 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                y = m_w_diff,
                                # y = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].diff().values,
                                name = 'Output diff.',
                                hoverinfo = 'x+y+name',
                                marker = dict(color=color1.tolist()),
                                showlegend=False
                                )],
                    layout = go.Layout(
                                title = '{}ly output difference in {}'.format(time_type.capitalize(), year__),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                    ))

    fig2.layout.yaxis.update(title = 'Output diff.',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True)


    fig3 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                y = 100*np.round(m_w_diff_yield,4),
                                name = 'Yield diff.',
                                hoverinfo = 'x+y+name',
                                marker = dict(color=color1_yield.tolist()),
                                showlegend=False
                                )],
                    layout = go.Layout(
                                title = '{}ly yield difference in {}'.format(time_type.capitalize(), year__),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))

    fig3.layout.yaxis.update(title = 'Yield diff. (%)',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True)


    fig4 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                y = year_diff,
                                name = '{} vs. {}'.format(year__, diff_call(year__)-1),
                                hoverinfo = 'x+y+name',
                                marker = dict(color=color2.tolist()),
                                showlegend=False
                                )],
                    layout = go.Layout(
                                title = 'Output comparison {} vs. {}'.format(year__, diff_call(year__)-1),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))

    fig4.layout.yaxis.update(title = 'Output diff.',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True)

    fig5 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                y = 100*np.round(year_diff_yield,4),
                                name = '{} vs. {}'.format(year__, diff_call(year__)-1),
                                hoverinfo = 'x+y+name',
                                marker = dict(color=color2_yield.tolist()),
                                showlegend=False
                                    )],
                    layout = go.Layout(
                                title ='Yield comparison {} vs. {}'.format(year__, diff_call(year__)-1),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))

    fig5.layout.yaxis.update(title = 'Yield diff. (%)',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True);

    fig6 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                y = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].cumsum().fillna(method='{}'.format(na_filter(year__))),
                                name = 'Cum.{}'.format(year__),
                                hoverinfo = 'x+y+name',
                                marker = dict(color='#0779e4'),
                                showlegend=False
                                    )],
                    layout = go.Layout(
                                title = 'Cumulative output in {}'.format(year__),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))

    fig6.layout.yaxis.update(title = 'Cum. output',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True);

    fig7 = go.Figure(
                    data = [go.Scatter(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                y = 100*np.round((df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year__] * df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year__]).cumsum()/df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year__].cumsum(),4),
                                name = 'Cum.{} yield'.format(year__),
                                hoverinfo = 'x+y+name',
                                marker = dict(color='#c70039'),
                                line = dict(color = '#c70039', width = 1.5),
                                showlegend=False
                                    )],
                    layout = go.Layout(
                                title = 'Cumulative yield in {}'.format(year__),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))

    fig7.layout.yaxis.update(title = 'Cum. yield (%)',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True);

    fig8 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                y = cum_diff,
                                name = '{} vs. {}'.format(year__, diff_call(year__)-1),
                                hoverinfo = 'x+y+name',
                                marker = dict(color=color3.tolist()),
                                showlegend=False
                                    )],
                    layout =go.Layout(
                                title = 'Cumulative output comparison {} vs. {}'.format(year__, diff_call(year__)-1),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))
    fig8.layout.yaxis.update(title = 'Cum. output diff.',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True)

    fig9 = go.Figure(
                    data = [go.Bar(
                                x = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                y = 100*cum_diff_yield,
                                name = '{} vs. {}'.format(year__, diff_call(year__)-1),
                                hoverinfo = 'x+y+name',
                                marker = dict(color=color3_yield.tolist()),
                                showlegend=False
                                    )],
                    layout = go.Layout(
                                title = 'Cumulative yield comparison {} vs. {}'.format(year__, diff_call(year__)-1),
                                titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                paper_bgcolor='white',
                                plot_bgcolor= '#d6e5fa',
                                autosize = False,
                                # width = 1500,
                                height = 380,
                                hovermode = 'x',
                                legend_orientation="h",
                                legend=dict(x=0.1, y=1.0)
                                      ))

    fig9.layout.yaxis.update(title = 'Cum. yield diff. (%)',
                            titlefont=dict(color= 'black', size=16, family = 'inherit'),
                            showgrid =True)

    fig2.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig3.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig4.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig5.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig6.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig7.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig8.layout.xaxis.update(tickmode=tick_mode(time_type))
    fig9.layout.xaxis.update(tickmode=tick_mode(time_type))

    return fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9

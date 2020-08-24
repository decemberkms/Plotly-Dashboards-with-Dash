import numpy as np
import pandas as pd
import pymssql

import dash
import plotly.graph_objects as go
import plotly.offline as py

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from plotly.subplots import make_subplots
from datetime import datetime

import dash_dangerously_set_inner_html

from app import app

# df_device_group = [i for i in df_yield_app['device_group'].unique()]

# quarter info
def get_quarter(date):
    return (date.month - 1) // 3 + 1

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

department_options = {
    'NAT': ['SOT223', 'SOT23', 'LFSOT23', 'SOT23F', 'ELineX (Schüttgut)', 'ELineX (STZ)', 'SM8'],
    'SEN': ['SEN']
    }

time_options = {
    'week': [2018, 2019, 2020],
    'month': [2018, 2019, 2020],
    'quarter': ['None'],
    'year': ['None']
    }

ratio_option = {
    'bar': ['None'],
    'non-bar-lot': ['SOT223', 'SOT23', 'LFSOT23', 'SOT23F', 'ELineX (Schüttgut)', 'ELineX (STZ)', 'SM8'],
    'non-bar-output': ['SOT223', 'SOT23', 'LFSOT23', 'SOT23F', 'ELineX (Schüttgut)', 'ELineX (STZ)', 'SM8'],
    'miscellaneous': ['Ausbeute', 'Output', 'Charge']
    }

# app layout
layout = html.Div(id = 'body-container', children =[
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
                    html.Div(className="content-container", children=[  # content-container start
                    html.H1(id = 'header1', className= 'app_title', children='Endmessungstatistik',
                                        style= {'text-align': 'center', 'font-family': 'Overpass'}),
                    html.Div(children=[html.Label('Produkttyp'),
                            dcc.RadioItems(id='department-select',
                                            options = [
                                                        {'label': 'NAT','value':'NAT'},
                                                        {'label': 'Nicht NAT','value':'SEN'}
                                                        ],
                                            labelStyle={'display': 'inline-block', 'paddingLeft': '15px'},
                                            value='NAT')],
                                    style={'width':'200px',  'display': 'inline-block', 'float':'left', 'paddingLeft': '30px'}),
                    html.Div([html.Label('Zeitraum'),
                            dcc.RadioItems(id='time-type',
                                            options=[{'label': 'Wöchentlich', 'value': 'week'},
                                                     {'label': 'Monatlich', 'value': 'month'},
                                                     {'label': 'Vierteljährlich', 'value': 'quarter'},
                                                     {'label': 'Jährlich', 'value': 'year'}],
                                            labelStyle={'display': 'inline-block', 'paddingLeft': '15px'},
                                            value= 'week')],
                                    style={'width':'450px',  'display': 'inline-block', 'float':'left', 'paddingLeft': '25px'}),
                    html.Div([html.Label('Jahr'),
                            dcc.Dropdown(
                                id='year-select',
                                options=[{'label': str(i).split('.')[0], 'value':i} for i in np.arange(2018, datetime.today().year + 1 , 1)],
                                value= datetime.today().year
                                )],
                                    style={'width':'150px',  'display': 'inline-block', 'float':'left', 'marginLeft': '500px'}),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph1-update')],
                                    style = {'marginLeft': '10px', 'marginRight': '10px', 'marginTop':'25px', 'paddingBottom': '25px'}),
                    html.Br(),
                    html.Div(children=[html.Label('Gehäuse'),
                            dcc.Dropdown(
                                id='package-select',
                                multi=True)],
                                    style={'paddingLeft': '15px', 'paddingRight': '15px', 'marginTop': '30px'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph2-update')],
                                    style = {'width': '950px', 'height':'490px', 'marginLeft': '10px', 'marginTop': '30px', 'marginBottom': '10px','display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            html.Div(id='table-title'),
                            html.Div(id='panel-1')],
                                    style = {'width': '330px', 'height':'490px', 'marginLeft': '25px', 'marginTop': '30px', 'marginBottom': '10px','display': 'inline-block', 'float':'left'}),
                    html.Br(),
                    html.Div(children=[html.Label('Diagramm Typ'),
                            dcc.RadioItems(
                                id='chart-select',
                                options=[
                                        {'label': 'Ausbeute/Outputvergleich', 'value': 'bar'},
                                        {'label': 'Verhältnis (Charge)', 'value': 'non-bar-lot'},
                                        {'label': 'Verhältnis (Output)', 'value': 'non-bar-output'},
                                        {'label': 'Verschiedenes', 'value': 'miscellaneous'}
                                        ],
                                value='non-bar-lot',
                                labelStyle={'display': 'inline-block', 'paddingLeft': '15px'})],
                                    style={'paddingLeft': '15px', 'display': 'inline-block', 'float':'left', 'marginTop': '30px'}),
                    html.Div([html.Label('Optionen'),
                            dcc.Dropdown(
                                id='device-select',
                                )],
                                    style={'width':'250px',  'display': 'inline-block', 'float':'left', 'marginLeft': '370px', 'marginTop': '30px'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph8-update')],
                                    style = {'width': '640px', 'height': '450px', 'marginLeft': '10px', 'marginTop': '15px', 'marginBottom': '50px','display': 'inline-block', 'float':'left'}),
                    html.Div(className="small-content-container", children=[
                            dcc.Graph(id='graph9-update')],
                                    style = {'width': '640px', 'height': '450px',  'marginLeft': '25px', 'marginTop': '15px', 'marginBottom': '50px','display': 'inline-block', 'float':'left'})
                                ], style = {'height': '1900px','width': '1325px', 'marginLeft': '15px', 'marginTop': '50px', 'marginBottom': '35px', 'paddingBottom': '35px'}) # content-container end
                    ]
                    )

@app.callback(
    Output('package-select', 'options'),
    [Input('department-select', 'value')])
def set_cities_options(selected_department):
    return [{'label': i, 'value': i} for i in department_options[selected_department]]

@app.callback(
    Output('package-select', 'value'),
    [Input('package-select', 'options')])
def set_cities_value(package_selection_chain):
    selection_list = [package_selection_chain[i]['value'] for i in range(len(package_selection_chain))]
    return selection_list

@app.callback(
    Output('year-select', 'options'),
    [Input('time-type', 'value')])
def set_cities_options(selected_time_type):
    return [{'label': i, 'value': i} for i in time_options[selected_time_type]]

@app.callback(
    Output('year-select', 'value'),
    [Input('year-select', 'options')])
def set_cities_value(year_selection):
    return year_selection[-1]['value']

@app.callback(
    Output('device-select', 'options'),
    [Input('chart-select', 'value')])
def set_cities_options(selected_ratio):
    return [{'label': i, 'value': i} for i in ratio_option[selected_ratio]]

@app.callback(
    Output('device-select', 'value'),
    [Input('device-select', 'options')])
def set_cities_value(device_selection):
    return device_selection[0]['value']

@app.callback(
            [Output('graph1-update', 'figure'),
             Output('graph2-update', 'figure'),
             Output('panel-1','children'),
             Output('table-title', 'children'),
             Output('graph8-update', 'figure'),
             Output('graph9-update', 'figure')],
            [Input('time-type', 'value'),
             Input('department-select', 'value'),
             Input('package-select', 'value'),
             Input('year-select', 'value'),
             Input('chart-select', 'value'),
             Input('device-select', 'value')])

def update_graph(time_type, dep_selected, package_selected, year_selected, chart_selected, device_selected):
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                           user='WebServer',
                           password='W3bS3rv3r',
                           database='ZNGFinalTest')

    if dep_selected == 'NAT':
        query = "SELECT lot AS a_lot, device, device_group, department, CASE WHEN package = 'ELineX' THEN package + ' ('+ ship_package + ')' ELSE package END as package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ship_package, die_size_code, transistor_type \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (package <> 'SEN') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') AND (final_test_yield >= 0) \
        ORDER BY a_lot DESC"
    elif dep_selected == 'SEN':
        query = "SELECT lot AS a_lot, device, device_group, department, CASE WHEN package = 'ELineX' THEN package + ' ('+ ship_package + ')' ELSE package END as package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date, ship_package, die_size_code, transistor_type \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package = 'SEN') AND (final_test_yield >= 0) \
        ORDER BY a_lot DESC"

    # starting data for beginning
    df_yield_app = pd.read_sql(query, conn)

    df_yield_app['year'] =  df_yield_app['delivery_date'].dt.year
    df_yield_app['month'] = df_yield_app['delivery_date'].dt.month
    df_yield_app['week'] = df_yield_app['delivery_date'].dt.week
    df_yield_app['day'] = df_yield_app['delivery_date'].dt.day
    df_yield_app['quarter'] = df_yield_app['delivery_date'].dt.quarter

    # total and each package yield & output
    if time_type == 'quarter':
        # total yield and output plot
        fig1 = make_subplots(rows=1,
                            cols=2,
                            print_grid=True,
                            specs=[
                                    [{"secondary_y": True, "colspan": 2}, None],
                                    ]);

        trace0 = go.Bar(x = df_yield_app.groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].sum().index.year.astype('str') + 'Q' + df_yield_app.groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].mean().index.quarter.astype('str'),
                        y = df_yield_app.groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].sum().values,
                        name = 'Output',
                        opacity = 0.9,
                        hoverinfo = 'x+y+name',
                        width = 0.8,
                        #legendgroup ="group",
                        marker = dict(color='#0779e4'),
                        showlegend = True)

        trace1 = go.Scatter(x = df_yield_app.groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_yield'].mean().index.year.astype('str') + 'Q' + df_yield_app.groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].mean().index.quarter.astype('str'),
                            y = 100*np.round(df_yield_app.groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_yield'].mean().values, 4),
                            name = 'Ausbeute (%)',
                            opacity = 0.75,
                            hoverinfo = 'x+y+name',
                            marker = dict(line = dict(width = 1), size = 8),
                            line = dict(color = '#c70039', width = 1.5),
                            showlegend = True)

        fig1.add_trace(trace0, 1, 1, secondary_y = False)
        fig1.add_trace(trace1, 1, 1, secondary_y = True)

        fig1.layout.update(title = 'Alle Gehäuse Ausbeute & Output',
                          titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                          paper_bgcolor='white',
                          plot_bgcolor= '#d6e5fa',
                          autosize = False,
                          width = 1300,
                          # height = 1300,
                          hovermode = 'x',
                          legend_orientation="h",
                          legend=dict(x=0.7, y=1.2))

        fig1.update_xaxes(autorange = True,
                         type = 'category',
                         tickfont=dict(color= 'black', size=16, family = 'Overpass'));

        fig1.layout.yaxis.update(title = "Output",
                                titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                # range = [15000000, 28000000],
                                showgrid =True)

        fig1.layout.yaxis2.update(title = "Ausbeute (%)",
                                 titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                 # range = [95,98],
                                 showgrid=False)

        # each package's yield and output
        fig2 = make_subplots(rows=1,
                            cols=2,
                            print_grid=True,
                            specs=[
                                    [{"secondary_y": True, "colspan": 2}, None],
                                    ]);

        trace2 = go.Bar(x = df_yield_app[package_list(df_yield_app, package_selected)].groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].sum().index.year.astype('str') + 'Q '+ df_yield_app[package_list(df_yield_app, package_selected)].groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].sum().index.quarter.astype('str'),
                        y = df_yield_app[package_list(df_yield_app, package_selected)].groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].sum().values,
                        name = 'Output',
                        opacity = 0.9,
                        hoverinfo = 'x+y+name',
                        width = 0.8,
                        #legendgroup ="group",
                        marker = dict(color='#0779e4'),
                        showlegend = True)

        trace3 = go.Scatter(x = df_yield_app[package_list(df_yield_app, package_selected)].groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_yield'].mean().index.year.astype('str') + 'Q '+ df_yield_app[package_list(df_yield_app, package_selected)].groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_output'].sum().index.quarter.astype('str'),
                            y = 100*np.round(df_yield_app[package_list(df_yield_app, package_selected)].groupby(df_yield_app['delivery_date'].dt.to_period('Q'))['final_test_yield'].mean().values, 4),
                            name = 'Ausbeute(%)',
                            opacity = 0.75,
                            hoverinfo = 'x+y+name',
                            marker = dict(line = dict(width = 1), size = 8),
                            line = dict(color = '#c70039', width = 1.5),
                            showlegend = True)

        fig2.add_trace(trace2, 1, 1, secondary_y = False)
        fig2.add_trace(trace3, 1, 1, secondary_y = True)

        fig2.layout.update(title = 'Ausbeute & Output (ausgewählt Gehäuse)',
                          titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                          paper_bgcolor='white',
                          plot_bgcolor= '#d6e5fa',
                          autosize = False,
                          width = 900,
                          height = 470,
                          hovermode = 'x',
                          legend_orientation="h",
                          legend=dict(x=0.7, y=1.2))

        fig2.update_xaxes(autorange = True,
                         type = 'category',
                         tickfont=dict(color= 'black', size=13, family = 'Overpass'));

        fig2.layout.yaxis.update(title = "Output",
                                titlefont=dict(color= 'black', size=13, family = 'Overpass'),
                                # range = [15000000, 28000000],
                                showgrid =True)

        fig2.layout.yaxis2.update(title = "Ausbeute (%)",
                                 titlefont=dict(color= 'black', size=13, family = 'Overpass'),
                                 # range = [95,98],
                                 showgrid=False)
    elif time_type == 'year':
        # total yield and output plot
        fig1 = make_subplots(rows=1,
                            cols=2,
                            print_grid=True,
                            specs=[
                                    [{"secondary_y": True, "colspan": 2}, None],
                                    ]);

        trace0 = go.Bar(x = df_yield_app.groupby('year')['final_test_output'].sum().index,
                        y = df_yield_app.groupby('year')['final_test_output'].sum().values,
                        name = 'Output',
                        opacity = 0.9,
                        hoverinfo = 'x+y+name',
                        width = 0.8,
                        #legendgroup ="group",
                        marker = dict(color='#0779e4'),
                        showlegend = True)

        trace1 = go.Scatter(x = df_yield_app.groupby('year')['final_test_yield'].mean().index,
                            y = 100*np.round(df_yield_app.groupby('year')['final_test_yield'].mean().values, 4),
                            name = 'Ausbeute (%)',
                            opacity = 0.75,
                            hoverinfo = 'x+y+name',
                            marker = dict(line = dict(width = 1), size = 8),
                            line = dict(color = '#c70039', width = 1.5),
                            showlegend = True)

        fig1.add_trace(trace0, 1, 1, secondary_y = False)
        fig1.add_trace(trace1, 1, 1, secondary_y = True)

        fig1.layout.update(title = 'Alle Gehäuse Ausbeute & Output',
                          titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                          paper_bgcolor='white',
                          plot_bgcolor= '#d6e5fa',
                          autosize = False,
                          width = 1300,
                          # height = 1300,
                          hovermode = 'x',
                          legend_orientation="h",
                          legend=dict(x=0.7, y=1.2))

        fig1.update_xaxes(autorange = True,
                         type = 'category',
                         tickfont=dict(color= 'black', size=16, family = 'Overpass'));

        fig1.layout.yaxis.update(title = "Output",
                                titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                # range = [15000000, 28000000],
                                showgrid =True)

        fig1.layout.yaxis2.update(title = "Ausbeute (%)",
                                 titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                 # range = [95,98],
                                 showgrid=False)

        # each package's yield and output
        fig2 = make_subplots(rows=1,
                            cols=2,
                            print_grid=True,
                            specs=[
                                    [{"secondary_y": True, "colspan": 2}, None],
                                    ]);

        trace2 = go.Bar(x = df_yield_app[package_list(df_yield_app, package_selected)].groupby('year')['final_test_output'].sum().index,
                        y = df_yield_app[package_list(df_yield_app, package_selected)].groupby('year')['final_test_output'].sum().values,
                        name = 'Output',
                        opacity = 0.9,
                        hoverinfo = 'x+y+name',
                        width = 0.8,
                        #legendgroup ="group",
                        marker = dict(color='#0779e4'),
                        showlegend = True)

        trace3 = go.Scatter(x = df_yield_app[package_list(df_yield_app, package_selected)].groupby('year')['final_test_yield'].mean().index,
                            y = 100*np.round(df_yield_app[package_list(df_yield_app, package_selected)].groupby('year')['final_test_yield'].mean().values, 4),
                            name = 'Ausbeute(%)',
                            opacity = 0.75,
                            hoverinfo = 'x+y+name',
                            marker = dict(line = dict(width = 1), size = 8),
                            line = dict(color = '#c70039', width = 1.5),
                            showlegend = True)

        fig2.add_trace(trace2, 1, 1, secondary_y = False)
        fig2.add_trace(trace3, 1, 1, secondary_y = True)

        fig2.layout.update(title = 'Ausbeute & Output (ausgewählt Gehäuse)',
                          titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                          paper_bgcolor='white',
                          plot_bgcolor= '#d6e5fa',
                          autosize = False,
                          width = 900,
                          height = 470,
                          hovermode = 'x',
                          legend_orientation="h",
                          legend=dict(x=0.7, y=1.2))

        fig2.update_xaxes(autorange = True,
                         type = 'category',
                         tickfont=dict(color= 'black', size=13, family = 'Overpass'));

        fig2.layout.yaxis.update(title = "Output",
                                titlefont=dict(color= 'black', size=13, family = 'Overpass'),
                                # range = [15000000, 28000000],
                                showgrid =True)

        fig2.layout.yaxis2.update(title = "Ausbeute (%)",
                                 titlefont=dict(color= 'black', size=13, family = 'Overpass'),
                                 # range = [95,98],
                                 showgrid=False)
    else:
        # total yield and output plot
        fig1 = make_subplots(rows=1,
                            cols=2,
                            print_grid=True,
                            specs=[
                                    [{"secondary_y": True, "colspan": 2}, None],
                                    ]);

        trace0 = go.Bar(x = df_yield_app.pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                        y = df_yield_app.pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year_selected].values,
                        name = 'Output',
                        opacity = 0.9,
                        hoverinfo = 'x+y+name',
                        width = 0.8,
                        #legendgroup ="group",
                        marker = dict(color='#0779e4'),
                        showlegend = True)

        trace1 = go.Scatter(x = df_yield_app.pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                            y = 100*np.round(df_yield_app.pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year_selected].values, 4),
                            name = 'Ausbeute(%)',
                            opacity = 0.75,
                            hoverinfo = 'x+y+name',
                            marker = dict(line = dict(width = 1), size = 8),
                            line = dict(color = '#c70039', width = 1.5),
                            showlegend = True)

        fig1.add_trace(trace0, 1, 1, secondary_y = False)
        fig1.add_trace(trace1, 1, 1, secondary_y = True)

        fig1.layout.update(title = 'Alle Gehäuse Ausbeute & Output {}'.format(year_selected),
                          titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                          paper_bgcolor='white',
                          plot_bgcolor= '#d6e5fa',
                          autosize = False,
                          width = 1300,
                          # height = 1300,
                          hovermode = 'x',
                          legend_orientation="h",
                          legend=dict(x=0.7, y=1.2))

        fig1.update_xaxes(autorange = True,
                         type = 'category',
                         tickfont=dict(color= 'black', size=16, family = 'Overpass'));

        fig1.layout.yaxis.update(title = "Output",
                                titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                # range = [15000000, 28000000],
                                showgrid =True)

        fig1.layout.yaxis2.update(title = "Ausbeute (%)",
                                 titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                 # range = [95,98],
                                 showgrid=False)

        # each package's yield and output
        fig2 = make_subplots(rows=1,
                            cols=2,
                            print_grid=True,
                            specs=[
                                    [{"secondary_y": True, "colspan": 2}, None],
                                    ]);

        trace2 = go.Bar(x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                        y = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year_selected].values,
                        name = 'Output',
                        opacity = 0.9,
                        hoverinfo = 'x+y+name',
                        width = 0.8,
                        #legendgroup ="group",
                        marker = dict(color='#0779e4'),
                        showlegend = True)

        trace3 = go.Scatter(x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                            y = 100*np.round(df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year_selected].values, 4),
                            name = 'Ausbeute (%)',
                            opacity = 0.75,
                            hoverinfo = 'x+y+name',
                            marker = dict(line = dict(width = 1), size = 8),
                            line = dict(color = '#c70039', width = 1.5),
                            showlegend = True)

        fig2.add_trace(trace2, 1, 1, secondary_y = False)
        fig2.add_trace(trace3, 1, 1, secondary_y = True)

        fig2.layout.update(title = 'Ausbeute & Output {} (ausgewählt Gehäuse)'.format(year_selected),
                          titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                          paper_bgcolor='white',
                          plot_bgcolor= '#d6e5fa',
                          autosize = False,
                          width = 900,
                          height = 470,
                          hovermode = 'x',
                          legend_orientation="h",
                          legend=dict(x=0.7, y=1.2))

        fig2.update_xaxes(autorange = True,
                         type = 'category',
                         tickfont=dict(color= 'black', size=13, family = 'Overpass'));

        fig2.layout.yaxis.update(title = "Output",
                                titlefont=dict(color= 'black', size=13, family = 'Overpass'),
                                # range = [15000000, 28000000],
                                showgrid =True)

        fig2.layout.yaxis2.update(title = "Ausbeute (%)",
                                 titlefont=dict(color= 'black', size=13, family = 'Overpass'),
                                 # range = [95,98],
                                 showgrid=False)

    # bar and pie plot
    if dep_selected == 'NAT':
        if chart_selected == 'bar':
            # comparison of yield & output
            if time_type == 'quarter':
                year_selected = datetime.today().year
                # color3 for bar
                cum_diff = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year_selected].cumsum().fillna(method='{}'.format(na_filter(year_selected))) - df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[diff_call(year_selected) - 1].cumsum().fillna(method='{}'.format(na_filter(year_selected)))
                color3=np.array(['orange']*cum_diff.shape[0])
                color3[cum_diff<0]='red'
                color3[cum_diff>=0]='blue'

                # color3_yield for bar
                cum_diff_yield = np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year_selected] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected].cumsum(),4) - np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[diff_call(year_selected) - 1] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1].cumsum(),4)
                color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
                color3_yield[cum_diff_yield<0]='red'
                color3_yield[cum_diff_yield>=0]='blue'

                fig8 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                            y = cum_diff,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3.tolist()),
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Kumulative Outputdifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig8.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig8.layout.yaxis.update(title = 'Outputdifferenz',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)

                fig9 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                            y = 100*cum_diff_yield,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3_yield.tolist()),
                                            showlegend=False
                                                )],
                                layout = go.Layout(
                                            title = 'Kumulative Ausbeutedifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig9.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig9.layout.yaxis.update(title = 'Ausbeutedifferenz (%)',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)
            elif time_type == 'year':
                year_selected = datetime.today().year
                # color3 for bar
                cum_diff = df_yield_app[package_list(df_yield_app, package_selected)].groupby('year')['final_test_output'].sum().diff()
                color3=np.array(['orange']*cum_diff.shape[0])
                color3[cum_diff<0]='red'
                color3[cum_diff>=0]='blue'

                # color3_yield for bar
                cum_diff_yield  = 100*round(df_yield_app.groupby('year')['final_test_yield'].mean().diff(),4)
                color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
                color3_yield[cum_diff_yield<0]='red'
                color3_yield[cum_diff_yield>=0]='blue'

                fig8 = go.Figure(
                                data = [go.Bar(
                                            x = cum_diff.index,
                                            y = cum_diff.values,
                                            name = 'Jährliche Differenz',
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3.tolist()),
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Kumulative Outputdifferenz',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig8.layout.xaxis.update(tickmode='linear')
                fig8.layout.yaxis.update(title = 'Outputdifferenz',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)

                fig9 = go.Figure(
                                data = [go.Bar(
                                            x = cum_diff_yield.index,
                                            y = cum_diff_yield.values,
                                            name = 'Jährliche Differenz',
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3_yield.tolist()),
                                            showlegend=False
                                                )],
                                layout = go.Layout(
                                            title = 'Kumulative Ausbeutedifferenz',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig9.layout.xaxis.update(tickmode='linear')
                fig9.layout.yaxis.update(title = 'Ausbeutedifferenz (%)',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)
            else:
                # color3 for bar
                cum_diff = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year_selected].cumsum().fillna(method='{}'.format(na_filter(year_selected))) - df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[diff_call(year_selected) - 1].cumsum().fillna(method='{}'.format(na_filter(year_selected)))
                color3=np.array(['orange']*cum_diff.shape[0])
                color3[cum_diff<0]='red'
                color3[cum_diff>=0]='blue'

                # color3_yield for bar
                cum_diff_yield = np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year_selected] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected].cumsum(),4) - np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[diff_call(year_selected) - 1] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1].cumsum(),4)
                color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
                color3_yield[cum_diff_yield<0]='red'
                color3_yield[cum_diff_yield>=0]='blue'

                fig8 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                            y = cum_diff,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3.tolist()),
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Kumulative Outputdifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig8.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig8.layout.yaxis.update(title = 'Outputdifferenz',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)

                fig9 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                            y = 100*cum_diff_yield,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3_yield.tolist()),
                                            showlegend=False
                                                )],
                                layout = go.Layout(
                                            title = 'Kumulative Ausbeutedifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig9.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig9.layout.yaxis.update(title = 'Ausbeutedifferenz (%)',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)
        elif chart_selected == 'non-bar-lot':
            ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
            if time_type == 'quarter':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['a_lot'].count().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Quartal)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today())) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today())) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Quartal): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'year':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['a_lot'].count().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Jahr)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Jahr): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'month':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['a_lot'].count().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieser Monat)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gruppe (dieser Monat): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'week':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['a_lot'].count().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gehäuse (diese Woche)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1]) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1]) & (ratio_chart['package'] == device_selected)].groupby('device_group')['a_lot'].count().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (diese Woche): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
        elif chart_selected == 'non-bar-output':
            ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
            if time_type == 'quarter':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['final_test_output'].sum().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Quartal)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today())) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today())) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Quartal): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'year':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['final_test_output'].sum().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Jahr)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Jahr): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'month':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['final_test_output'].sum().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieser Monat)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gruppe (dieser Monat): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'week':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['final_test_output'].sum().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gehäuse (diese Woche)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1]) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1]) & (ratio_chart['package'] == device_selected)].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (diese Woche): {}'.format(device_selected),
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
        elif chart_selected == 'miscellaneous':
            if device_selected == 'Charge':
                ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
                if time_type == 'quarter':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'year':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'month':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'week':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
            elif device_selected == 'Output':
                ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
                if time_type == 'quarter':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'year':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt(dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'month':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'week':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
            elif device_selected == 'Ausbeute':
                ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
                if time_type == 'quarter':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'year':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'month':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'week':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
    elif dep_selected == 'SEN':
        if chart_selected == 'bar':
            # comparison of yield & output
            if time_type == 'quarter':
                year_selected = datetime.today().year
                # color3 for bar
                cum_diff = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year_selected].cumsum().fillna(method='{}'.format(na_filter(year_selected))) - df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[diff_call(year_selected) - 1].cumsum().fillna(method='{}'.format(na_filter(year_selected)))
                color3=np.array(['orange']*cum_diff.shape[0])
                color3[cum_diff<0]='red'
                color3[cum_diff>=0]='blue'

                # color3_yield for bar
                cum_diff_yield = np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year_selected] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected].cumsum(),4) - np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[diff_call(year_selected) - 1] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1].cumsum(),4)
                color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
                color3_yield[cum_diff_yield<0]='red'
                color3_yield[cum_diff_yield>=0]='blue'

                fig8 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                            y = cum_diff,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3.tolist()),
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Kumulative Outputdifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig8.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig8.layout.yaxis.update(title = 'Outputdifferenz',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)

                fig9 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                            y = 100*cum_diff_yield,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3_yield.tolist()),
                                            showlegend=False
                                                )],
                                layout = go.Layout(
                                            title = 'Kumulative Ausbeutedifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig9.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig9.layout.yaxis.update(title = 'Ausbeutedifferenz (%)',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)
            elif time_type == 'year':
                year_selected = datetime.today().year
                # color3 for bar
                cum_diff = df_yield_app[package_list(df_yield_app, package_selected)].groupby('year')['final_test_output'].sum().diff()
                color3=np.array(['orange']*cum_diff.shape[0])
                color3[cum_diff<0]='red'
                color3[cum_diff>=0]='blue'

                # color3_yield for bar
                cum_diff_yield  = 100*round(df_yield_app.groupby('year')['final_test_yield'].mean().diff(),4)
                color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
                color3_yield[cum_diff_yield<0]='red'
                color3_yield[cum_diff_yield>=0]='blue'

                fig8 = go.Figure(
                                data = [go.Bar(
                                            x = cum_diff.index,
                                            y = cum_diff.values,
                                            name = 'Jährliche Differenz',
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3.tolist()),
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Kumulative Outputdifferenz',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig8.layout.xaxis.update(tickmode='linear')
                fig8.layout.yaxis.update(title = 'Outputdifferenz',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)

                fig9 = go.Figure(
                                data = [go.Bar(
                                            x = cum_diff_yield.index,
                                            y = cum_diff_yield.values,
                                            name = 'Jährliche Differenz',
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3_yield.tolist()),
                                            showlegend=False
                                                )],
                                layout = go.Layout(
                                            title = 'Kumulative Ausbeutedifferenz',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig9.layout.xaxis.update(tickmode='linear')
                fig9.layout.yaxis.update(title = 'Ausbeutedifferenz (%)',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)
            else:
                # color3 for bar
                cum_diff = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year_selected].cumsum().fillna(method='{}'.format(na_filter(year_selected))) - df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[diff_call(year_selected) - 1].cumsum().fillna(method='{}'.format(na_filter(year_selected)))
                color3=np.array(['orange']*cum_diff.shape[0])
                color3[cum_diff<0]='red'
                color3[cum_diff>=0]='blue'

                # color3_yield for bar
                cum_diff_yield = np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[year_selected] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[year_selected].cumsum(),4) - np.round((df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean)[diff_call(year_selected) - 1] * df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1]).cumsum()/df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = 'count')[diff_call(year_selected) - 1].cumsum(),4)
                color3_yield=np.array(['orange']*cum_diff_yield.shape[0])
                color3_yield[cum_diff_yield<0]='red'
                color3_yield[cum_diff_yield>=0]='blue'

                fig8 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum).index,
                                            y = cum_diff,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3.tolist()),
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Kumulative Outputdifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig8.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig8.layout.yaxis.update(title = 'Outputdifferenz',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)

                fig9 = go.Figure(
                                data = [go.Bar(
                                            x = df_yield_app[package_list(df_yield_app, package_selected)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_yield',  aggfunc = np.mean).index,
                                            y = 100*cum_diff_yield,
                                            name = '{} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            hoverinfo = 'x+y+name',
                                            marker = dict(color=color3_yield.tolist()),
                                            showlegend=False
                                                )],
                                layout = go.Layout(
                                            title = 'Kumulative Ausbeutedifferenz {} vs. {}'.format(year_selected, diff_call(year_selected)-1),
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            autosize = False,
                                            # width = 1500,
                                            height = 440,
                                            hovermode = 'x',
                                            legend_orientation="h",
                                            legend=dict(x=0.1, y=1.0)
                                                  ))
                fig9.layout.xaxis.update(tickmode=tick_mode(time_type))
                fig9.layout.yaxis.update(title = 'Ausbeutedifferenz (%)',
                                        titlefont=dict(color= 'black', size=16, family = 'Overpass'),
                                        showgrid =True)
        elif chart_selected == 'non-bar-lot':
            ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
            if time_type == 'quarter':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['a_lot'].count().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Quartal)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device_group')['a_lot'].count().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Quartal)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'year':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['a_lot'].count().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Jahr)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device_group')['a_lot'].count().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Jahr)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'month':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['a_lot'].count().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieser Monat)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device_group')['a_lot'].count().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gruppe (dieser Monat)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'week':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['a_lot'].count().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gehäuse (diese Woche)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device_group')['a_lot'].count().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device_group')['a_lot'].count().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (diese Woche)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
        elif chart_selected == 'non-bar-output':
            ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
            if time_type == 'quarter':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('package')['final_test_output'].sum().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Quartal)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Quartal)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'year':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('package')['final_test_output'].sum().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieses Jahr)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (dieses Jahr)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'month':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('package')['final_test_output'].sum().values,
                                        hole=.3
                                            )],
                            layout =go.Layout(
                                        title = 'Gehäuse (dieser Monat)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gruppe (dieser Monat)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
            elif time_type == 'week':
                fig8 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('package')['final_test_output'].sum().values,
                                        hole=.3)],
                            layout =go.Layout(
                                        title = 'Gehäuse (diese Woche)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
                fig9 = go.Figure(
                            data = [go.Pie(
                                        labels = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device_group')['final_test_output'].sum().index,
                                        values = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device_group')['final_test_output'].sum().values,
                                        hole=.3
                                        )],
                            layout =go.Layout(
                                        title = 'Gruppe (diese Woche)',
                                        titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                        paper_bgcolor='#d6e5fa',
                                        plot_bgcolor= '#d6e5fa',
                                        autosize = True,
                                        margin = dict(t=70, l=70, r=70, b=70)
                                        ))
        elif chart_selected == 'miscellaneous':
            if device_selected == 'Charge':
                ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
                if time_type == 'quarter':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'year':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'month':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'week':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die häufigste Charge nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['a_lot'].count().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die wenigstene Charge nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
            elif device_selected == 'Output':
                ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
                if time_type == 'quarter':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'year':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt(dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'month':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'week':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).head(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das größte Output nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).index,
                                            y = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_output'].sum().sort_values(ascending=False).tail(10).values,
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Das kleinste Output nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
            elif device_selected == 'Ausbeute':
                ratio_chart = df_yield_app[package_list(df_yield_app, package_selected)]
                if time_type == 'quarter':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['quarter'] == get_quarter(datetime.today()))].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (dieses Quartal)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'year':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (dieses Jahr)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'month':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['month'] == datetime.today().month)].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (dieser Monat)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                elif time_type == 'week':
                    fig8 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).head(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die beste Ausbeute nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))
                    fig9 = go.Figure(
                                data = [go.Bar(
                                            x = ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).index,
                                            y = list(map(lambda x: round(x,2), 100*ratio_chart[(ratio_chart['year'] == datetime.today().year) & (ratio_chart['week'] == datetime.today().isocalendar()[1])].groupby('device')['final_test_yield'].mean().sort_values(ascending=False).tail(10).values)),
                                            hoverinfo = 'x+y',
                                            showlegend=False
                                                )],
                                layout =go.Layout(
                                            title = 'Die schlechteste Ausbeute nach Produkt (diese Woche)',
                                            titlefont=dict(color= 'black', size=21, family = 'Overpass'),
                                            paper_bgcolor='white',
                                            plot_bgcolor= '#d6e5fa',
                                            # autosize = True,
                                            # margin = dict(t=70, l=70, r=70, b=70)
                                            ))

    # table creation
    if 1==1:
        # date calculation for table
        df_yield_app = df_yield_app[package_list(df_yield_app, package_selected)]
        ## week yield
        weekly_yield_last = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['week'] == datetime.today().isocalendar()[1] - 1)]['final_test_yield'].mean(),4)
        weekly_yield_current = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['week'] == datetime.today().isocalendar()[1])]['final_test_yield'].mean(),4)
        if weekly_yield_current > weekly_yield_last:
            weekly_yield_current = '<font color="green">' +  str(round(weekly_yield_current,2)) + '</font>' + '% (' + '<font color="green">' + str(round(weekly_yield_current - weekly_yield_last, 4)) + '%↑' + '</font>'+')'
            weekly_yield_last = str(round(weekly_yield_last,2)) + '%'
        elif weekly_yield_current < weekly_yield_last:
            weekly_yield_current = '<font color="red">' +  str(round(weekly_yield_current,2)) + '</font>' + '% (' + '<font color="red">' + str(round(weekly_yield_current - weekly_yield_last, 4)) + '%↓' + '</font>'+')'
            weekly_yield_last = str(round(weekly_yield_last,2)) + '%'
        else:
            weekly_yield_current = str(round(weekly_yield_current,2)) + '% (' + '<font color="black">' + str(round(weekly_yield_current - weekly_yield_last, 4)) + '-' + '</font>'+')'
            weekly_yield_last = str(round(weekly_yield_last,2)) + '%'

        ## month yield
        monthly_yield_last = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['month'] == datetime.today().month - 1)]['final_test_yield'].mean(),4)
        monthly_yield_current = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['month'] == datetime.today().month)]['final_test_yield'].mean(),4)
        if monthly_yield_current > monthly_yield_last:
            monthly_yield_current = '<font color="green">' +  str(round(monthly_yield_current,2)) + '</font>' + '% (' + '<font color="green">' + str(round(monthly_yield_current - monthly_yield_last, 4)) + '%↑' + '</font>'+')'
            monthly_yield_last = str(round(monthly_yield_last,2)) + '%'
        elif monthly_yield_current < monthly_yield_last:
            monthly_yield_current = '<font color="red">' +  str(round(monthly_yield_current,2)) + '</font>' + '% (' + '<font color="red">' + str(round(monthly_yield_current - monthly_yield_last, 4)) + '%↓' + '</font>'+')'
            monthly_yield_last = str(round(monthly_yield_last,2)) + '%'
        else:
            monthly_yield_current = str(round(monthly_yield_current,2)) + '% (' + '<font color="black">' + str(round(monthly_yield_current - monthly_yield_last, 4)) + '-' + '</font>'+')'
            monthly_yield_last = str(round(monthly_yield_last,2)) + '%'

        ## quarter yield
        quarterly_yield_last = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['quarter'] == get_quarter(datetime.today()) - 1)]['final_test_yield'].mean(),4)
        quarterly_yield_current = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['quarter'] == get_quarter(datetime.today()))]['final_test_yield'].mean(),4)
        if quarterly_yield_current > quarterly_yield_last:
            quarterly_yield_current = '<font color="green">' +  str(round(quarterly_yield_current,2)) + '</font>' + '% (' + '<font color="green">' + str(round(quarterly_yield_current - quarterly_yield_last, 4)) + '%↑' + '</font>'+')'
            quarterly_yield_last = str(round(quarterly_yield_last,2)) + '%'
        elif quarterly_yield_current < quarterly_yield_last:
            quarterly_yield_current = '<font color="red">' +  str(round(quarterly_yield_current,2)) + '</font>' + '% (' + '<font color="red">' + str(round(quarterly_yield_current - quarterly_yield_last, 4)) + '%↓' + '</font>'+')'
            quarterly_yield_last = str(round(quarterly_yield_last,2)) + '%'
        else:
            quarterly_yield_current = str(round(quarterly_yield_current,2)) + '% (' + '<font color="black">' + str(round(quarterly_yield_current - quarterly_yield_last, 4)) + '-' + '</font>'+')'
            quarterly_yield_last = str(round(quarterly_yield_last,2)) + '%'

        ## year yield
        cummulative_yield_last = 100*round(df_yield_app[(df_yield_app['year'] == (datetime.today().year - 1))]['final_test_yield'].mean(),4)
        cummulative_yield_current = 100*round(df_yield_app[(df_yield_app['year'] == datetime.today().year)]['final_test_yield'].mean(),4)
        if cummulative_yield_current > cummulative_yield_last:
            cummulative_yield_current = '<font color="green">' +  str(round(cummulative_yield_current,2)) + '</font>' + '% (' + '<font color="green">' + str(round(cummulative_yield_current - cummulative_yield_last, 4)) + '%↑' + '</font>'+')'
            cummulative_yield_last = str(round(cummulative_yield_last,2)) + '%'
        elif cummulative_yield_current < cummulative_yield_last:
            cummulative_yield_current = '<font color="red">' +  str(round(cummulative_yield_current,2)) + '</font>' + '% (' + '<font color="red">' + str(round(cummulative_yield_current - cummulative_yield_last, 4)) + '%↓' + '</font>'+')'
            cummulative_yield_last = str(round(cummulative_yield_last,2)) + '%'
        else:
            cummulative_yield_current = str(round(cummulative_yield_current,2)) + '% (' + '<font color="black">' + str(round(cummulative_yield_current - cummulative_yield_last, 4)) + '-' + '</font>'+')'
            cummulative_yield_last = str(round(cummulative_yield_last,2)) + '%'

        ## week output
        weekly_output_last =  df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['week'] == datetime.today().isocalendar()[1] - 1)]['final_test_output'].sum()/1000000
        weekly_output_current = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['week'] == datetime.today().isocalendar()[1])]['final_test_output'].sum()/1000000
        if weekly_output_current > weekly_output_last:
            weekly_output_current = '<font color="green">' +  str(round(weekly_output_current, 3)) + 'M</font>' + ' (' + '<font color="green">' + str(round(weekly_output_current - weekly_output_last, 3)) + 'M↑' + '</font>'+')'
            weekly_output_last = str(round(weekly_output_last, 3)) + 'M'
        elif weekly_output_current < weekly_output_last:
            weekly_output_current = '<font color="red">' +  str(round(weekly_output_current, 3)) + 'M</font>' + ' (' + '<font color="red">' + str(round(weekly_output_current - weekly_output_last, 3)) + 'M↓' + '</font>'+')'
            weekly_output_last = str(round(weekly_output_last, 3)) + 'M'
        else:
            weekly_output_current = str(round(weekly_output_current, 3)) + 'M (' + '<font color="black">' + str(round(weekly_output_current - weekly_output_last, 3)) + '-' + '</font>'+')'
            weekly_output_last = str(round(weekly_output_last, 3)) + 'M'

        ## month output
        monthly_output_last = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['month'] == datetime.today().month - 1)]['final_test_output'].sum()/1000000
        monthly_output_current = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['month'] == datetime.today().month)]['final_test_output'].sum()/1000000
        if monthly_output_current > monthly_output_last:
            monthly_output_current = '<font color="green">' + str(round(monthly_output_current, 3)) + 'M</font>' + ' (' + '<font color="green">' + str(round(monthly_output_current - monthly_output_last, 3)) + 'M↑' + '</font>'+')'
            monthly_output_last = str(round(monthly_output_last, 3)) + 'M'
        elif monthly_output_current < monthly_output_last:
            monthly_output_current = '<font color="red">' +  str(round(monthly_output_current, 3))+ 'M</font>' + ' (' + '<font color="red">' + str(round(monthly_output_current - monthly_output_last, 3)) + 'M↓' + '</font>'+')'
            monthly_output_last = str(round(monthly_output_last, 3)) + 'M'
        else:
            monthly_output_current = str(round(monthly_output_current, 3)) + 'M (' + '<font color="black">' + str(round(monthly_output_current - monthly_output_last, 3)) + '-' + '</font>'+')'
            monthly_output_last = str(round(monthly_output_last, 3)) + 'M'

        ## quarter output
        quarterly_output_last = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['quarter'] == get_quarter(datetime.today()) - 1)]['final_test_output'].sum()/1000000
        quarterly_output_current = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['quarter'] == get_quarter(datetime.today()))]['final_test_output'].sum()/1000000
        if quarterly_output_current > quarterly_output_last:
            quarterly_output_current = '<font color="green">' +  str(round(quarterly_output_current, 3))+ 'M</font>' + ' (' + '<font color="green">' + str(round(quarterly_output_current - quarterly_output_last, 3)) + 'M↑' + '</font>'+')'
            quarterly_output_last = str(round(quarterly_output_last, 3)) + 'M'
        elif quarterly_output_current < quarterly_output_last:
            quarterly_output_current = '<font color="red">' +  str(round(quarterly_output_current, 3)) + 'M</font>' + ' (' + '<font color="red">' + str(round(quarterly_output_current - quarterly_output_last, 3)) + 'M↓' + '</font>'+')'
            quarterly_output_last = str(round(quarterly_output_last, 3)) + 'M'
        else:
            quarterly_output_current = str(round(quarterly_output_current, 3)) + 'M (' + '<font color="black">' + str(round(quarterly_output_current - quarterly_output_last, 3)) + '-' + '</font>'+')'
            quarterly_output_last = str(round(quarterly_output_last, 3)) + 'M'

        ## year output
        cummulative_output_last = df_yield_app[(df_yield_app['year'] == (datetime.today().year - 1))]['final_test_output'].sum()/1000000
        cummulative_output_current = df_yield_app[(df_yield_app['year'] == datetime.today().year)]['final_test_output'].sum()/1000000
        if cummulative_output_current > cummulative_output_last:
            cummulative_output_current = '<font color="green">' +  str(round(cummulative_output_current, 3))+ 'M</font>' + ' (' + '<font color="green">' + str(round(cummulative_output_current - cummulative_output_last, 3)) + 'M↑' + '</font>'+')'
            cummulative_output_last = str(round(cummulative_output_last, 3)) + 'M'
        elif cummulative_output_current < cummulative_output_last:
            cummulative_output_current = '<font color="red">' +  str(round(cummulative_output_current, 3)) + 'M</font>' + ' (' + '<font color="red">' + str(round(cummulative_output_current - cummulative_output_last, 3)) + 'M↓' + '</font>'+')'
            cummulative_output_last = str(round(cummulative_output_last, 3)) + 'M'
        else:
            cummulative_output_current = str(round(cummulative_output_current, 3)) + 'M (' + '<font color="black">' + str(round(cummulative_output_current - cummulative_output_last, 3)) + '-' + '</font>'+')'
            cummulative_output_last = str(round(cummulative_output_last, 3)) + 'M'

        ## week lot
        weekly_lot_last = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['week'] == datetime.today().isocalendar()[1] - 1)]['a_lot'].count()
        weekly_lot_current = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['week'] == datetime.today().isocalendar()[1])]['a_lot'].count()
        if weekly_lot_current > weekly_lot_last:
            weekly_lot_current = '<font color="green">' +  str(weekly_lot_current) + '</font>' + ' (' + '<font color="green">' + str(weekly_lot_current - weekly_lot_last) + '↑' + '</font>'+')'
        elif weekly_lot_current < weekly_lot_last:
            weekly_lot_current = '<font color="red">' +  str(weekly_lot_current) + '</font>' + ' (' + '<font color="red">' + str(weekly_lot_current - weekly_lot_last) + '↓' + '</font>'+')'
        else:
            weekly_lot_current = str(weekly_lot_current) +  ' (' + '<font color="black">' + str(weekly_lot_current - weekly_lot_last) + '-' + '</font>'+')'

        # month output
        monthly_lot_last = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['month'] == datetime.today().month - 1)]['a_lot'].count()
        monthly_lot_current = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['month'] == datetime.today().month)]['a_lot'].count()
        if monthly_lot_current > monthly_lot_last:
            monthly_lot_current = '<font color="green">' + str(monthly_lot_current) + '</font>' + ' (' + '<font color="green">' + str(monthly_lot_current - monthly_lot_last) + '↑' + '</font>'+')'
        elif monthly_lot_current < monthly_lot_last:
            monthly_lot_current = '<font color="red">' +  str(monthly_lot_current)+ '</font>' + ' (' + '<font color="red">' + str(monthly_lot_current - monthly_lot_last) + '↓' + '</font>'+')'
        else:
            monthly_lot_current = str(monthly_lot_current) + ' (' + '<font color="black">' + str(monthly_lot_current - monthly_lot_last) + '-' + '</font>'+')'

        ## quarter output
        quarterly_lot_last = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['quarter'] == get_quarter(datetime.today()) - 1)]['a_lot'].count()
        quarterly_lot_current = df_yield_app[(df_yield_app['year'] == datetime.today().year) & (df_yield_app['quarter'] == get_quarter(datetime.today()))]['a_lot'].count()
        if quarterly_lot_current > quarterly_lot_last:
            quarterly_lot_current = '<font color="green">' +  str(quarterly_lot_current)+ '</font>' + ' (' + '<font color="green">' + str(quarterly_lot_current - quarterly_lot_last) + '↑' + '</font>'+')'
        elif quarterly_lot_current < quarterly_lot_last:
            quarterly_lot_current = '<font color="red">' +  str(quarterly_lot_current) + '</font>' + ' (' + '<font color="red">' + str(quarterly_lot_current - quarterly_lot_last) + '↓' + '</font>'+')'
        else:
            quarterly_lot_current = str(quarterly_lot_current) + ' (' + '<font color="black">' + str(quarterly_lot_current - quarterly_lot_last) + '-' + '</font>'+')'

        ## year output
        cummulative_lot_last = df_yield_app[(df_yield_app['year'] == (datetime.today().year - 1))]['a_lot'].count()
        cummulative_lot_current = df_yield_app[(df_yield_app['year'] == datetime.today().year)]['a_lot'].count()
        if cummulative_lot_current > cummulative_lot_last:
            cummulative_lot_current = '<font color="green">' +  str(cummulative_lot_current)+ '</font>' + ' (' + '<font color="green">' + str(cummulative_lot_current - cummulative_lot_last) + '↑' + '</font>'+')'
        elif cummulative_lot_current < cummulative_lot_last:
            cummulative_lot_current = '<font color="red">' +  str(cummulative_lot_current) + '</font>' + ' (' + '<font color="red">' + str(cummulative_lot_current - cummulative_lot_last) + '↓' + '</font>'+')'
        else:
            cummulative_lot_current = str(cummulative_lot_current) + ' (' + '<font color="black">' + str(cummulative_lot_current - cummulative_lot_last) + '-' + '</font>'+')'


        # table
        table_stats = html.Table(
            # Header 1
            [html.Tr([html.Th('Ausbeute'), html.Th('Bisherige'), html.Th('Aktuell')])] +
            # Body 1
            [html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Wöchentlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(weekly_yield_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(weekly_yield_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Monatlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(monthly_yield_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(monthly_yield_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Vierteljährlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(quarterly_yield_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(quarterly_yield_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Jährlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(cummulative_yield_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(cummulative_yield_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Total</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('-')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML( str(100*round(df_yield_app['final_test_yield'].mean(), 4)) + '%' ))
                    ]
                    )
            ] +
            # Header 2
            [html.Tr([html.Th('Output'), html.Th('Bisherige'), html.Th('Aktuell')])]  +
            # Body 2
            [html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Wöchentlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(weekly_output_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(weekly_output_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Monatlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(monthly_output_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(monthly_output_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Vierteljährlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(quarterly_output_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(quarterly_output_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Jährlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(cummulative_output_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(cummulative_output_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Total</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('-')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML( str(round(df_yield_app['final_test_output'].sum()/1000000, 3)) + 'M' ))
                    ]
                    )
            ] +
            # Header 3
            [html.Tr([html.Th('Lot'), html.Th('Bisherige'), html.Th('Aktuell')])]  +
            # Body 3
            [html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Wöchentlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(weekly_lot_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(weekly_lot_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Monatlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(monthly_lot_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(monthly_lot_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Vierteljährlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(quarterly_lot_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(quarterly_lot_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Jährlich</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(cummulative_lot_last)),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML(cummulative_lot_current))
                    ]
                    ),
            html.Tr(
                    [
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('<strong>Total</strong>')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML('-')),
                    html.Td(dash_dangerously_set_inner_html.DangerouslySetInnerHTML( df_yield_app['a_lot'].count() ))
                    ]
                    )
            ]
        )

    table_tile = "Ausgewählte Gehäuse dieses Jahres"

    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")
    print("           DASHBOARD (STATS)   ")
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")

    return fig1, fig2, table_stats, table_tile, fig8, fig9

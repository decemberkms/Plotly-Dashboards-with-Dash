import numpy as np
import pandas as pd
import pymssql

import dash
import plotly.graph_objects as go
import plotly.offline as py

import dash_core_components as dcc
from datetime import datetime as dt
import dash_html_components as html
import dash_dangerously_set_inner_html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from datetime import datetime
import dateutil.relativedelta
from plotly.subplots import make_subplots
import dash_table
# import json
import math
import re

from io import StringIO
from html.parser import HTMLParser

from app import app

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

df = pd.read_csv('initial_lot.txt')
df_package = [i for i in df['package'].unique()]
df['month'].fillna(1, inplace=True)

# for package
def package_filter(df, package_update):
    if len(package_update) == 1:
        return (df['package'] == package_update[0])
    elif len(package_update) == 2:
        return (df['package'] == package_update[0]) | (df['package'] == package_update[1])
    elif len(package_update) == 3:
        return (df['package'] == package_update[0]) | (df['package'] == package_update[1]) | (df['package'] == package_update[2])
    elif len(package_update) == 4:
        return (df['package'] == package_update[0]) | (df['package'] == package_update[1]) | (df['package'] == package_update[2]) | (df['package'] == package_update[3])
    elif len(package_update) == 5:
        return (df['package'] == package_update[0]) | (df['package'] == package_update[1]) | (df['package'] == package_update[2]) | (df['package'] == package_update[3]) | (df['package'] == package_update[4])
    elif len(package_update) == 6:
        return (df['package'] == package_update[0]) | (df['package'] == package_update[1]) | (df['package'] == package_update[2]) | (df['package'] == package_update[3]) | (df['package'] == package_update[4]) | (df['package'] == package_update[5])

# for wire
def wire_filter(df, wire_update):
    if len(wire_update) == 1:
        return (df['bond_wire'] == wire_update[0])
    elif len(wire_update) == 2:
        return (df['bond_wire'] == wire_update[0]) | (df['bond_wire'] == wire_update[1])
    elif len(wire_update) == 3:
        return (df['bond_wire'] == wire_update[0]) | (df['bond_wire'] == wire_update[1]) | (df['bond_wire'] == wire_update[2])

# for device group
def device_group_update(df, device_g_update):
        if len(device_g_update) == 1:
            return (df['device_group'] == device_g_update[0])
        elif len(device_g_update) == 2:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1])
        elif len(device_g_update) == 3:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2])
        elif len(device_g_update) == 4:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3])
        elif len(device_g_update) == 5:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4])
        elif len(device_g_update) == 6:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5])
        elif len(device_g_update) == 7:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6])
        elif len(device_g_update) == 8:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7])
        elif len(device_g_update) == 9:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8])
        elif len(device_g_update) == 10:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9])
        elif len(device_g_update) == 11:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10])
        elif len(device_g_update) == 12:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11])
        elif len(device_g_update) == 13:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12])
        elif len(device_g_update) == 14:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13])
        elif len(device_g_update) == 15:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14])
        elif len(device_g_update) == 16:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15])
        elif len(device_g_update) == 17:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16])
        elif len(device_g_update) == 18:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17])
        elif len(device_g_update) == 19:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18])
        elif len(device_g_update) == 20:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19])
        elif len(device_g_update) == 21:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19]) | (df['device_group'] == device_g_update[20])
        elif len(device_g_update) == 22:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19]) | (df['device_group'] == device_g_update[20]) | (df['device_group'] == device_g_update[21])
        elif len(device_g_update) == 23:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19]) | (df['device_group'] == device_g_update[20]) | (df['device_group'] == device_g_update[21]) | (df['device_group'] == device_g_update[22])
        elif len(device_g_update) == 24:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19]) | (df['device_group'] == device_g_update[20]) | (df['device_group'] == device_g_update[21]) | (df['device_group'] == device_g_update[22]) | (df['device_group'] == device_g_update[23])
        elif len(device_g_update) == 25:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19]) | (df['device_group'] == device_g_update[20]) | (df['device_group'] == device_g_update[21]) | (df['device_group'] == device_g_update[22]) | (df['device_group'] == device_g_update[23]) | (df['device_group'] == device_g_update[24])
        elif len(device_g_update) == 26:
            return (df['device_group'] == device_g_update[0]) | (df['device_group'] == device_g_update[1]) | (df['device_group'] == device_g_update[2]) | (df['device_group'] == device_g_update[3]) | (df['device_group'] == device_g_update[4]) | (df['device_group'] == device_g_update[5]) | (df['device_group'] == device_g_update[6]) | (df['device_group'] == device_g_update[7]) | (df['device_group'] == device_g_update[8]) | (df['device_group'] == device_g_update[9]) | (df['device_group'] == device_g_update[10]) | (df['device_group'] == device_g_update[11]) | (df['device_group'] == device_g_update[12]) | (df['device_group'] == device_g_update[13]) | (df['device_group'] == device_g_update[14]) | (df['device_group'] == device_g_update[15]) | (df['device_group'] == device_g_update[16]) | (df['device_group'] == device_g_update[17]) | (df['device_group'] == device_g_update[18]) | (df['device_group'] == device_g_update[19]) | (df['device_group'] == device_g_update[20]) | (df['device_group'] == device_g_update[21]) | (df['device_group'] == device_g_update[22]) | (df['device_group'] == device_g_update[23]) | (df['device_group'] == device_g_update[24]) | (df['device_group'] == device_g_update[25])

# for color scale
def color_scale(df):
    if df['rejected'] < 5000:
        return 0
    elif 5000 <= df['rejected'] < 10000:
        return 0.3
    elif 10000 <= df['rejected'] < 9999999998:
        return 0.6
    else:
        return 1

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
                    html.Div(className="content-container", children=[
                    html.H1(className= 'app_title', children='Endmessunginformation'),
                    html.Br(),
                    # html.P(className='para1',children="Please select the options below and click on the <Click> button."),
                    html.Div(children=[
                    dcc.RadioItems(id='whatdata',
                                    options=[
                                        {'label': 'Verkürzte Info.', 'value': 'short'},
                                        {'label': 'Waferinfo. mit Details', 'value': 'wafer'},
                                        {'label': 'Kommentar', 'value': 'comment'},
                                        {'label': 'Lagerinfo.', 'value': 'storage'},
                                        {'label': ' Charge ohne FT data', 'value': 'bevfore_ft'}],  # lots without FT data and without SEN -> Q info is not only for SMD but also SEN
                                    value='short',
                                    labelStyle={'display': 'inline-block', 'marginRight': '2%'}
                                        )],
                                            style = {'paddingLeft': '5%'}),
                    html.Div([html.Label('Datum'),
                            dcc.DatePickerRange(
                                id='date-picker-range',
                                month_format='MMMM-D-Y',
                                end_date_placeholder_text='MMMM-D-Y',
                                start_date=datetime.today() + dateutil.relativedelta.relativedelta(months=-1),
                                end_date=datetime.today()
                                )],
                                    style={'width':'22%', 'display': 'inline-block', 'float':'left', 'marginLeft': '5%'}),
                    html.Div([html.Label('Gehäuse'),
                            dcc.Dropdown(
                                id='package-update',
                                options=[{'label': i, 'value':i} for i in ['ELineX', 'SOT223', 'SOT23', 'SOT23F', 'SM8', 'LFSOT23']],
                                value=sorted( ['ELineX', 'SOT223', 'SOT23', 'SOT23F', 'SM8', 'LFSOT23']),
                                multi=True)],
                                    style={'width':'42%', 'display': 'inline-block', 'float':'left'}),
                    html.Div([html.Label('Draht'),
                            dcc.Dropdown(
                                id='wire-update',
                                options=[{'label': i, 'value':i} for i in df['bond_wire'].unique()],
                                value= [i for i in df['bond_wire'].unique()],
                                multi=True)],
                                    style={'width':'23%', 'display': 'inline-block', 'float':'left', 'paddingRight': '5%'}),
                    html.Div([html.Label('Devicegruppe'),
                            dcc.Dropdown(
                                id='device-group-update',
                                options=[{'label': i, 'value':i} for i in sorted(df['device_group'].unique())],
                                value= [i for i in sorted(df['device_group'].unique())],
                                multi=True)],
                                    style={'width':'85%', 'display': 'inline-block', 'float':'left', 'paddingLeft': '5%'}),
                    html.Div([
                            html.Button(
                                id='plot-button',
                                n_clicks=0,
                                children='Click',
                                className='myButton1')],
                                    style={'width':'12%', 'display': 'inline-block', 'float':'left', 'paddingLeft': '0.8%', 'marginTop':'3%', 'paddingRight': '5%'}),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Br(),
                    html.Div(className="small-content-container", children=[
                    html.Div(
                            [dash_table.DataTable(
                                id='lot-data-table',
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
                                 columns=[
                                                 {'name': 'Charge', 'id': 'a_lot'},
                                                 {'name': 'Typ', 'id': 'device'},
                                                 {'name': 'Package', 'id': 'package'},
                                                 {'name': 'Group', 'id': 'device_group'},
                                                 {'name': 'Reject', 'id': 'rejected'},
                                                 {'name': 'Output', 'id': 'final_test_output'},
                                                 {'name': 'Ausbeute', 'id': 'final_test_yield'},
                                                 {'name': 'LieferD.', 'id': 'delivery_date'},
                                                 {'name': 'Q-ID', 'id': 'quality_id'},
                                                 {'name': 'Class', 'id': 'class_name'},
                                                 {'name': 'Editer', 'id': 'edit_user'},
                                                 {'name': 'Editdatum', 'id': 'edit_date'}],

                                 style_header={'backgroundColor': '#6983aa', 'fontWeight': 'bold'},
                                 style_cell={'backgroundColor': '#e4e4e4',
                                            'color': 'black',
                                            'textAlign': 'left',
                                            'font-family': 'Overpass',
                                            'font-size': '0.83rem'},
                                 style_table={
                                            'title': 'Datatable for lots',
                                            'maxWidth': '100%',
                                            'maxHeight': '540px',
                                            'overflowX': 'scroll',
                                            'textOverflow': 'ellipsis'},
                                style_data_conditional=[
                                                {
                                                    'if': {
                                                        'column_id': 'rejected_perc',
                                                        'filter_query': '{rejected_perc} >= 1.5 && {rejected_perc}  < 2'
                                                    },
                                                    'backgroundColor': '#f17808',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'rejected_perc',
                                                        'filter_query': '{rejected_perc} >= 2'
                                                    },
                                                    'backgroundColor': '#d92027',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'ta_perc',
                                                        'filter_query': '{ta_perc} >= 1.5 && {ta_perc}  < 2'
                                                    },
                                                    'backgroundColor': '#f17808',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'ta_perc',
                                                        'filter_query': '{ta_perc} >= 2'
                                                    },
                                                    'backgroundColor': '#d92027',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'gw_perc',
                                                        'filter_query': '{gw_perc} >= 1.5 && {gw_perc}  < 2'
                                                    },
                                                    'backgroundColor': '#f17808',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'gw_perc',
                                                        'filter_query': '{gw_perc} >= 2'
                                                    },
                                                    'backgroundColor': '#d92027',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'final_test_gross_fails',
                                                        'filter_query': '{final_test_gross_fails} >= 5000 && {final_test_gross_fails}  < 10000'
                                                    },
                                                    'backgroundColor': '#f17808',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'final_test_gross_fails',
                                                        'filter_query': '{final_test_gross_fails} >= 10000 && {final_test_gross_fails}  < 9999999999'
                                                    },
                                                    'backgroundColor': '#d92027',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'final_test_gross_fails',
                                                        'filter_query': '{final_test_gross_fails} >= 9999999999'
                                                    },
                                                    'backgroundColor': '#303960',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'final_test_para_fails',
                                                        'filter_query': '{final_test_para_fails} >= 5000 && {final_test_para_fails}  < 10000'
                                                    },
                                                    'backgroundColor': '#f17808',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'final_test_para_fails',
                                                        'filter_query': '{final_test_para_fails} >= 10000 && {final_test_para_fails}  < 9999999999'
                                                    },
                                                    'backgroundColor': '#d92027',
                                                    'color': 'white'
                                                },
                                                {
                                                    'if': {
                                                        'column_id': 'final_test_para_fails',
                                                        'filter_query': '{final_test_para_fails} >= 9999999999'
                                                    },
                                                    'backgroundColor': '#303960',
                                                    'color': 'white'
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
                                                        'column_id': 'rejected',
                                                        'filter_query': '{rejected} >= 9999999999'
                                                    },
                                                    'backgroundColor': '#303960',
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
                                    style = {'height': '540px', 'paddingLeft': '0.7%', 'paddingRight': '0.7%','paddingTop' : '0.7%'})],
                                    style={'marginLeft': '3%', 'marginRight': '3%', 'marginTop': '3.5%', 'paddingBottom': '3.7%'}),
                    html.Div(className="small-content-container", children = [dcc.Graph(id='app3-graph-1')],
                                    style = {'width':'405px', 'marginTop': '5%', 'marginBottom': '1.5%', 'display': 'inline-block', 'paddingBottom': '30px', 'float': 'left'}),

                    html.Div(className="small-content-container", children = [html.H5("TP Summary"), html.Div(id='data-table-2')],
                                    style = {'width':'405px', 'marginTop': '5%', 'marginBottom': '1.5%','marginLeft': '15px','display': 'inline-block', 'paddingBottom': '30px', 'float': 'left'}),

                    html.Div(className="small-content-container", children = [html.H5("Testdaten"), html.Div(id='data-table-3')],
                                    style = {'width':'485px', 'marginTop': '5%', 'marginBottom': '1.5%','marginLeft': '15px','marginRight': '0%','display': 'inline-block', 'paddingBottom': '30px', 'float': 'left'})
                    ], style = {'width': '1325px', 'marginLeft': '15px',  'marginTop': '50px', 'marginBottom': '35px', 'paddingBottom': '35px'})
])

@app.callback(
         [Output('lot-data-table', 'data'),
          Output('lot-data-table', 'columns'),
          Output('lot-data-table', 'page_count')],
        [Input('plot-button', 'n_clicks'),
         Input('lot-data-table', "page_current"),
         Input('lot-data-table', "page_size"),
         Input('lot-data-table', "sort_by"),
         Input('lot-data-table', "filter_query")],
        [State('whatdata','value'),
         State('package-update', 'value'),
         State('wire-update', 'value'),
         State('date-picker-range', 'start_date'),
         State('date-picker-range', 'end_date'),
         State('device-group-update', 'value')])

def update_table_lot(n_clicks, page_current, page_size, sort_by, filter, what_data, package_update, wire_update, start_date, end_date, device_g_update):
    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                       user='WebServer',
                       password='W3bS3rv3r',
                       database='ZNGFinalTest')
    # data cleaning and sorting
    if what_data == 'wafer':
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date,ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (package <> 'SEN') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
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
        tbl4 AS ( \
        SELECT DISTINCT ZNGFinalTest.final_test3.tbl_summaries.lot, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.workplace AS NVARCHAR(MAX)), '; ') AS workplace, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.tester AS NVARCHAR(MAX)), '; ') AS tester, STRING_AGG(CAST(ZNGFinalTest.final_test3.tbl_summaries.operator AS NVARCHAR(MAX)), '; ') AS operator \
        FROM ZNGFinalTest.final_test3.tbl_summaries \
        GROUP BY ZNGFinalTest.final_test3.tbl_summaries.lot \
        ), \
        tbl5 AS ( \
        SELECT lot, STRING_AGG(CAST(ba AS NVARCHAR(MAX)), ', ') AS ba \
        FROM ZNGProduction.catuno.tbl_lots \
        GROUP BY lot \
        ) \
        SELECT tbl1.a_lot, tbl5.ba, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.department, tbl1.package, tbl1.bond_wire, tbl1.ship_package, tbl1.uk_input, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, tbl4.operator, tbl4.tester, tbl4.workplace, tbl1.transistor_type, tbl1.chip_configuration, tbl1.lead_frame \
        FROM tbl1  \
        LEFT JOIN tbl2 \
        ON tbl2.lot = tbl1.a_lot \
        LEFT JOIN tbl4 \
        ON tbl4.lot = tbl1.a_lot \
        LEFT JOIN tbl5 \
        ON tbl5.lot = tbl1.a_lot \
        ORDER BY a_lot DESC"

        df = pd.read_sql(query, conn)
        df = df[df['final_test_yield'].notnull()]

        # df.to_csv("initial_lot.txt",index=False)

        # df['create_date'] = df['create_date'].astype(str)
        # df['create_date'] = df['create_date'].str.split('\s+').str[0]
        # df['create_user'] = df['create_user'].str.split('-').str[0].str.capitalize()
        # df['create_date'].replace({'NaT': ' '}, inplace=True)

        #cleaing for workplace, operator and tester
        df['workplace'].fillna('; ', inplace=True)
        df['workplace'] = df['workplace'].apply(lambda s: ', '.join(set(s.split('; '))))
        df['operator'].fillna('; ', inplace=True)
        df['operator'] = df['operator'].apply(lambda s: ', '.join(set(s.split('; '))))
        df['tester'].fillna('; ', inplace=True)
        df['tester'] = df['tester'].apply(lambda s: ', '.join(set(s.split('; '))))

        # df['comment'].fillna('<p>', inplace=True)
        # df['comment'] = df['comment'].map(strip_tags)

        # fill Nan value
        df['transistor_type'].fillna("-", inplace=True)
        df['ship_package'].fillna("-", inplace=True)
        # df['lead_frame'].fillna("-", inplace=True)
        # df['box_class'].fillna("-", inplace=True)

        # for total rejection
        df['rejected'] = df['final_test_para_fails'] + df['final_test_gross_fails']
        df['rejected_perc'] = round(100*(df['rejected'])/(df['final_test_output'] + df['rejected']), 2)
        # GW percentage
        df['gw_perc'] = round(100*(df['final_test_para_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # TA percentage
        df['ta_perc'] = round(100*(df['final_test_gross_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # remove old data not delivered or with missing data
        df = df[(df['a_lot'] != '446609') & (df['a_lot'] != '450934') & (df['a_lot'] != '456671') & (df['a_lot'] != '462456') & (df['a_lot'] != '464058')& (df['a_lot'] != '464058')& (df['a_lot'] != '478010')& (df['a_lot'] != '479189')& (df['a_lot'] != '511654')& (df['a_lot'] != '569602')&  (df['a_lot'] != '574134')]

        # fill empty cells in wafer info
        df['wafer_info'].fillna("Unbekannt", inplace=True)

        table_columns=[
                        {'name': 'Charge', 'id': 'a_lot'},
                        {'name': 'LS #', 'id': 'ba'},
                        {'name': 'Typ', 'id': 'device'},
                        {'name': 'Package', 'id': 'package'},
                        {'name': 'Group', 'id': 'device_group'},
                        {'name': 'Transistor', 'id': 'transistor_type'},
                        {'name': 'GW', 'id': 'final_test_para_fails'},
                        {'name': 'TA', 'id': 'final_test_gross_fails'},
                        {'name': 'Reject', 'id': 'rejected'},
                        {'name': 'Output', 'id': 'final_test_output'},
                        {'name': 'GW (%)', 'id': 'gw_perc'},
                        {'name': 'TA (%)', 'id': 'ta_perc'},
                        {'name': 'Reject (%)', 'id': 'rejected_perc'},
                        {'name': 'Ausbeute (%)', 'id': 'final_test_yield'},
                        {'name': 'LieferD.', 'id': 'delivery_date'},
                        {'name': 'Wafer: Menge(probed/unprobed))', 'id': 'wafer_info'},
                        {'name': 'Gurt', 'id': 'ship_package'},
                        {'name': 'Maschine N.', 'id': 'workplace'},
                        {'name': 'Tester', 'id': 'tester'},
                        {'name': 'Operator', 'id': 'operator'}
                        ]
    elif what_data == 'comment':
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date,ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (package <> 'SEN') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
        ), \
        tbl3 AS ( \
        SELECT ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ), \
        tbl5 AS ( \
        SELECT lot, STRING_AGG(CAST(ba AS NVARCHAR(MAX)), ', ') AS ba \
        FROM ZNGProduction.catuno.tbl_lots \
        GROUP BY lot \
        ) \
        SELECT tbl1.a_lot, tbl5.ba, tbl1.device, tbl1.device_group, tbl1.department, tbl1.package, tbl1.bond_wire, tbl1.ship_package, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, tbl3.comment,  REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date, REPLACE(REPLACE(tbl3.create_user, 'EU\\', ''), '_', '-') AS create_user, tbl3.create_date \
        FROM tbl1 \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot \
        LEFT JOIN tbl5 \
        ON tbl5.lot = tbl1.a_lot \
        ORDER BY a_lot DESC"

        df = pd.read_sql(query, conn)
        df = df[df['final_test_yield'].notnull()]
        df['create_date'] = df['create_date'].astype(str)
        df['create_date'] = df['create_date'].str.split('\s+').str[0]
        df['create_user'] = df['create_user'].str.split('-').str[0].str.capitalize()
        df['create_date'].replace({'NaT': ' '}, inplace=True)

        df['comment'].fillna('<p>', inplace=True)
        df['comment'] = df['comment'].map(strip_tags)

        # for total rejection
        df['rejected'] = df['final_test_para_fails'] + df['final_test_gross_fails']
        df['rejected_perc'] = round(100*(df['rejected'])/(df['final_test_output'] + df['rejected']), 2)
        # GW percentage
        df['gw_perc'] = round(100*(df['final_test_para_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # TA percentage
        df['ta_perc'] = round(100*(df['final_test_gross_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # remove old data not delivered or with missing data
        df = df[(df['a_lot'] != '446609') & (df['a_lot'] != '450934') & (df['a_lot'] != '456671') & (df['a_lot'] != '462456') & (df['a_lot'] != '464058')& (df['a_lot'] != '464058')& (df['a_lot'] != '478010')& (df['a_lot'] != '479189')& (df['a_lot'] != '511654')& (df['a_lot'] != '569602')&  (df['a_lot'] != '574134')]

        table_columns=[
                        {'name': 'Charge', 'id': 'a_lot'},
                        {'name': 'LS #', 'id': 'ba'},
                        {'name': 'Typ', 'id': 'device'},
                        {'name': 'Package', 'id': 'package'},
                        {'name': 'Group', 'id': 'device_group'},
                        {'name': 'GW', 'id': 'final_test_para_fails'},
                        {'name': 'TA', 'id': 'final_test_gross_fails'},
                        {'name': 'Reject', 'id': 'rejected'},
                        {'name': 'Output', 'id': 'final_test_output'},
                        {'name': 'Ausbeute (%)', 'id': 'final_test_yield'},
                        {'name': 'Q-ID', 'id': 'quality_id'},
                        {'name': 'LieferD.', 'id': 'delivery_date'},
                        {'name': 'WPS', 'id': 'wps'},
                        {'name': 'FA', 'id': 'fa'},
                        {'name': 'Class', 'id': 'class_name'},
                        {'name': 'Ursache', 'id': 'cause'},
                        {'name': 'Ersteller', 'id': 'create_user'},
                        {'name': 'Erstellungsdatum', 'id': 'create_date'},
                        {'name': 'Editer', 'id': 'edit_user'},
                        {'name': 'Editdatum', 'id': 'edit_date'},
                        {'name': 'Comment', 'id': 'comment'},
                        ]
    elif what_data == 'storage':
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date,ZNGProduction.catuno.tbl_products.lead_frame, ZNGProduction.catuno.tbl_products.transistor_type, ZNGProduction.catuno.tbl_products.chip_configuration \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (package <> 'SEN') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
        ), \
        tbl3 AS ( \
        SELECT ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ), \
        tbl5 AS ( \
        SELECT lot, STRING_AGG(CAST(ba AS NVARCHAR(MAX)), ', ') AS ba \
        FROM ZNGProduction.catuno.tbl_lots \
        GROUP BY lot \
        ), \
        tbl6 AS ( \
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
        ) \
        SELECT tbl1.a_lot, tbl5.ba, tbl1.device, tbl1.device_group, tbl1.package, tbl1.bond_wire, tbl1.ship_package, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, tbl3.comment,  REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date, REPLACE(REPLACE(tbl3.create_user, 'EU\\', ''), '_', '-') AS create_user, tbl3.create_date, tbl6.box_class \
        FROM tbl1 \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot \
        LEFT JOIN tbl5 \
        ON tbl5.lot = tbl1.a_lot \
        LEFT JOIN tbl6 \
        ON tbl5.lot =tbl6.lot \
        ORDER BY a_lot DESC"

        df = pd.read_sql(query, conn)
        df = df[df['final_test_yield'].notnull()]

        df['create_date'] = df['create_date'].astype(str)
        df['create_date'] = df['create_date'].str.split('\s+').str[0]
        df['create_user'] = df['create_user'].str.split('-').str[0].str.capitalize()
        df['create_date'].replace({'NaT': ' '}, inplace=True)


        df['comment'].fillna('<p>', inplace=True)
        df['comment'] = df['comment'].map(strip_tags)

        # fill Nan value
        df['box_class'].fillna("-", inplace=True)

        # for total rejection
        df['rejected'] = df['final_test_para_fails'] + df['final_test_gross_fails']
        df['rejected_perc'] = round(100*(df['rejected'])/(df['final_test_output'] + df['rejected']), 2)
        # GW percentage
        df['gw_perc'] = round(100*(df['final_test_para_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # TA percentage
        df['ta_perc'] = round(100*(df['final_test_gross_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # remove old data not delivered or with missing data
        df = df[(df['a_lot'] != '446609') & (df['a_lot'] != '450934') & (df['a_lot'] != '456671') & (df['a_lot'] != '462456') & (df['a_lot'] != '464058')& (df['a_lot'] != '464058')& (df['a_lot'] != '478010')& (df['a_lot'] != '479189')& (df['a_lot'] != '511654')& (df['a_lot'] != '569602')&  (df['a_lot'] != '574134')]

        table_columns=[{'name': 'Charge', 'id': 'a_lot'},
                        {'name': 'LS #', 'id': 'ba'},
                        {'name': 'Typ', 'id': 'device'},
                        {'name': 'Package', 'id': 'package'},
                        {'name': 'Group', 'id': 'device_group'},
                        {'name': 'Reject', 'id': 'rejected'},
                        {'name': 'Output', 'id': 'final_test_output'},
                        {'name': 'Ausbeute (%)', 'id': 'final_test_yield'},
                        {'name': 'Gurt', 'id': 'ship_package'},
                        {'name': 'Q-ID', 'id': 'quality_id'},
                        {'name': 'LieferD.', 'id': 'delivery_date'},
                        {'name': 'Storage', 'id': 'box_class'}
                        ]
    elif what_data == 'short':
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') AND (package <> 'SEN') \
        ), \
        tbl3 AS ( \
        SELECT ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ) \
        SELECT tbl1.a_lot, tbl1.device, tbl1.device_group, tbl1.package, tbl1.bond_wire, tbl1.ship_package, tbl1.final_test_input, tbl1.final_test_para_fails, tbl1.final_test_gross_fails, tbl1.final_test_output, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, tbl3.cause, tbl3.comment, REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date \
        FROM tbl1 \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot\
        ORDER BY a_lot DESC"

        df = pd.read_sql(query, conn)
        df = df[df['final_test_yield'].notnull()]

        # for total rejection
        df['rejected'] = df['final_test_para_fails'] + df['final_test_gross_fails']
        df['rejected_perc'] = round(100*(df['rejected'])/(df['final_test_output'] + df['rejected']), 2)
        # GW percentage
        df['gw_perc'] = round(100*(df['final_test_para_fails'])/(df['final_test_output'] + df['rejected']), 2)

        # TA percentage
        df['ta_perc'] = round(100*(df['final_test_gross_fails'])/(df['final_test_output'] + df['rejected']), 2)


        # remove old data not delivered or with missing data
        df = df[(df['a_lot'] != '446609') & (df['a_lot'] != '450934') & (df['a_lot'] != '456671') & (df['a_lot'] != '462456') & (df['a_lot'] != '464058')& (df['a_lot'] != '464058')& (df['a_lot'] != '478010')& (df['a_lot'] != '479189')& (df['a_lot'] != '511654')& (df['a_lot'] != '569602')&  (df['a_lot'] != '574134')]

        table_columns=[

                        {'name': 'Charge', 'id': 'a_lot'},
                        {'name': 'Typ', 'id': 'device'},
                        {'name': 'Package', 'id': 'package'},
                        {'name': 'Group', 'id': 'device_group'},
                        {'name': 'Reject', 'id': 'rejected'},
                        {'name': 'Output', 'id': 'final_test_output'},
                        {'name': 'Ausbeute', 'id': 'final_test_yield'},
                        {'name': 'LieferD.', 'id': 'delivery_date'},
                        {'name': 'Q-ID', 'id': 'quality_id'},
                        {'name': 'Class', 'id': 'class_name'},
                        {'name': 'Editer', 'id': 'edit_user'},
                        {'name': 'Editdatum', 'id': 'edit_date'}]
    else:
        query = "WITH tbl1 AS ( \
        SELECT ZNGProduction.catuno.tbl_lots.lot AS a_lot, device, device_group, department, package, bond_wire, ship_package, uk_input, final_test_input, final_test_para_fails, final_test_gross_fails, final_test_output, final_test_yield, delivery_date \
        FROM ZNGProduction.catuno.vw_yield  /*yield*/ \
        LEFT JOIN ZNGProduction.catuno.tbl_lots /*product for connection*/ \
        ON ZNGProduction.catuno.vw_yield.ba = ZNGProduction.catuno.tbl_lots.ba \
        LEFT JOIN ZNGProduction.catuno.tbl_products /*package and die device group*/ \
        ON ZNGProduction.catuno.tbl_products.product = ZNGProduction.catuno.tbl_lots.product \
        WHERE (package <> 'STACK') AND (package <> 'DIODE') AND (package <> 'SEN') AND (lot <> '430101') AND (lot <> '378471') AND (lot <> 'FST866FTA') AND (device_group <> 'REST') \
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
        SELECT ZNGFinalTest.quality.vw_lots.quality_id, ZNGFinalTest.quality.vw_lots.lot, comment, cause, ZNGFinalTest.quality.vw_lots.wps, ZNGFinalTest.quality.vw_lots.fa, ZNGFinalTest.quality.vw_lots.edit_user,  ZNGFinalTest.quality.vw_last_comments.date, ZNGFinalTest.quality.tbl_classes.class_name, ZNGFinalTest.quality.vw_lots.create_user, ZNGFinalTest.quality.vw_lots.create_date \
        FROM ZNGFinalTest.quality.vw_last_comments \
        JOIN ZNGFinalTest.quality.vw_lots \
        ON ZNGFinalTest.quality.vw_lots.quality_id = ZNGFinalTest.quality.vw_last_comments.quality_id \
        JOIN ZNGFinalTest.quality.tbl_classes \
        ON ZNGFinalTest.quality.tbl_classes.class_id = ZNGFinalTest.quality.vw_lots.class_id \
        ) \
        SELECT tbl1.a_lot, tbl1.device, tbl2.wafer_info, tbl1.device_group, tbl1.package, tbl1.bond_wire, tbl1.ship_package, tbl1.final_test_yield, tbl1.delivery_date, CASE WHEN tbl3.quality_id IS NULL THEN '0' ELSE tbl3.quality_id END AS quality_id, tbl3.wps, tbl3.fa, CASE WHEN tbl3.class_name = 'Qualität allg. / Zuverlässigkeit' THEN 'Allg. & ZVR.' WHEN tbl3.class_name = 'nicht klassifiziert' THEN 'N.K.' ELSE tbl3.class_name END AS class_name, REPLACE(REPLACE(tbl3.cause, '<div>', ''), '</div>', '') AS cause, tbl3.comment, REPLACE(REPLACE(tbl3.edit_user, 'EU\\', ''), '_', '-') AS edit_user, tbl3.date AS edit_date \
        FROM tbl1 \
        LEFT JOIN tbl2  \
        ON tbl2.lot = tbl1.a_lot \
        LEFT JOIN tbl3 \
        ON tbl3.lot = tbl1.a_lot \
        ORDER BY a_lot DESC"

        df = pd.read_sql(query, conn)
        df = df[df['final_test_yield'].isnull()]
        df['month'] = datetime.today().month
        df['year'] = datetime.today().year

        # for total rejection
        df['rejected'] = df['a_lot']
        df['rejected_perc'] = df['a_lot']
        # # GW percentage
        df['gw_perc'] = df['a_lot']

        # TA percentage
        df['ta_perc'] = df['a_lot']

        # fill empty cells in wafer info
        df['wafer_info'].fillna("Unbekannt", inplace=True)
        table_columns=[
                        {'name': 'Charge', 'id': 'a_lot'},
                        {'name': 'Typ', 'id': 'device'},
                        {'name': 'Package', 'id': 'package'},
                        {'name': 'Group', 'id': 'device_group'},
                        {'name': 'Q-ID', 'id': 'quality_id'},
                        {'name': 'Class', 'id': 'class_name'},
                        {'name': 'Ursache', 'id': 'cause'},
                        {'name': 'Editer', 'id': 'edit_user'},
                        {'name': 'Editdatum', 'id': 'edit_date'},
                        {'name': 'Wafer: Menge(probed/unprobed))', 'id': 'wafer_info'}
                        ]

    # date-picker data
    start_date, end_date = dt.strptime(re.split('T| ', start_date)[0], '%Y-%m-%d'), dt.strptime(re.split('T| ', end_date)[0], '%Y-%m-%d')

    # date filtering by datepicker
    filtered_data = df[(df['delivery_date'] >= start_date) & (df['delivery_date'] <= end_date) | (df['delivery_date'].isnull())]

    # NaN or NaT data sorting
    filtered_data['delivery_date'] = filtered_data['delivery_date'].astype(str)
    filtered_data['delivery_date'].replace({'NaT': 'Vor Auslieferung'}, inplace=True)
    # df['delivery_date'].fillna('Not_yet_delivered x', inplace=True)
    # df['day'].fillna('Not_delivered', inplace=True)
    # df['month'].fillna(datetime.today().month, inplace=True)
    # df['year'].fillna(datetime.today().year, inplace=True)

    # data filtering by options - buttons
    filtered_data = filtered_data[(package_filter(filtered_data, package_update)) & (wire_filter(filtered_data, wire_update)) & (device_group_update(filtered_data, device_g_update))]

    # filter for edit date and wps,fa <- because of the change made after writing this code so this filter was added in order to fitler them later.
    if what_data == 'wafer':
        pass
    elif what_data == 'comment':
        # Q date sorting
        filtered_data['edit_date'] = filtered_data['edit_date'].astype(str)
        filtered_data['edit_date'] = filtered_data['edit_date'].str.split('\s+').str[0]
        filtered_data['edit_date'].replace({'NaT': ' '}, inplace=True)
        filtered_data['edit_user'] = filtered_data['edit_user'].str.split('-').str[0].str.capitalize()

        #################### wps and fa data type change ####################
        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df is loop by columns, same as for column in booleandf.columns:
        for column in filtered_data[['wps', 'fa']]:
            filtered_data[column] = filtered_data[column].map(booleanDictionary)
        #####################################################################
    elif what_data == 'storage':
        # Q date sorting
        filtered_data['edit_date'] = filtered_data['edit_date'].astype(str)
        filtered_data['edit_date'] = filtered_data['edit_date'].str.split('\s+').str[0]
        filtered_data['edit_date'].replace({'NaT': ' '}, inplace=True)
        filtered_data['edit_user'] = filtered_data['edit_user'].str.split('-').str[0].str.capitalize()

        #################### wps and fa data type change ####################
        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df is loop by columns, same as for column in booleandf.columns:
        for column in filtered_data[['wps', 'fa']]:
            filtered_data[column] = filtered_data[column].map(booleanDictionary)
        #####################################################################
    elif what_data == 'short':
        # Q date sorting
        filtered_data['edit_date'] = filtered_data['edit_date'].astype(str)
        filtered_data['edit_date'] = filtered_data['edit_date'].str.split('\s+').str[0]
        filtered_data['edit_date'].replace({'NaT': ' '}, inplace=True)
        filtered_data['edit_user'] = filtered_data['edit_user'].str.split('-').str[0].str.capitalize()

        #################### wps and fa data type change ####################
        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df is loop by columns, same as for column in booleandf.columns:
        for column in filtered_data[['wps', 'fa']]:
            filtered_data[column] = filtered_data[column].map(booleanDictionary)
        #####################################################################
    else:
        # Q date sorting
        filtered_data['edit_date'] = filtered_data['edit_date'].astype(str)
        filtered_data['edit_date'] = filtered_data['edit_date'].str.split('\s+').str[0]
        filtered_data['edit_date'].replace({'NaT': ' '}, inplace=True)
        filtered_data['edit_user'] = filtered_data['edit_user'].str.split('-').str[0].str.capitalize()

        #################### wps and fa data type change ####################
        # replace wps boolean
        booleanDictionary = {True: 'O', False: 'X'}

        #loop by df is loop by columns, same as for column in booleandf.columns:
        for column in filtered_data[['wps', 'fa']]:
            filtered_data[column] = filtered_data[column].map(booleanDictionary)
        #####################################################################

    # turn into percentage
    filtered_data['final_test_yield'] = round(100*filtered_data['final_test_yield'],2)

    # combine device with wire
    filtered_data['device'] = filtered_data['device'] + '-'+ filtered_data['bond_wire']


    ############### table filter ####################
    # filtering for datatable
    filtering_expressions = filter.split(' && ')

    # reassign filtered data to dff for filter of datatable
    dff = filtered_data
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    # pagination
    page_count = math.ceil(len(filtered_data['a_lot'])/page_size)
    ##################################################

    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")
    print("           DASHBOARD (INFO)    ")
    print("###############################")
    print("###############################")
    print("###############################")
    print("###############################")

    return dff.iloc[page_current*page_size: (page_current + 1)*page_size].to_dict('records'), table_columns, page_count

@app.callback(
        [Output('app3-graph-1', 'figure'),
         Output('data-table-2', 'children'),
         Output('data-table-3', 'children')],
         [Input('lot-data-table', 'derived_virtual_data'),
         Input('lot-data-table', 'derived_virtual_selected_rows')])

def FT_summary(rows, derived_virtual_data, max_rows=300):
    # extract lot number
    if len(derived_virtual_data) == 0:
        selected_lot_number = pd.DataFrame(rows).iloc[0]['a_lot']
    else:
        dff2 = pd.DataFrame.from_dict({'a_lot':[1,2,3], 'aaa': [4,5,6]}) if rows is None else pd.DataFrame(rows)
        selected_lot_number = dff2.iloc[derived_virtual_data]['a_lot'].values[0]

    conn = pymssql.connect(server='ZNGERP01\\ZNGFINALTEST',
                       user='WebServer',
                       password='W3bS3rv3r',
                       database='ZNGFinalTest')

    query = "SELECT DISTINCT lot, sub_lot, field_lot, device, field_operator, ISNULL(bin_name, 'Unbekannt') + ' [' + CAST(bin_number as varchar(20)) + ']' AS bin_ID, count, pass_fail \
    FROM ZNGFinalTest.final_test3.tbl_summaries \
    FULL JOIN ZNGFinalTest.final_test3.tbl_summary_bins \
    ON ZNGFinalTest.final_test3.tbl_summaries.summary_id = ZNGFinalTest.final_test3.tbl_summary_bins.summary_id \
    WHERE (tape_reel = 0) AND (lot NOT LIKE 'Z%') AND (lot NOT LIKE '1%') AND (lot NOT LIKE '2%') AND (lot NOT LIKE '3%') AND (lot = '{}') \
    ORDER BY lot DESC, sub_lot, bin_ID".format(selected_lot_number)

    df = pd.read_sql(query, conn)

    if len(df) == 0:
        # dummy graph if there's no data
        fig_1 = go.Figure(
                        data= [
                        {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'B'},
                        {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'A'}
                        ],
                        layout = go.Layout(
                                    title = 'Keine Daten',
                                    xaxis_tickangle=-90,
                                    # titlefont=dict(color= 'black', size=21, family = 'inherit'),
                                    # paper_bgcolor='white',
                                    # plot_bgcolor= '#d6e5fa',
                                    # autosize = False,
                                    # width = 1500,
                                    # height = 380,
                                    hovermode = 'x',
                                    # legend_orientation="h",
                                    # legend=dict(x=0.1, y=1.0)
                                        )
                        )

    else:
        if df['pass_fail'].nunique() == 1:
            whole_lot_yield = df.groupby(['lot','bin_ID'])['count'].agg(count= sum)
            whole_lot_yield['percentage'] = round(df.groupby(['lot','bin_ID',])['count'].agg(count= sum).groupby(level = 0).apply(lambda x : 100 * x / float(x.sum())), 2)
            whole_lot_yield.reset_index(inplace=True)
            whole_lot_yield.rename(columns={'lot': 'Lot', 'bin_ID': 'Bin', 'count': 'Count', 'percentage': 'Percent'}, inplace=True)
            whole_lot_yield.sort_values('Percent', inplace=True, ascending=False)
            fig_1 = go.Figure(
                            data = [go.Bar(
                                        x = whole_lot_yield['Bin'],
                                        y = whole_lot_yield['Percent'],
                                        # y = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].diff().values,
                                        name = 'name',
                                        hoverinfo = 'y',
                                        # marker = dict(color=color1.tolist()),
                                        showlegend=False
                                        )],
                            layout = go.Layout(
                                        title = 'Endmessung Statistik (Total)',
                                        xaxis_tickangle=-90,
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

            fig_1.layout.yaxis.update(title = 'Prozent',
                                    # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                    showgrid =True)

        else:
            whole_lot_yield = df[df['pass_fail'] != 0].groupby(['lot','bin_ID'])['count'].agg(count= sum)
            whole_lot_yield['percentage'] = round(df[df['pass_fail'] != 0].groupby(['lot','bin_ID',])['count'].agg(count= sum).groupby(level = 0).apply(lambda x : 100 * x / float(x.sum())), 2)
            whole_lot_yield.reset_index(inplace=True)
            whole_lot_yield.rename(columns={'lot': 'Lot', 'bin_ID': 'Bin', 'count': 'Count', 'percentage': 'Percent'}, inplace=True)
            whole_lot_yield.sort_values('Percent', inplace=True, ascending=False)
            fig_1 = go.Figure(
                            data = [go.Bar(
                                        x = whole_lot_yield['Bin'],
                                        y = whole_lot_yield['Percent'],
                                        # y = df_yield_app[package_list(df_yield_app, package_)].pivot_table(index = time_type, columns = df_yield_app['year'], values = 'final_test_output',  aggfunc = np.sum)[year__].diff().values,
                                        name = 'name',
                                        hoverinfo = 'y',
                                        # marker = dict(color=color1.tolist()),
                                        showlegend=False
                                        )],
                            layout = go.Layout(
                                        title = 'Endmessung Statistik (Total)',
                                        xaxis_tickangle=-90,
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

            fig_1.layout.yaxis.update(title = 'Prozent',
                                    # titlefont=dict(color= 'black', size=16, family = 'inherit'),
                                    showgrid =True)

    if len(df) == 0:
        table_2 = html.H4("Keine Summarydaten im SQLserver.")
    else:
        if df['pass_fail'].nunique() == 1:
            sub_lot_yield = df.groupby(['field_lot','bin_ID'])['count'].agg(count = sum)
            sub_lot_yield['percentage'] = round(df.groupby(['field_lot','bin_ID'])['count'].agg(count= sum).groupby(level = 0).apply(lambda x : 100 * x / float(x.sum())), 2)
            sub_lot_yield.reset_index(inplace=True)
            sub_lot_yield.rename(columns={'lot': 'Lot', 'bin_ID': 'Bin', 'count': 'Count', 'percentage': 'Percent'}, inplace=True)
            table_2 =  html.Div([html.Div(className="datadiv", children=["TP Summarydaten"]),
                html.Table(
                # Header
                [html.Tr([html.Th(col) for col in sub_lot_yield.columns]) ] +
                # Body
                [html.Tr([
                    html.Td(sub_lot_yield.iloc[i][col]) for col in sub_lot_yield.columns
                ]) for i in range(min(len(sub_lot_yield), max_rows))]
            )
            ])

        else:
            sub_lot_yield = df[df['pass_fail'] != 0].groupby(['field_lot','bin_ID'])['count'].agg(count = sum)
            sub_lot_yield['percentage'] = round(df[df['pass_fail'] != 0].groupby(['field_lot','bin_ID'])['count'].agg(count= sum).groupby(level = 0).apply(lambda x : 100 * x / float(x.sum())), 2)
            sub_lot_yield.reset_index(inplace=True)
            sub_lot_yield.rename(columns={'field_lot': 'Lot/TP', 'bin_ID': 'Bin', 'count': 'Count', 'percentage': 'Percent'}, inplace=True)
            table_2 =  html.Div([html.Div(className="datadiv", children=["TP Summarydaten"]),
                html.Table(
                # Header
                [html.Tr([html.Th(col) for col in sub_lot_yield.columns]) ] +
                # Body
                [html.Tr([
                    html.Td(sub_lot_yield.iloc[i][col]) for col in sub_lot_yield.columns
                ]) for i in range(min(len(sub_lot_yield), max_rows))]
            )
            ])

    query2 = "SELECT DISTINCT field_lot, lot,device ,test_name, test_number,tbl_summary_tests.count \
    FROM final_test3.tbl_summaries \
    FULL JOIN final_test3.tbl_summary_bins \
    ON tbl_summaries.summary_id = tbl_summary_bins.summary_id \
    FULL JOIN final_test3.tbl_summary_tests \
    ON final_test3.tbl_summary_tests.summary_id = final_test3.tbl_summaries.summary_id \
    WHERE (lot NOT LIKE 'Z%') AND (lot NOT LIKE '1%') AND (lot NOT LIKE '2%') AND (lot NOT LIKE '3%') AND (lot = '{}') \
    ORDER BY field_lot, test_number".format(selected_lot_number)

    df2 = pd.read_sql(query2, conn)

    if len(df2) == 0:
        table_3 = html.H4("Keine Testdaten im SQLserver.")
    else:
        test_result = df2[['field_lot', 'device', 'test_name', 'test_number', 'count']]
        test_result.reset_index(inplace=True)
        test_result.drop(columns=['index'], inplace=True)
        test_result.rename(columns={'field_lot': 'Lot/TP', 'device': 'Typ', 'test_name': 'Test', 'test_number': 'TestN.', 'count': 'Count'}, inplace=True)
        table_3 = html.Div([html.Div(className="datadiv", children=["Testdaten"]),
            html.Table(
            # Header
            [html.Tr([html.Th(col) for col in test_result.columns]) ] +
            # Body
            [html.Tr([
                html.Td(test_result.iloc[i][col]) for col in test_result.columns
            ]) for i in range(min(len(test_result), max_rows))]
        )
        ])
    return  fig_1, table_2, table_3

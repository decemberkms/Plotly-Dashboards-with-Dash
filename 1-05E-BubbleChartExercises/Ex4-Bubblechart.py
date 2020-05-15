#######
# Objective: Create a bubble chart that compares three other features
# from the mpg.csv dataset. Fields include: 'mpg', 'cylinders', 'displacement'
# 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'name'
######

# Perform imports here:
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# create a DataFrame from the .csv file:
df = pd.read_csv('../data/mpg.csv')
print(df)

# create data by choosing fields for x, y and marker size attributes
trace0 = go.Scatter(
                x = df['mpg'],
                y = df['displacement'],
                text = df['name'],
                mode ='markers',
                marker = dict(size=3*df['cylinders'], color=df['weight'],
                showscale=True)
)

data =[trace0]
# create a layout with a title and axis labels
layout = go.Layout(
                title ='Three comparison',
                hovermode = 'closest',
                xaxis = dict(title = 'mpg'),
                yaxis = dict(title='displacement')
)

# create a fig from data & layout, and plot the fig
fig = go.Figure(data=data, layout=layout)

pyo.plot(fig)

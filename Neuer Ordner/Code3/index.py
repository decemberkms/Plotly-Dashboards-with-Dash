import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3, app4


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='content-field-in-app')
])


@app.callback(Output('content-field-in-app', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.layout
    elif pathname == '/apps/app4':
        return app4.layout
    elif pathname == '/':
        return app1.layout
    else:
        return '404'

if __name__ == '__main__':
    #app.run_server(debug=False, port=8060, host='0.0.0.0')
    app.run_server(debug=False)

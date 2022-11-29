from dash import Dash, dcc, html, Input, Output, callback
import webbrowser
from threading import Timer

from layouts import layout1, layout2
import callbacks

app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
         return layout1
    elif pathname == '/page2':
         return layout2
    else:
        return '404'

def open_browser():
    url = "127.0.0.1:8050/page1"
    webbrowser.open_new_tab(url)

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run(debug=True, use_reloader=False)


    

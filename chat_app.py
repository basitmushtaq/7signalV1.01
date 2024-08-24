import dash
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests  # Import requests to make HTTP calls

# Initialize the Dash app with a dark Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# Define app layout with a gradient theme and scroll management
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Copilot", className="text-center", style={'color': '#fff'}), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Textarea(id='logs', placeholder="Enter your logs here...", className="mb-3",
                                 style={'width': '100%', 'height': 'calc(100vh - 200px)', 'color': '#fff', 'backgroundColor': '#222'}),
                    dbc.Button('Initiate Chat', id='init-chat-button', color='success', className='w-100', style={'height': '50px'})
                ], style={'padding': '20px', 'backgroundColor': '#222', 'borderColor': '#333'})
            ], style={'height': 'calc(100vh - 100px)', 'overflowY': 'auto'})
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Markdown('', id='chat-history', style={'white-space': 'pre-wrap', 'color': '#fff', 'backgroundColor': '#222'})
                ], style={'height': 'calc(100vh - 100px)', 'overflowY': 'auto', 'padding': '20px', 'backgroundColor': '#222', 'borderColor': '#333'})
            ], style={'height': 'calc(100vh - 100px)', 'overflowY': 'auto'})
        ], width=9)
    ])
], fluid=True, style={"max-width": "100%", 'height': '100vh', 'padding': '0', 'overflowY': 'hidden', 
                      'backgroundColor': '#333', 'backgroundImage': 'linear-gradient(to right, #333 25%, #444 75%)'})

# Callback to update chat area with chat history
@callback(
    Output('chat-history', 'children'),
    Input('init-chat-button', 'n_clicks'),
    State('logs', 'value'),
    prevent_initial_call=True
)
def update_chat_area(n_clicks, logs):
    if n_clicks is None or not logs:
        raise PreventUpdate
    response = requests.post("http://localhost:8000/initiate_chat/", json={"logs": logs})
    print(response)
    if response.status_code == 200:
        chat_history_response = requests.get("http://localhost:8000/analysis/")
        if chat_history_response.status_code == 200:
            return chat_history_response.json()["Analysis"]
        else:
            return "Failed to retrieve chat history."
    else:
        return "Failed to initiate chat. Error: " + response.text

if __name__ == '__main__':
    app.run_server(debug=True)

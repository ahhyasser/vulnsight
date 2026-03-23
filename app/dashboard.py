import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import requests
import pandas as pd

app = dash.Dash(__name__)

# ======================
# Layout
# ======================
app.layout = html.Div([
    html.H1("🚨 VulnSight Dashboard"),

    dcc.Interval(
        id='interval',
        interval=3000,  # كل 3 ثواني
        n_intervals=0
    ),

    html.Div(id='content')
])

# ======================
# Load Data Function
# ======================
def load_alerts():
    try:
        url = "http://127.0.0.1:8000/alerts"
        response = requests.get(url)

        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            return pd.DataFrame()

    except:
        return pd.DataFrame()

# ======================
# Callback (Auto Update)
# ======================
@app.callback(
    Output('content', 'children'),
    Input('interval', 'n_intervals')
)
def update_dashboard(n):

    df = load_alerts()

    if df.empty:
        return html.H3("❌ No data")

    return [
        html.H3(f"Total Alerts: {len(df)}"),

        dcc.Graph(
            figure={
                'data': [{'x': df['severity'], 'type': 'histogram'}],
                'layout': {'title': 'Severity Distribution'}
            }
        ),

        dcc.Graph(
            figure={
                'data': [{'x': df['confidence'], 'type': 'histogram'}],
                'layout': {'title': 'Confidence Distribution'}
            }
        )
    ]

# ======================
# Run
# ======================
if __name__ == "__main__":
    app.run(debug=True)
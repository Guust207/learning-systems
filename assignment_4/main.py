from dash import Dash, html, dcc, Input, Output, callback
import plotly.graph_objs as go
import numpy as np

marks = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
         0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]

marks_dict = {i: str(i) for i in marks}

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H3("Assignment 4"),

        html.Div([
            html.Label("s"),
            dcc.Slider(id='s-slider', min=1, max=25, step=1, value=1,
                       marks={i: str(i) for i in range(1, 26)})
        ], style={'margin': '20px'}),

        html.Div([
            html.Label("P(L|Y)"),
            dcc.Slider(id='P_L_Y-slider', min=0, max=1, step=0.05, value=0.5,
                       marks=marks_dict)
        ], style={'margin': '20px'}),

        html.Div([
            html.Label("P(Y)"),
            dcc.Slider(id='P_Y-slider', min=0, max=1, step=0.05, value=0.5,
                       marks=marks_dict)
        ], style={'margin': '20px'}),

        html.Div([
            html.Label("P(nL|nY)"),
            dcc.Slider(id='P_nL_nY-slider', min=0, max=1, step=0.05, value=0.5,
                       marks=marks_dict)
        ], style={'margin': '20px'}),

        dcc.Graph(id='bar-chart')
    ],
    style={
        "width": "60%",
        "margin": "0 auto",
        "textAlign": "center",
        "backgroundColor": "#f9f9f9",
        "padding": "30px",
        "borderRadius": "12px",
        "boxShadow": "0px 0px 12px rgba(0,0,0,0.1)"
    })


@callback(
    Output("bar-chart", "figure"),
    Input("s-slider", "value"),
    Input("P_L_Y-slider", "value"),
    Input("P_Y-slider", "value"),
    Input("P_nL_nY-slider", "value")
)
def calculate_automatas(s, P_L_Y, P_Y, P_nL_nY):
    # Calculate all probabilities
    P_nL_Y = 1 - P_L_Y
    P_nY = 1 - P_Y

    probs = [
        P_Y ** 4 * P_L_Y ** 0 * P_nL_Y ** 7 * s ** 0 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 0,
        P_Y ** 3 * P_L_Y ** 0 * P_nL_Y ** 6 * s ** 1 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 1,
        P_Y ** 2 * P_L_Y ** 0 * P_nL_Y ** 5 * s ** 2 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 2,
        P_Y ** 1 * P_L_Y ** 0 * P_nL_Y ** 4 * s ** 3 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 3,
        P_Y ** 0 * P_L_Y ** 0 * P_nL_Y ** 3 * s ** 4 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 4,
        P_Y ** 0 * P_L_Y ** 1 * P_nL_Y ** 2 * s ** 5 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 4,
        P_Y ** 0 * P_L_Y ** 2 * P_nL_Y ** 1 * s ** 6 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 4,
        P_Y ** 0 * P_L_Y ** 3 * P_nL_Y ** 0 * s ** 7 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 4
    ]

    alfa = 1 / sum(probs)
    probs = [alfa * prob for prob in probs]

    # Update the data structure
    x_values = [i for i in range(1, 9)]
    y_values = probs

    # Update the figure for bar chart
    fig = go.Figure(data=[go.Bar(x=x_values, y=y_values)])

    fig.update_traces(marker_color="#828282", marker_line_color="black", marker_line_width=2, opacity=0.8)

    fig.update_layout(
        title=dict(text="Dynamic Stationary Distribution for Literal Automaton", x=0.5),
        xaxis=dict(title="π"),
        yaxis=dict(title="Probabilities", range=[0, 1], fixedrange=True),
        bargap=0,
        height=400,
        margin=dict(l=50, r=30, t=50, b=50),
        shapes=[
            dict(
                type="line",
                xref="x",
                yref="paper",
                x0=4.5,
                x1=4.5,
                y0=0,
                y1=1,
                line=dict(color="black", width=2, dash="dot")
            )
        ],
        annotations=[
            # Forgotten
            dict(
                x=4,  # roughly center of bars 1–4
                y=0.95,
                xref='x',
                yref='paper',
                text="Forgotten",
                showarrow=False,
                font=dict(size=14, color="black"),
                align="center"
            ),
            # Memorized
            dict(
                x=5,
                y=0.95,
                xref='x',
                yref='paper',
                text="Memorized",
                showarrow=False,
                font=dict(size=14, color="black"),
                align="center"
            )
        ])

    return fig


if __name__ == '__main__':
    app.run(debug=True)

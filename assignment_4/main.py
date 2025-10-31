from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd


pi_automatas = {"index": ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6", "pi7", "pi8"],
                "prob": [0, 0, 0, 0, 0, 0, 0, 0]}
df = pd.DataFrame(data=pi_automatas)

barchart_x = "index"
barchart_y = "prob"
barchart_title = "Literal Automaton Distribution"

initial_barchart = px.bar(df, x=barchart_x, y=barchart_y, title=barchart_title)

app = Dash()
app.layout = [
    html.Div(children='Assignment 4'),
    dcc.Graph(id="barchart", figure=initial_barchart),
    dcc.Slider(id="s-slider", min=1, max=25, step=1, value=1),
    dcc.Slider(id="P_L_Y-slider", min=0, max=1, step=0.1, value=0.5),
    dcc.Slider(id="P_Y-slider", min=0, max=1, step=0.1, value=0.5),
    dcc.Slider(id="P_nL_nY-slider", min=0, max=1, step=0.1, value=0.5)
]

@callback(
    Output("barchart", "figure"),
    [Input("s-slider", "value"),
     Input("P_L_Y-slider", "value"),
     Input("P_Y-slider", "value"),
     Input("P_nL_nY-slider", "value")]
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
        P_Y ** 0 * P_L_Y ** 1 * P_nL_Y ** 2 * s ** 5 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 5,
        P_Y ** 0 * P_L_Y ** 2 * P_nL_Y ** 1 * s ** 6 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 6,
        P_Y ** 0 * P_L_Y ** 3 * P_nL_Y ** 0 * s ** 7 * (P_L_Y * P_Y + P_nL_nY * P_nY) ** 7
    ]

    alfa = 1 / sum(probs)
    probs = [alfa * prob for prob in probs]

    updated_data = pi_automatas
    updated_data["prob"] = probs
    updated_df = pd.DataFrame(data=updated_data)

    updated_barchart = px.bar(updated_df, x=barchart_x, y=barchart_y, title=barchart_title)

    return updated_barchart

if __name__ == '__main__':
    app.run(debug=True)

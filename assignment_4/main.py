from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import pandas as pd

s = 0
P_L_Y = 0
P_Y = 0
P_nL_nY = 0

pi_automatas = {"index": ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6", "pi7", "pi8"],
                "prob": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]}
df = pd.DataFrame(data=pi_automatas)

app = Dash()
app.layout = [
    html.Div(children='Assignment 4'),
    dcc.Graph(id="barchart", figure=px.bar(df, x="index", y="prob", title="Literal Automaton Distribution")),
    dcc.Slider(id="test-slider", min=1, max=25, step=1, value=1),
    html.Div(id="slider-container")
]

@callback(
    Output("barchart", "figure"),
    Input("test-slider", "value")
)
def update_charts(value):
    new_automatas = {"index": ["pi1", "pi2", "pi3", "pi4", "pi5", "pi6", "pi7", "pi8"],
                "prob": [value, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]}

    new_df = pd.DataFrame(data=new_automatas)

    return px.bar(new_df, x="index", y="prob", title="Literal Automaton Distribution")

if __name__ == '__main__':
    app.run(debug=True)

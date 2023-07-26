import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("tweets.csv")
df["name"] = pd.Series(df["name"]).str.lower()
df["date_time"] = pd.to_datetime(df["date_time"], format='mixed')
df = (
    df.groupby([df["date_time"].dt.date, "name"])[
        ["number_of_likes", "number_of_shares"]
    ]
    .mean()
    .astype(int)
)
df = df.reset_index()

fig = px.line(data_frame=df, x="date_time", y="number_of_likes", color="name", log_y=True)

stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=stylesheets)
app.layout = html.Div([html.Div(html.H1("Twitter Likes Analysis of Famous People",
                                        style={"textAlign": "center"}),
                                className="row"),
                       html.Div(dcc.Graph(id="line-chart", figure=fig), className="row"),
                       html.Div([
                           html.Div(dcc.Dropdown(id="my-dropdown", multi=True,
                                                 options=[{"label": x, "value": x}
                                                          for x in sorted(df["name"].unique())],
                                                 value=["taylorswift13", "cristiano", "jtimberlake"],
                                                 style={"color": "green"}), className="four columns"),
                           html.Div(dcc.Dropdown(), className="four columns"),
                           html.Div(dcc.Dropdown(id="my-second-dropdown", multi=True,
                                                 options=[{"label": "Taylor", "value": "taylorswift13"},
                                                          {"label": "Ronaldo", "value": "cristiano"}],
                                                 style={"color": "green"}), className="four columns"),
                       ], className='row'), html.Div(html.A(id="my_link", children="Click her to visit linceAI",
                                                            href="https://linceai.com", target="_blank",
                                                            style={"color": "red", "backgroundColor": "yellow",
                                                                   "fontSize": "40px"}),
                                                     className="row")])


@app.callback(Output(component_id="line-chart", component_property="figure"),
              [Input(component_id="my-dropdown", component_property="value")])
def update_graph(chosen_values):
    print(f"Values chosen by user: {chosen_values}")

    if len(chosen_values) == 0:
        return {}
    else:
        df_filtered = df[df["name"].isin(chosen_values)]
        fig = px.line(
            data_frame=df_filtered,
            x="date_time",
            y="number_of_likes",
            color="name",
            log_y=True,
            labels={
                "number_of_likes": "Likes",
                "date_time": "Date",
                "name": "Celebrity",
            },
        )
        return fig


if __name__ == "__main__":
    app.run_server(debug=True)

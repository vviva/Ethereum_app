from etherscan import Etherscan
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd


def get_data(startblock, endblock):
    uniq_address_count = {}
    if startblock is not None and endblock is not None:
        for block_num in range(startblock, endblock):
            block = eth.get_proxy_block_by_number(hex(block_num))
            txs = block['transactions']
            uniq_address = []
            for tx in txs:
                if tx['from'] not in uniq_address:
                    uniq_address.append(tx['from'])
            uniq_address_count[block_num] = len(uniq_address)
            print(f"Fetched block {block_num}")

    df = pd.DataFrame(data=uniq_address_count.items(), columns=['Block_Num', 'Uniq_Address_Count'])

    return df


eth = Etherscan("XURIZCRG4V3ZUKAK8FIVBT8SHC65F8CPYN")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Unique Address by Block'),
    "StartBlock: ",
    dcc.Input(id='startblock', type='number'),
    "EndBlock: ",
    dcc.Input(id='endblock', type='number'),
    html.Button('Run', id='run', n_clicks=0),
    dcc.Graph(id='fig'),
], )


@app.callback(
    Output('fig', 'figure'),
    State('startblock', 'value'),
    State('endblock', 'value'),
    Input('run', 'n_clicks'),
    prevent_initial_call = True
)
def update_graph(startblock, endblock, n_clicks):
    data = get_data(startblock, endblock+1)
    fig = px.line(data, x="Block_Num", y="Uniq_Address_Count")
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)

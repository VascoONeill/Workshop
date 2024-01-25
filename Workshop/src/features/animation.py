import plotly.graph_objects as go
from plotly.subplots import make_subplots


def graphic(dataframe):

    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scatter'}]])

    # linha inicial ao gráfico
    trace1 = go.Scatter(x=dataframe.index[:150], y=dataframe[0][:150], mode='lines', line_color='white',
                        line_width=1, name='ECG Signal')

    trace2 = go.Scatter(x=dataframe.index[:150], y=dataframe[0][:150], mode='lines', line_color='limegreen',
                        opacity=0.5, line_width=5, name='ECG Signal')

    trace3 = go.Scatter(x=dataframe.index[:150], y=dataframe[0][:150], mode='lines', line_color='black',
                        opacity=0.0001, line_width=0.1, name='ECG Signal')

    trace_point = go.Scatter(x=dataframe[149:150], y=dataframe[0][149:150], mode='markers',
                             marker=dict(color='limegreen', size=10), name='Moving Point')

    fig.add_traces([trace1, trace2, trace3, trace_point])

    # botão de play
    frames = [go.Frame(data=[go.Scatter(x=dataframe.index[i-150:i + 10], y=dataframe[0][i-150:i + 10], mode='lines'),
                             go.Scatter(x=dataframe.index[i-150:i + 10], y=dataframe[0][i-150:i + 10], mode='lines'),
                             go.Scatter(x=dataframe.index[i-150:i + 150], y=dataframe[0][i-150:i + 150], mode='lines'),
                             go.Scatter(x=dataframe.index[i+9:i+10], y=dataframe[0][i+9:i+10], mode='markers')],
                       name=f'frame_{i + 5}') for i in range(500, len(dataframe), 5)]

    fig.frames = frames

    # layout
    fig.update_layout(updatemenus=[dict(type='buttons',
                                        showactive=False,
                                        buttons=[dict(label='Play',
                                                      method='animate',
                                                      args=[None, dict(frame=dict(duration=120, redraw=True),
                                                                       fromcurrent=True)])])], plot_bgcolor="black")

    # layout do eixos
    fig.update_xaxes(title_text='Time')
    fig.update_yaxes(title_text='ECG Signal')

    # gráfico
    fig.show()

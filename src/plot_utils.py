import plotly.graph_objects as go
import numpy as np


def plot_val_arousal(val, arousal):
    # Create a layout with visible axes centered at (0, 0)
    annot_kwargs = dict(showarrow=False, bgcolor="white")
    layout = go.Layout(
        xaxis=dict(
            range=[-1.2, 1.2],
            zeroline=True,
            zerolinewidth=2,
            showgrid=True,
            gridcolor='grey',
            zerolinecolor='black'
        ),
        yaxis=dict(
            range=[-1.2, 1.2],
            zeroline=True,
            zerolinewidth=2,
            showgrid=True,
            gridcolor='grey',
            zerolinecolor='black'
        ),
        plot_bgcolor="white",
        width=800,
        height=800,
        title='Valence-Arousal Plot',
        showlegend=False,
        annotations=[
            dict(x=-1, y=0, text="Negative", font={"color": "red", "size": 16}, **annot_kwargs),
            dict(x=1, y=0, text="Positive", font={"color": "green", "size": 16}, **annot_kwargs),
            dict(x=0, y=0, text="Neutral", font={"size": 16}, **annot_kwargs),
            dict(x=0.9, y=0.2, text="Happy", font={"size": 16}, **annot_kwargs),
            dict(x=0.4, y=0.9, text="Surprise", font={"size": 16}, **annot_kwargs),
            dict(x=-0.2, y=0.9, text="Fear", font={"size": 16}, **annot_kwargs),
            dict(x=-0.9, y=0.4, text="Disgust", font={"size": 16}, **annot_kwargs),
            dict(x=-0.8, y=0.6, text="Contempt", font={"size": 16}, **annot_kwargs),
            dict(x=-0.6, y=0.8, text="Anger", font={"size": 16}, **annot_kwargs),
            dict(x=-0.9, y=-0.4, text="Sad", font={"size": 16}, **annot_kwargs),
            dict(x=0, y=1.1, text="Excited", font={"color": "orange", "size": 16}, **annot_kwargs),
            dict(x=0, y=-1.1, text="Calm", font={"color": "blue", "size": 16}, **annot_kwargs)
        ]
    )

    # Create a trace for the unit circle
    theta = np.linspace(0, 2 * np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)

    unit_circle = go.Scatter(
        x=x_circle,
        y=y_circle,
        mode='lines',
        line=dict(
            color='black',
            width=2,
        ),
        showlegend=False,
    )

    point = go.Scatter(
        x=[val],
        y=[arousal],
        name="Emotion",
        mode='markers',
        marker=dict(color="red", size=16)
    )

    theta = np.linspace(0, 2 * np.pi, 100)
    x_circle = np.cos(theta)
    y_circle = np.sin(theta)

    circle = go.Scatter(
        x=x_circle,
        y=y_circle,
        mode='lines',
        line=dict(
            color='black',
            width=2,
        ),
        showlegend=False,
    )

    fig = go.Figure(data=[point, circle],
                    layout=layout,
                    )
    fig.show()

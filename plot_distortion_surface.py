import plotly.graph_objects as go
import json

file_path = "/path/to/file/here.json"
with open(file_path, 'r') as file:
    file_content = file.read()
measure_data = json.loads(file_content)

pfreq = []
plevel = []
pthd = []

distortion_to_plot = 'thdPlusN' # Valid values are thdPlusN, H# e.x. H2

graph_levels = []
for freq, levels in measure_data.items():
    # don't plot frequencies outside this range
    if(float(freq) < 20 or float(freq) > 10000):
        continue
    pfreq.append(float(freq))
    this_level = []
    for level, thd in levels.items():
        if float(level) not in plevel:
            plevel.append(float(level))
        if distortion_to_plot in thd:
            this_level.append(float(thd.get(distortion_to_plot)))
        else:
            this_level.append(None)
    graph_levels.append(this_level)


fig = go.Figure(data=[go.Surface(name="THD+N", z=graph_levels, x=plevel, y=pfreq,
                                 colorscale='Rainbow')])

fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                  highlightcolor="limegreen", project_z=True))

fig.update_layout(
    scene=dict(
        yaxis=dict(
            dtick=1, 
            type='log',
            title=dict(
                text='Frequency (y)'
            )
        ),
        xaxis=dict(
            title=dict(
                text='dBu (x)'
            )
        ),
        zaxis=dict(
            range=[-150, -60],
            title=dict(
                text='THD+N (z)'
            )
        )
    )
)

fig.layout.scene.aspectratio = {'x':1, 'y':1, 'z':1}
fig.update_layout(title=dict(text='Distortion Surface'))
fig.show()
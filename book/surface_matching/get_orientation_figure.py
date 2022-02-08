import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import trimesh  # <- conda install -c conda-forge scikit-image shapely rtree pyembree / pip install trimesh[all]
import numpy as np  # <- conda install -c anaconda numpy
from stl import mesh  # <- conda install -c conda-forge numpy-stl
from scipy import optimize  # <- conda install -c anaconda scipy
import plotly.graph_objects as go  # <- conda install -c plotly plotly
import pandas as pd  # <- conda install -c anaconda pandas
from skimage import io
from plotly.subplots import make_subplots

# import gbu  # <- python -m pip install git+https://github.com/elmokulc/GBU_pose_classifier.git


def stl2mesh3d(stl_mesh):
    # stl_mesh is read by nympy-stl from a stl file; it is  an array of faces/triangles (i.e. three 3d points)
    # this function extracts the unique vertices and the lists I, J, K to define a Plotly mesh3d
    p, q, r = stl_mesh.vectors.shape  # (p, 3, 3)
    # the array stl_mesh.vectors.reshape(p*q, r) can contain multiple copies of the same vertex;
    # extract unique vertices from all mesh triangles
    vertices, ixr = np.unique(
        stl_mesh.vectors.reshape(p * q, r), return_inverse=True, axis=0
    )
    I = np.take(ixr, [3 * k for k in range(p)])
    J = np.take(ixr, [3 * k + 1 for k in range(p)])
    K = np.take(ixr, [3 * k + 2 for k in range(p)])
    return vertices, I, J, K


def create_mesh3D(
    stl_file="scapula.stl",
    title="Mesh3d from a STL file<br>AT&T building",
    colorscale=None,
    return_mesh=False,
):

    if colorscale is None:
        colorscale = [[0, "#e5dee5"], [1, "#e5dee5"]]
    vertices, I, J, K = stl2mesh3d(mesh.Mesh.from_file(stl_file))
    x, y, z = vertices.T
    mesh3D = go.Mesh3d(
        x=x,
        y=y,
        z=z,
        i=I,
        j=J,
        k=K,
        flatshading=True,
        colorscale=colorscale,
        intensity=z,
        name="AT&T",
        showscale=False,
    )

    layout = go.Layout(
        paper_bgcolor="rgb(1,1,1)",
        title_text=title,
        title_x=0.5,
        font_color="white",
        width=800,
        height=800,
        scene_camera=dict(eye=dict(x=1.25, y=-1.25, z=1)),
        scene_xaxis_visible=False,
        scene_yaxis_visible=False,
        scene_zaxis_visible=False,
    )
    fig = go.Figure(data=[mesh3D], layout=layout)

    lighting_effects = dict(
        ambient=0.4,
        diffuse=1,
        roughness=0.1,
        specular=1,
        fresnel=0.1,
        facenormalsepsilon=0,
    )
    fig.data[0].update(lighting=lighting_effects)
    norm_light = 3000
    light_vec = np.array([1, 1, 1]) * norm_light
    fig.data[0].update(
        lightposition=dict(x=light_vec[0], y=light_vec[1], z=light_vec[2])
    )

    if return_mesh:
        return fig, mesh3D
    else:
        return fig


def add_points(points, fig, name, scale=1e3, return_sct=False, *args, **kwargs):
    sct = go.Scatter3d(
        x=np.concatenate([points, points]).reshape(-1, 3)[:, 0] * scale,
        y=np.concatenate([points, points]).reshape(-1, 3)[:, 1] * scale,
        z=np.concatenate([points, points]).reshape(-1, 3)[:, 2] * scale,
        name=name,
        mode="markers",
        **kwargs
    )
    fig.add_trace(sct)
    if return_sct:
        return fig, sct
    else:
        return fig


fig = create_mesh3D(stl_file="scapula.stl", title="Scapula Left <br> stl file")

# # Default parameters which are used when `layout.scene.camera` is not provided
camera = dict(
    up=dict(x=0, y=0, z=1), center=dict(x=0, y=0, z=0), eye=dict(x=1.25, y=1.25, z=1.25)
)

# fig.update_layout(
#     scene_camera=camera,
#     autosize=False,
#     width=400,
#     height=400,
# )
# # df_scan = pd.read_pickle("data_scan.p")
# # cols = set([cols[0] for cols in df_scan.columns])
# # fig = go.Figure()
# # for i, c in enumerate(cols):
# #     fig.add_trace(
# #         go.Scatter3d(
# #             x=df_scan[c].p3d.x,
# #             y=df_scan[c].p3d.y,
# #             z=df_scan[c].p3d.z,
# #             name=c,
# #             marker_size=2,
# #             mode="markers",
# #         )
# #     )


p_glene_stl = np.array([0.02515289854664963, 0.03122873596800735, 0.036798809060995745])
p_coracoide_stl = np.array(
    [0.026787610816186087, 0.05609095153197788, -0.0043762069034760384]
)
p_acromion_stl = np.array(
    [-0.008420164259823573, 0.07140986464971243, 0.018059532550748165]
)

_, mesh_scp = create_mesh3D(
    stl_file="scapula.stl", title="Scapula Left <br> stl file", return_mesh=True
)
_, sct_g = add_points(points=p_glene_stl, fig=fig, name="glène", return_sct=True)
_, sct_c = add_points(
    points=p_coracoide_stl, fig=fig, name="coracoide", return_sct=True
)
_, sct_a = add_points(points=p_acromion_stl, fig=fig, name="acromion", return_sct=True)


img = io.imread("./scapula.jpg")
py_img = go.Image(z=img)

fig = make_subplots(rows=1, cols=2, specs=[[{"type": "scene"}, {"type": "xy"}]])
fig.add_trace(mesh_scp, row=1, col=1)
fig.add_trace(sct_g, row=1, col=1)
fig.add_trace(sct_c, row=1, col=1)
fig.add_trace(sct_a, row=1, col=1)

fig.add_trace(py_img, row=1, col=2)

fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))

fig.update_layout(
    scene_camera=camera,
    autosize=False,
    width=1000,
    height=1000,
)

layout = go.Layout(
    paper_bgcolor="rgb(1,1,1)",
    title_x=0.5,
    font_color="white",
    scene_xaxis_visible=False,
    scene_yaxis_visible=False,
    scene_zaxis_visible=False,
)
fig.update_layout(layout)
lighting_effects = dict(
    ambient=0.4,
    diffuse=1,
    roughness=0.1,
    specular=1,
    fresnel=0.1,
    facenormalsepsilon=0,
)
fig.data[0].update(lighting=lighting_effects)
norm_light = 3000
light_vec = np.array([1, 1, 1]) * norm_light
fig.data[0].update(lightposition=dict(x=light_vec[0], y=light_vec[1], z=light_vec[2]))


app = dash.Dash()
app.layout = html.Div(
    [
        html.Div(id="output"),  # use to print current relayout values
        dcc.Graph(id="fig", figure=fig),
    ]
)


@app.callback(Output("output", "children"), Input("fig", "relayoutData"))
def show_data(data):
    # show camera settings like eye upon change
    return [str(data)]


app.run_server(debug=False, use_reloader=False)

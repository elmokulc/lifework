import gbu
import numpy as np
import pandas as pd
import image_datasets as imsets
from cv2 import aruco


def get_stylus_points(data_dir, compo_scapula, compo_stylet):

    metadata = imsets.core.MetaData(path=data_dir)
    image_directory = metadata.image_directory
    camera_matrix = metadata.camera_matrix
    distortion_coefficients = metadata.distortion_coefficients
    marker_dimension = metadata.marker_dimension
    # Aruco settings
    parameters = aruco.DetectorParameters_create()
    parameters.cornerRefinementMethod = 3
    parameters.cornerRefinementWinSize = 5
    parameters.cornerRefinementMaxIterations = 100

    batch = gbu.calibration.ImageBatchCompositePose(
        composites={"scapula": compo_scapula, "stylet": compo_stylet},
        directory=image_directory,
        aruco_dict=aruco.DICT_6X6_250,
        parameters=parameters,
        marker_dimension=marker_dimension,
        output_directory=image_directory + "/_outputs/",
        camera_matrix=camera_matrix,
        distortion_coefficients=distortion_coefficients,
    )

    rvecs, tvecs = batch.change_reference_frame(cid_in="stylet", cid_out="scapula")

    return tvecs


compo_stylet = gbu.core.load_composite("composite_stylet.json")
compo_scapula = gbu.core.load_composite("composite_scapula.json")

# Get ref point glène
p_glene_scapula = get_stylus_points(
    data_dir="data/surface_matching/dataset1",
    compo_scapula=compo_scapula,
    compo_stylet=compo_stylet,
)

p_acromion_scapula = get_stylus_points(
    data_dir="data/surface_matching/dataset2",
    compo_scapula=compo_scapula,
    compo_stylet=compo_stylet,
)

p_coracoide_scapula = get_stylus_points(
    data_dir="data/surface_matching/dataset3",
    compo_scapula=compo_scapula,
    compo_stylet=compo_stylet,
)

p_scan_scapula = get_stylus_points(
    data_dir="data/surface_matching/dataset4",
    compo_scapula=compo_scapula,
    compo_stylet=compo_stylet,
)

data_points = {
    "p_glene_scapula": p_glene_scapula,
    "p_acromion_scapula": p_acromion_scapula,
    "p_coracoide_scapula": p_coracoide_scapula,
    "p_scan_scapula": p_scan_scapula,
}


def dt(points, key):
    sdic = {key: {"x": [], "z": [], "y": []}}
    for p in points:
        sdic[key]["x"].append(p[0])
        sdic[key]["y"].append(p[1])
        sdic[key]["z"].append(p[2])
    return sdic


pp = []
cc = ["x", "y", "z"]
for key in data_points.keys():
    for c in cc:
        pp.append((key, "p3d", c))

cols = pd.MultiIndex.from_tuples(pp)
df = pd.DataFrame(columns=cols)
for key, value in data_points.items():
    for ii in range(len(value)):
        for i in range(3):
            df.at[ii, (key, "p3d", "xyz"[i])] = value[ii, i]

df.to_pickle("data_scan.p")

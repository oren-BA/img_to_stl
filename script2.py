import numpy as np
import imageio
from scipy import ndimage, misc
import trimesh

def create_mesh(image_data, model_height):
    nx, ny = image_data.shape
    vertices = np.zeros((nx, ny, 3))
    for x in range(0, nx):
        for y in range(0, ny):
            height = model_height if image_data[x, y] >= 0.5 else 0.0
            vertices[x, y] = [16.0 * x / nx, 64.0 * y / ny, height]

    faces = []
    for x in range(0, nx - 1):
        for y in range(0, ny - 1):
            vertice1 = vertices[x, y]
            vertice2 = vertices[x + 1, y]
            vertice3 = vertices[x + 1, y + 1]
            face1 = np.array([vertice1, vertice2, vertice3])
            face2 = np.array([vertice1, vertice3, vertice2])
            faces.append(face1)
            faces.append(face2)
    return np.array(faces)

image = imageio.imread('spotify_code.jpg', mode='L')
image = misc.imresize(image, (160, 640), interp='bilinear', mode='F')
image_data = image / 255.0
model_height = 1.0
faces = create_mesh(image_data, model_height)
vertices = faces.reshape(-1, 3)
faces = np.arange(vertices.shape[0]).reshape(-1, 3)  # Ensure correct shape for faces
tri_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
tri_mesh.export('output2.stl')

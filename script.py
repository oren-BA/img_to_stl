import numpy as np
from PIL import Image
from stl import mesh


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
            vertice1 = vertices[x, y]
            vertice2 = vertices[x + 1, y + 1]
            vertice3 = vertices[x + 1, y]
            face2 = np.array([vertice1, vertice2, vertice3])
            faces.append(face1)
            faces.append(face2)
    return np.array(faces)

image = Image.open('spotify_code.jpg').convert('L')
# image = image.resize((160, 640), resample=Image.BILINEAR)
image_data = np.array(image)/255.0
model_height = 1.0
faces = create_mesh(image_data,model_height)
surface = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        surface.vectors[i][j] = f[j]

surface.save('output.stl')

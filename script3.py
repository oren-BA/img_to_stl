import numpy as np
from PIL import Image
from stl import mesh
from sklearn.cluster import KMeans


def simplify_mesh(vertices, faces, target_vertex_count):
    n_vertices = vertices.shape[0]
    if n_vertices <= target_vertex_count:
        return vertices, faces

    # Apply K-means clustering to find representative vertices
    kmeans = KMeans(n_clusters=target_vertex_count, random_state=42)
    kmeans.fit(vertices)
    simplified_vertices = kmeans.cluster_centers_

    # Update face indices to match the simplified vertices
    vertex_map = {tuple(v): i for i, v in enumerate(simplified_vertices)}
    simplified_faces = []
    for face in faces:
        simplified_face = [vertex_map[tuple(v)] for v in face]
        simplified_faces.append(simplified_face)

    return simplified_vertices, np.array(simplified_faces)


def create_mesh(image_data, model_height, target_vertex_count):
    nx, ny = image_data.shape
    vertices = np.zeros((nx, ny, 3))
    for x in range(nx):
        for y in range(ny):
            height = model_height if image_data[x, y] >= 0.5 else 0.0
            vertices[x, y] = [16.0 * x / nx, 64.0 * y / ny, height]

    faces = []
    for x in range(nx - 1):
        for y in range(ny - 1):
            vertice1 = vertices[x, y]
            vertice2 = vertices[x + 1, y]
            vertice3 = vertices[x + 1, y + 1]
            face1 = np.array([vertice1, vertice2, vertice3])
            vertice1 = vertices[x, y]
            vertice2 = vertices[x + 1, y + 1]
            vertice3 = vertices[x, y + 1]
            face2 = np.array([vertice1, vertice2, vertice3])
            faces.append(face1)
            faces.append(face2)

    faces = np.array(faces)
    vertices, faces = simplify_mesh(vertices.reshape(-1, 3), faces, target_vertex_count)
    return vertices, faces


image = Image.open('spotify_code.jpg').convert('L')
image = image.resize((480, 1920), Image.ANTIALIAS)
image_data = np.array(image) / 255.0
model_height = 1.0
target_vertex_count = 10000  # Adjust this value as desired

vertices, faces = create_mesh(image_data, model_height, target_vertex_count)
surface = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        surface.vectors[i][j] = vertices[f[j]]

surface.save('output_final2.stl')


import numpy as np
from PIL import Image
from stl import mesh



def create_3d_model(image_path, output_path):
    # Open the image and convert it to grayscale
    image = Image.open(image_path).convert("L")

    # Get the image dimensions
    width, height = image.size

    # Create a 3D array to represent the model
    depth = 10  # Depth for white pixels (in mm)
    model = np.zeros((height, width, depth))

    # Iterate over each pixel in the image
    for y in range(height):
        for x in range(width):
            # Check if the pixel is white
            if image.getpixel((x, y)) == 255:
                # Assign the depth value to white pixels
                model[y, x, :depth] = 1

    # Create the STL mesh object
    stl_mesh = mesh.Mesh(np.zeros(int(model.sum()), dtype=mesh.Mesh.dtype))
    index = 0

    # Iterate over each voxel in the 3D model
    for z in range(depth):
        for y in range(height):
            for x in range(width):
                # Check if the voxel has depth
                if model[y, x, z] == 1:
                    # Assign the vertices for each voxel
                    stl_mesh.vectors[index] = [
                        (x, y, z),
                        (x + 1, y, z),
                        (x, y + 1, z)
                    ]
                    stl_mesh.vectors[index + 1] = [
                        (x + 1, y, z),
                        (x + 1, y + 1, z),
                        (x, y + 1, z)
                    ]
                    index += 2
                if index >= 131500:
                    break

    # Save the STL mesh to a file
    stl_mesh.save(output_path)

if __name__ == '__main__':
    create_3d_model('spotify_code.jpg', 'output_model.stl')

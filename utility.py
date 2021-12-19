import numpy as np
from numpy.random import default_rng

def Vec3(x, y, z):
    return np.array([x, y, z], dtype=np.float64)

def Color(r, g, b):
    return Vec3(r, g, b)

def Point3(u, v, w):
    return Vec3(u, v, w)

def unit_vector(vec):
	return vec / np.linalg.norm(vec)

def format_color(pixel_color, samples_per_pixel):
    # Divide the color by the number of samples.
    scaled_pixel_color = pixel_color / samples_per_pixel

    # Write the translated [0,255] value of each color component.
    return 256 * np.clip(scaled_pixel_color, 0.0, 0.999)

X = R = 0
Y = G = 1
Z = B = 2
rng = default_rng()
import numpy as np

def Vec3(x, y, z):
    return np.array([x, y, z])

def Color(r, g, b):
    return Vec3(r, g, b)

def Point3(u, v, w):
    return Vec3(u, v, w)

def unit_vector(vec):
	return vec / np.linalg.norm(vec)

def format_color(color):
	return np.trunc(255.999 * color)

X = 0
Y = 1
Z = 2
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

def near_zero(vec):
	return np.allclose(vec, np.zeros(3))

def reflect(v, n):
	return v - 2*np.dot(v,n)*n

def random_in_unit_sphere():
	while True:
		p = rng.uniform(-1.0, 1.0, 3)
		if np.dot(p, p) >= 1:
			continue
		return p

def random_unit_vector():
	return unit_vector(random_in_unit_sphere())

def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    if np.dot(in_unit_sphere, normal) > 0.0: # In the same hemisphere as the normal
        return in_unit_sphere
    else:
        return -in_unit_sphere

def format_color(pixel_color, samples_per_pixel):
	# Divide the color by the number of samples and gamma-correct for gamma=2.0.
	scaled_pixel_color = np.sqrt(pixel_color / samples_per_pixel)

	# Write the translated [0,255] value of each color component.
	return 256 * np.clip(scaled_pixel_color, 0.0, 0.999)

X = R = 0
Y = G = 1
Z = B = 2
rng = default_rng()
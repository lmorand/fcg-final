import numpy as np
from ray import Ray
from utility import *

class Camera:

	def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio):
		theta = np.deg2rad(vfov)
		h = np.tan(theta/2)
		viewport_height = 2.0 * h
		viewport_width = aspect_ratio * viewport_height
		focal_length = 1.0

		w = unit_vector(lookfrom - lookat)
		u = unit_vector(np.cross(vup, w))
		v = np.cross(w, u)

		self.origin = lookfrom
		self.horizontal = viewport_width * u
		self.vertical = viewport_height * v
		self.lower_left_corner = self.origin - self.horizontal/2 - self.vertical/2 - w
	
	def get_ray(self, s, t):
		return Ray(self.origin, self.lower_left_corner + s*self.horizontal + t*self.vertical - self.origin)
import numpy as np
from hittable import Hittable

class Sphere(Hittable):

	def __init__(self, center, radius, material):
		self.center = center
		self.radius = radius
		self.material = material

	def hit(self, r, t_min, t_max):
		def get_face_normal():
			outward_normal = (p - self.center) / self.radius
			front_face = np.dot(r.direction(), outward_normal) < 0
			normal = outward_normal if front_face else -outward_normal
			return normal, front_face

		oc = r.origin() - self.center
		a = np.dot(r.direction(), r.direction())
		half_b = np.dot(oc, r.direction())
		c = np.dot(oc, oc) - self.radius**2

		discriminant = half_b**2 - a*c
		if discriminant < 0:
			return None

		# Find the nearest root that lies in the acceptable range.
		sqrtd = np.sqrt(discriminant)
		root = (-half_b - sqrtd) / a
		if root < t_min or t_max < root:
			root = (-half_b + sqrtd) / a
			if root < t_min or t_max < root:
				return None

		t = root
		p = r.at(t)

		return t, p, *get_face_normal(), self.material
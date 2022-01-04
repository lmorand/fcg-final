from abc import ABC, abstractmethod
import numpy as np
from ray import Ray
from utility import *

class Material(ABC):

	@abstractmethod
	def scatter(self, r_in, hit_rec):
		pass

class Lambertian(Material):
	
	def __init__(self, albedo):
		self.albedo = albedo

	def scatter(self, r_in, hit_rec):
		p, normal = hit_rec[1:3]
		scatter_direction = normal + random_unit_vector()

		# Catch degenerate scatter direction
		if near_zero(scatter_direction):
			scatter_direction = normal

		scattered = Ray(p, scatter_direction)
		attenuation = self.albedo
		return scattered, attenuation

class Metal(Material):
	
	def __init__(self, albedo, fuzz):
		self.albedo = albedo
		self.fuzz = fuzz if fuzz < 1.0 else 1.0

	def scatter(self, r_in, hit_rec):
		p, normal = hit_rec[1:3]
		reflected = reflect(unit_vector(r_in.direction()), normal)
		scattered = Ray(p, reflected + self.fuzz*random_in_unit_sphere())
		attenuation = self.albedo

		if np.dot(scattered.direction(), normal) > 0:
			return scattered, attenuation
		else:
			return None
	
	# def reflect(self, v, n):
	# 	return v - 2*np.dot(v,n)*n

class Dielectric(Material):

	def __init__(self, index_of_refraction):
		self.ir = index_of_refraction

	def scatter(self, r_in, hit_rec):
		p, normal, front_face = hit_rec[1:4]
		refraction_ratio = (1.0/self.ir) if front_face else self.ir

		unit_direction = unit_vector(r_in.direction())
		cos_theta = min(np.dot(-unit_direction, normal), 1.0)
		sin_theta = np.sqrt(1.0 - cos_theta**2)

		cannot_refract = refraction_ratio * sin_theta > 1.0

		if (cannot_refract or self.reflectance(cos_theta, refraction_ratio) > rng.random()):
			direction = reflect(unit_direction, normal)
		else:
			direction = refract(unit_direction, normal, refraction_ratio)

		scattered = Ray(p, direction)
		attenuation = Color(1.0, 1.0, 1.0)
		return scattered, attenuation
	
	def reflectance(self, cosine, ref_idx):
		# Use Schlick's approximation for reflectance.
		r0 = (1-ref_idx) / (1+ref_idx)
		r0 = r0**2
		return r0 + (1-r0)*(1 - cosine)**5
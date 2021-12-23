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
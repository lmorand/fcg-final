import numpy as np
from utility import *
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
from material import *

def materials(aspect_ratio):
	world = HittableList()

	material_ground = Lambertian(Color(0.8, 0.8, 0.0))
	material_center = Lambertian(Color(0.1, 0.2, 0.5))
	material_left   = Dielectric(1.5)
	material_right  = Metal(Color(0.8, 0.6, 0.2), 0.0)

	world.add(Sphere(Point3(0,0,-1), 0.5, material_center))
	world.add(Sphere(Point3(0,-100.5,-1), 100, material_ground))
	world.add(Sphere(Point3(-1.0,0.0,-1.0), 0.5, material_left))
	world.add(Sphere(Point3(-1.0,0.0,-1.0), -0.4, material_left))
	world.add(Sphere(Point3(1.0,0.0,-1.0), 0.5, material_right))

	lookfrom = Point3(0,0,0.5)
	lookat = Point3(0,0,-1)
	vup = Vec3(0,1,0)
	dist_to_focus = np.linalg.norm(lookfrom-lookat)
	aperture = 0.0

	cam = Camera(lookfrom, lookat, vup, 90, aspect_ratio, aperture, dist_to_focus)

	return world, cam

def depth_of_field(aspect_ratio):
	world = HittableList()

	material_ground = Lambertian(Color(0.8, 0.8, 0.0))
	material_center = Lambertian(Color(0.1, 0.2, 0.5))
	material_left   = Dielectric(1.5)
	material_right  = Metal(Color(0.8, 0.6, 0.2), 0.0)

	world.add(Sphere(Point3(0,0,-1), 0.5, material_center))
	world.add(Sphere(Point3(0,-100.5,-1), 100, material_ground))
	world.add(Sphere(Point3(-1.0,0.0,-1.0), 0.5, material_left))
	world.add(Sphere(Point3(-1.0,0.0,-1.0), -0.45, material_left))
	world.add(Sphere(Point3(1.0,0.0,-1.0), 0.5, material_right))

	lookfrom = Point3(3,3,2)
	lookat = Point3(0,0,-1)
	vup = Vec3(0,1,0)
	dist_to_focus = np.linalg.norm(lookfrom-lookat)
	aperture = 2.0

	cam = Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

	return world, cam

def random_scene(aspect_ratio):
	ground_material = Lambertian(Color(0.5, 0.5, 0.5))
	world = HittableList()
	world.add(Sphere(Point3(0,-1000,0), 1000, ground_material))

	for a in range(-11, 11):
		for b in range (-11, 11):
			choose_mat = rng.random()
			center = Point3(a + 0.9*rng.random(), 0.2, b + 0.9*rng.random())

			if np.linalg.norm(center - Point3(4, 0.2, 0)) > 0.9:
				if choose_mat < 0.8:
					# diffuse
					albedo = rng.random(3) * rng.random(3)
					sphere_material = Lambertian(albedo)
					world.add(Sphere(center, 0.2, sphere_material))
				elif choose_mat < 0.95:
					# metal
					albedo = rng.uniform(0.5, 1, 3)
					fuzz = rng.uniform(0, 0.5)
					sphere_material = Metal(albedo, fuzz)
					world.add(Sphere(center, 0.2, sphere_material))
				else:
					# glass
					sphere_material = Dielectric(1.5)
					world.add(Sphere(center, 0.2, sphere_material))

	material1 = Dielectric(1.5)
	world.add(Sphere(Point3(0, 1, 0), 1.0, material1))

	material2 = Lambertian(Color(0.4, 0.2, 0.1))
	world.add(Sphere(Point3(-4, 1, 0), 1.0, material2))

	material3 = Metal(Color(0.7, 0.6, 0.5), 0.0)
	world.add(Sphere(Point3(4, 1, 0), 1.0, material3))

	lookfrom = Point3(13,2,3)
	lookat = Point3(0,0,0)
	vup = Vec3(0,1,0)
	dist_to_focus = 10.0
	aperture = 0.1

	cam = Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)

	return world, cam
from multiprocessing import Pool
import numpy as np
from PIL import Image
from ray import Ray
from utility import *
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
from material import *

def ray_color(ray, world, depth):
	# If we've exceeded the ray bounce limit, no more light is gathered.
	if depth <= 0:
		return Color(0,0,0)

	hit_rec = world.hit(ray, 0.001, np.inf)
	if hit_rec is not None:
		material = hit_rec[4]
		scattered = material.scatter(ray, hit_rec)
		if scattered is not None:
			return scattered[1]*ray_color(scattered[0], world, depth-1)
		return Color(0, 0, 0)
	
	unit_direction = unit_vector(ray.direction())
	t = 0.5 * (unit_direction[Y] + 1.0)
	return (1.0-t)*Color(1.0, 1.0, 1.0) + t*Color(0.5, 0.7, 1.0)

def sample(i, j):
	u = i / (image_width-1)
	v = j / (image_height-1)
	r = cam.get_ray(u, v)
	return ray_color(r, world, max_depth)

def init_sampler(_image_width, _image_height, _cam, _world, _max_depth):
	global image_width
	global image_height
	global cam
	global world
	global max_depth
	
	image_width = _image_width
	image_height = _image_height
	cam = _cam
	world = _world
	max_depth = _max_depth

def random_scene():
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

	return world

if __name__ == "__main__":
	aspect_ratio = 16.0 / 9.0
	# aspect_ratio = 3.0 / 2.0
	image_width = 1280
	# image_width = 600
	image_height = round(image_width / aspect_ratio)
	samples_per_pixel = 1
	max_depth = 50

	world = random_scene()

	material_ground = Lambertian(Color(0.8, 0.8, 0.0))
	material_center = Lambertian(Color(0.1, 0.2, 0.5))
	material_left   = Dielectric(1.5)
	material_right  = Metal(Color(0.8, 0.6, 0.2), 0.0)

	# world.add(Sphere(Point3(0,0,-1), 0.5, material_center))
	# world.add(Sphere(Point3(0,-100.5,-1), 100, material_ground))
	# world.add(Sphere(Point3(-1.0,0.0,-1.0), 0.5, material_left))
	# world.add(Sphere(Point3(-1.0,0.0,-1.0), -0.45, material_left))
	# world.add(Sphere(Point3(1.0,0.0,-1.0), 0.5, material_right))

	lookfrom = Point3(13,2,3)
	lookat = Point3(0,0,0)
	vup = Vec3(0,1,0)
	dist_to_focus = 10.0
	aperture = 0.1

	cam = Camera(lookfrom, lookat, vup, 20, aspect_ratio, aperture, dist_to_focus)
	image = np.empty((image_height, image_width, 3), dtype=np.uint8)
	n_procs = 8
	step_j = -10
	step_i = 10

	with Pool(processes=n_procs, initializer=init_sampler, initargs=(image_width, image_height, cam, world, max_depth)) as pool:
		for j in range(image_height-1, -1, step_j):
			print(f'\rScanlines remaining: {j:4}', end='')
			limit_y = j + step_j
			if limit_y < -1: limit_y = -1
			indeces_y = range(j, limit_y, -1)
			for i in range(0, image_width, step_i):
				limit_x = i + step_i
				if limit_x > image_width: limit_x = image_width
				indeces_x = range(i, limit_x, 1)
				indeces = []
				for x in indeces_x:
					for y in indeces_y:
						indeces.append((x,y))
				sampled_colors = pool.starmap(sample, indeces, chunksize=12)
				for pixel_color, index in zip(sampled_colors, indeces):
					image[index] = format_color(pixel_color, samples_per_pixel)

	# image = np.array(image, dtype=np.uint8).reshape((image_height, image_width, 3))
	Image.fromarray(image, 'RGB').save('out.png')
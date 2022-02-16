from multiprocessing import Pool
import numpy as np
from PIL import Image
from ray import Ray
from utility import *
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera
from material import *
from examples import materials

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
	u = (i + rng.random()) / (image_width-1)
	v = (j + rng.random()) / (image_height-1)
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

if __name__ == "__main__":
	aspect_ratio = 16.0 / 9.0
	image_width = 400
	image_height = round(image_width / aspect_ratio)
	samples_per_pixel = 100
	max_depth = 50

	world, cam = materials(aspect_ratio)
	image = []
	n_procs = 8

	with Pool(processes=n_procs, initializer=init_sampler, initargs=(image_width, image_height, cam, world, max_depth)) as pool:
		for j in range(image_height-1, -1, -1):
			print(f'\rScanlines remaining: {j:3}', end='')
			for i in range(image_width):
				sampled_colors = pool.starmap(sample, [(i,j) for x in range(samples_per_pixel)], chunksize=12)
				pixel_color = sum(sampled_colors)
				image.append(format_color(pixel_color, samples_per_pixel))

	image = np.array(image, dtype=np.uint8).reshape((image_height, image_width, 3))
	Image.fromarray(image, 'RGB').save('out.png')
import numpy as np
from PIL import Image
from ray import Ray
from utility import *
from sphere import Sphere
from hittable_list import HittableList
from camera import Camera

def ray_color(ray, world, depth):
	# If we've exceeded the ray bounce limit, no more light is gathered.
	if depth <= 0:
		return Color(0,0,0)

	hit_rec = world.hit(ray, 0.001, np.inf)
	if hit_rec is not None:
		p, normal = hit_rec[1:3]
		target = p + normal + random_unit_vector()
		return 0.5*ray_color(Ray(p, target - p), world, depth-1)
	
	unit_direction = unit_vector(ray.direction())
	t = 0.5 * (unit_direction[Y] + 1.0)
	return (1.0-t)*Color(1.0, 1.0, 1.0) + t*Color(0.5, 0.7, 1.0)

aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = round(image_width / aspect_ratio)
samples_per_pixel = 100
max_depth = 5

world = HittableList()
world.add(Sphere(Point3(0,0,-1), 0.5))
world.add(Sphere(Point3(0,-100.5,-1), 100))

cam = Camera()
image = []

try:
	for j in range(image_height-1, -1, -1):
		print('\rScanlines remaining: ', j, end='')
		for i in range(image_width):
			pixel_color = Color(0, 0, 0)
			for s in range(samples_per_pixel):
				u = (i + rng.random()) / (image_width-1)
				v = (j + rng.random()) / (image_height-1)
				r = cam.get_ray(u, v)
				pixel_color += ray_color(r, world, max_depth)
			image.append(format_color(pixel_color, samples_per_pixel))

	image = np.array(image, dtype=np.uint8).reshape((image_height, image_width, 3))
	Image.fromarray(image, 'RGB').save('out.png')

except KeyboardInterrupt:
	image = np.array(image[:(image_height-j-1)*image_width], dtype=np.uint8).reshape((image_height-j-1, image_width, 3))
	Image.fromarray(image, 'RGB').save('partial_out.png')
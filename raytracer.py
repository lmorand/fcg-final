import numpy as np
from PIL import Image
from ray import Ray
from utility import *
from sphere import Sphere
from hittable_list import HittableList

def ray_color(ray, world):
	hit_rec = world.hit(ray, 0, np.inf)
	if hit_rec is not None:
		n = hit_rec[2]
		return 0.5*Color(*(n+1))
	
	unit_direction = unit_vector(ray.direction())
	t = 0.5 * (unit_direction[Y] + 1.0)
	return (1.0-t)*Color(1.0, 1.0, 1.0) + t*Color(0.5, 0.7, 1.0)

aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = round(image_width / aspect_ratio)

world = HittableList()
world.add(Sphere(Point3(0,0,-1), 0.5))
world.add(Sphere(Point3(0,-100.5,-1), 100))

viewport_height = 2.0
viewport_width = aspect_ratio * viewport_height
focal_length = 1.0

origin = Point3(0, 0, 0)
horizontal = Vec3(viewport_width, 0, 0)
vertical = Vec3(0, viewport_height, 0)
lower_left_corner = origin - horizontal/2 - vertical/2 - Vec3(0, 0, focal_length)

image = []

for j in range(image_height-1, -1, -1):
	# print('\rScanlines remaining: ', j)
	for i in range(image_width):
		u = i / (image_width-1)
		v = j / (image_height-1)
		r = Ray(origin, lower_left_corner + u*horizontal + v*vertical - origin)
		image.append(format_color(ray_color(r, world)))

image = np.array(image, dtype=np.uint8).reshape((image_height, image_width, 3))
Image.fromarray(image, 'RGB').save('out.png')
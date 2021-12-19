from hittable import Hittable

class HittableList(Hittable):

	def __init__(self):
		self.objects = []
	
	def clear(self):
		self.objects.clear()
	
	def add(self, object):
		self.objects.append(object)
	
	def hit(self, r, t_min, t_max):
		hit_anything = False
		closest_so_far = t_max

		for object in self.objects:
			temp_hit_record = object.hit(r, t_min, closest_so_far)
			if temp_hit_record is not None:
				hit_anything = True
				closest_so_far = temp_hit_record[0]
				hit_record = temp_hit_record

		return hit_record if hit_anything else None
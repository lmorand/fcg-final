from abc import ABC, abstractmethod

class Hittable(ABC):

	@abstractmethod
	def hit(r, t_min, t_max):
		pass
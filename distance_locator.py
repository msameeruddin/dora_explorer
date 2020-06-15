from india_data import india_dumped

class LocationHelper(object):
	def __init__(self):
		pass

	
	def _get_noded_places(self, place_list):
		"""
		Assign a node number for each place_name in the form dict
		:param place_list: list[string]
		:return: dict(int, string)
		"""
		place_dict = {
			i : j 
			for (i, j) in zip(
				range(1, len(place_list) + 1), place_list
			)
		}
		return place_dict


	def _get_noded_coords(self, place_list):
		"""
		Get the coordination values for each place
		:parma place_list: list[string]
		:return: dict(string, list[float])
		"""
		place_coords = {
			i : j
			for (i, j) in zip(
				place_list, [india_dumped[i] for i in place_list]
			)
		}
		return place_coords



class DistanceLocator(LocationHelper):
	def __init__(self, place_list):
		self.place_list = self._get_noded_places(place_list=place_list)

	
	def get_distance(self, from_, to_):
		"""
		Get the `haversine_distance` from `lat` and `lon`
		:param from_: string
		:param to_: string
		:return: float

		Examplesstring
		:return: float

		Examples
		--------
		>>> get_distance('munich', 'berlin')
		504.2
		"""
		from mpu import haversine_distance

		from_coords = india_dumped[from_]
		to_coords = india_dumped[to_]

		dist = haversine_distance(
			origin=from_coords, 
			destination=to_coords
		)
		dist = round(dist, 2)

		return dist

	
	def set_distance_matrix(self, num):
		"""
		Set the distance matrix showing the distance values from `a` to `b`
		:param num: int
		:return: dict[tuple[int], float]
		"""
		distance_matrix = {}

		for i in range(1, num + 1):
			for j in range(1, num + 1):
				from_= self.place_list[i]
				to_ = self.place_list[j]
				distance_matrix[(i, j)] = self.get_distance(from_=from_, to_=to_)

		return distance_matrix





if __name__ == '__main__':
	# place_list = {
	# 	1 : 'Red Fort', 
	# 	2 : 'Pink City', 
	# 	3 : 'Goa', 
	# 	4 : 'Hawa Mahal'
	# }

	# place_coords = {
	# 	'Red Fort' : [28.6562, 77.2410],
	# 	'Pink City' : [26.9124, 75.7873],
	# 	'Goa' : [15.2993, 74.1240],
	# 	'Hawa Mahal' : [26.9239, 75.8267]
	# }

	place_list = ['Punch', 'Zunheboto', 'Zaidpur']

	dl = DistanceLocator(
		place_list=place_list
	)

	print(dl.set_distance_matrix(len(place_list)))

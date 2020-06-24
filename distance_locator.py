from india_data import india_dumped

class LocationHelper(object):
	def __init__(self):
		pass

	
	def _get_noded_places(self, place_list):
		"""
		Assign a node number for each place_name in the form dict
		:param list place_list: Consists of city names
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
		:parma list place_list: Consists of city names
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
	def __init__(self):
		pass

	
	def get_distance(self, from_, to_):
		"""
		Get the `haversine_distance` from `lat` and `lon`
		:param string from_: from place
		:param string to_: to place
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

	
	def set_distance_matrix(self, place_list):
		"""
		Set the distance matrix showing the distance values from `a` to `b`
		:param  dict place_list: dict of places - {1 : 'place_name', 2 : 'place_name' ...}
		:return: dict[tuple[int], float]
		"""
		distance_matrix = {}
		for i in range(1, len(place_list) + 1):
			for j in range(1, len(place_list) + 1):
				from_= place_list[i]
				to_ = place_list[j]
				distance_matrix[(i, j)] = self.get_distance(from_=from_, to_=to_)

		return distance_matrix





if __name__ == '__main__':

	place_list = ['Punch', 'Zunheboto', 'Zaidpur']

	dl = DistanceLocator()

	print(dl.set_distance_matrix(dl._get_noded_places(place_list)))
	print(dl.get_distance('Bengaluru', 'Mumbai'))

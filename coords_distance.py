
class DistanceLocator(object):
	def __init__(self, place_list, place_coords):
		self.place_list = place_list
		self.place_coords = place_coords

	def get_distance(self, from_, to_):
		import mpu
		"""
		return float/int formatted distance calculated by taking
		`from_` coordinates and `to_` coordinates
		"""
		from_coords = self.place_coords[from_]
		to_coords = self.place_coords[to_]

		dist = mpu.haversine_distance(
			origin=from_coords, 
			destination=to_coords
		)
		dist = round(dist, 2)

		return dist

	def set_distance_matrix(self, num):
		distance_matrix = {}

		for i in range(1, num + 1):
			for j in range(1, num + 1):
				from_= self.place_list[i]
				to_ = self.place_list[j]
				distance_matrix[(i, j)] = self.get_distance(from_=from_, to_=to_)

		return distance_matrix





if __name__ == '__main__':
	place_list = {
		1 : 'Red Fort', 
		2 : 'Pink City', 
		3 : 'Goa', 
		4 : 'Hawa Mahal'
	}

	place_coords = {
		'Red Fort' : [28.6562, 77.2410],
		'Pink City' : [26.9124, 75.7873],
		'Goa' : [15.2993, 74.1240],
		'Hawa Mahal' : [26.9239, 75.8267]
	}

	dl = DistanceLocator(
		place_list=place_list, 
		place_coords=place_coords
	)

	print(dl.set_distance_matrix(len(place_list)))

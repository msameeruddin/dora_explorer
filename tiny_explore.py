import random

from find_path import ShortestPathFinder

class DoraTheExplorer(object):
	def __init__(self, place_list, place_coords):
		self.place_list = place_list
		self.place_coords = place_coords
		self.cities_count = len(self.place_list)
		self.num_cities = self.set_distance_matrix(num=self.cities_count)
		self.one_step_nodes = []
		self.distances = []
		self.final_step_nodes = []


	def set_distance_matrix(self, num):
		"""
		returns a dict that basically contains the cost from `a` to `b`
		{(1, 2) : 10, ...}
		"""
		distance_matrix = {}

		for i in range(1, num + 1):
			for j in range(1, num + 1):
				from_= self.place_list[i]
				to_ = self.place_list[j]
				distance_matrix[(i, j)] = self.get_distance(from_=from_, to_=to_)

		return distance_matrix


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


	def get_cost_val(self, row, col, source):
		"""
		returns an int value corresponding to it's `row` and `col`
		"""
		if col == 0:
			col = source
			return self.num_cities[(row, col)]

		return self.num_cities[(row, col)]


	def get_possibilities(self):
		"""
		returns a dict showing all possible sources and non_source cities
		"""
		cities = list(range(1, self.cities_count + 1))
		possibilities = {}

		for city in cities:
			dtars = cities[:]
			dtars.remove(city)
			possibilities[city] = dtars

		return possibilities


	def get_paths_from_source(self, source_city):
		"""
		returns a list showing all possible paths from source
		"""
		all_possibilities = self.get_possibilities()
		non_source_cities = all_possibilities[source_city]
		possible_paths = []

		for i in range(len(non_source_cities)):
			placeholder_cities = non_source_cities[:]
			sub_ = placeholder_cities.pop(i)
			placeholder_cities.insert(0, sub_)
			possible_paths.append(placeholder_cities)

		return possible_paths


	def get_min_distance(self, main_city, dummy_city, cities):
		"""
		returns an int value which is the minimal distance 
		required to travel all the cities and return to the 
		corresponding source by travelling each city once
		"""
		if len(cities) == 1:
			min_dis = self.get_cost_val(row=dummy_city, col=cities[0], source=main_city) \
			+ self.get_cost_val(row=cities[0], col=0, source=main_city)
			self.one_step_nodes.append([dummy_city, cities[0]])

			return min_dis

		else:
			dists = []
			ocities = []

			for city in cities:
				dcities = cities[:]
				dcities.remove(city)
				curr_min_dis = self.get_min_distance(
					main_city=main_city, 
					dummy_city=city, 
					cities=dcities
				)
				dists.append(
					self.get_cost_val(
						row=dummy_city, 
						col=city, 
						source=dummy_city
					) + curr_min_dis
				)
				ocities.append([dummy_city, city])
			
			self.distances.append(dists)
			self.final_step_nodes.append(ocities)

			return min(dists)

	def find_shortest_path(self, source_city):
		"""
		returns a tuple with the best possible shortest path 
		and the minimal distance
		"""
		if self.cities_count > 2:
			possible_paths = self.get_paths_from_source(source_city)
			self.get_min_distance(
				main_city=source_city,
				dummy_city=source_city,
				cities=possible_paths[0]
			)

			if (self.cities_count != 4):
				print('cannot find path for {} cities'.format(self.cities_count))
				return '~>>~',  min(self.distances[-1])

			end_dis = self.distances[-1]
			non_end_nodes = self.final_step_nodes[:len(self.final_step_nodes) - 1]
			non_end_dis = self.distances[:len(self.distances) - 1]

			spf = ShortestPathFinder(
				source=source_city, 
				non_source_cities=possible_paths[0], 
				non_end_dis=non_end_dis
			)
			shortest_path, actual_min_dis = spf.get_shortest_path(
				nen=non_end_nodes,
				osn=self.one_step_nodes,
				ned=non_end_dis,
				end_dis=end_dis
			)
			return shortest_path, actual_min_dis

		return """Exploration can't be done""", 0





if __name__ == '__main__':
	place_list = {
		1 : 'Red Fort', 
		2 : 'Pink City', 
		3 : 'Goa', 
		4 : 'Howrah Bridge'
	}

	place_coords = {
		'Red Fort' : [28.6562, 77.2410],
		'Pink City' : [26.9124, 75.7873],
		'Goa' : [15.2993, 74.1240],
		'Howrah Bridge' : [22.5851, 88.3468]
	}

	explore = DoraTheExplorer(
		place_list=place_list,
		place_coords=place_coords
	)

	path, dis = explore.find_shortest_path(source_city=2)
	print(path)
	print(dis)
	# print(explore.distances)
	# print(explore.one_step_nodes)
	# print(explore.final_step_nodes)
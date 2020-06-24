
from find_path import ShortestPathFinder
from travel_places import GeoTraveller

class DoraTheExplorer(GeoTraveller, ShortestPathFinder):
	def __init__(self, place_list):
		self.place_list = self._get_noded_places(place_list=place_list)
		self.cities_count = len(self.place_list)
		self.num_cities = self.set_distance_matrix(place_list=self.place_list)
		self.one_step_nodes = []
		self.final_step_nodes = []
		self.end_distances = []


	def get_cost_val(self, row, col, source):
		"""
		Get the corresponding value with respect  to `row` and `col`
		:param int row: index of the row
		:param int col: index of the column
		:parma int source: Source node 
		:return int: corresponding value 
		"""
		if col == 0:
			col = source
			return self.num_cities[(row, col)]
		return self.num_cities[(row, col)]


	def get_possibilities(self):
		"""
		Get all the possibilities leaving the source node
		:param:
		:return: dict[int, list[int]]
		"""
		cities = list(range(1, self.cities_count + 1))
		possibilities = {}

		for city in cities:
			dtars = cities[:]
			dtars.remove(city)
			possibilities[city] = dtars

		return possibilities


	def get_non_source_nodes(self, source_city):
		"""
		Get all the possible nodes from which the path is found
		:param int source_city: Source node
		:return: list[list[int]]
		If `1` is source, then possible paths would be
		[[2, 3, 4]
		 [3, 2, 4]
		 [4, 2, 3]]
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


	def solve_tsp(self, main_city, dummy_city, cities):
		"""
		Get the minimal value for tsp problem
		:param int main_city: Main city node
		:param int dummy_city: Dummy city node
		:param list cities: list of cities leaving source city
		:return int: minimum distance
		"""
		if len(cities) == 1:
			min_dis = self.get_cost_val(
				row=dummy_city, 
				col=cities[0], 
				source=main_city
			) + self.get_cost_val(
				row=cities[0], 
				col=0, 
				source=main_city
			)
			self.one_step_nodes.append([dummy_city, cities[0]])
			
			return min_dis

		else:
			dists = []
			ocities = []

			for city in cities:
				dcities = cities[:]
				dcities.remove(city)
				curr_min_dis = self.solve_tsp(
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
			
			self.end_distances.append(dists)
			self.final_step_nodes.append(ocities)

			return min(dists)

	
	def get_min_dis(self, source_city):
		"""
		Get the possible minimal of minimal values for tsp
		:param int source_city:
		:return: float
		"""
		possible_paths = self.get_non_source_nodes(source_city)
		self.solve_tsp(
			main_city=source_city,
			dummy_city=source_city,
			cities=possible_paths[0]
		)
		end_dis = self.end_distances[-1]

		self.one_step_nodes = []
		self.final_step_nodes = []
		self.end_distances = []

		return round(min(end_dis), 2)
	

	def find_shortest_path(self, source_city):
		"""
		Find the shortest path after solving tsp
		:param int source_city: 1
		:return string: "1 >> 2 >> 4 >> 3 >> 1"
		"""
		if self.cities_count == 4:
			possible_paths = self.get_non_source_nodes(source_city)
			
			self.solve_tsp(
				main_city=source_city,
				dummy_city=source_city,
				cities=possible_paths[0]
			)

			end_dis = self.end_distances[-1]
			non_end_nodes = self.final_step_nodes[:len(self.final_step_nodes) - 1]
			non_end_dis = self.end_distances[:len(self.end_distances) - 1]

			shortest_path = self.get_shortest_path(
				sc=source_city, 
				nen=non_end_nodes,
				osn=self.one_step_nodes,
				ned=non_end_dis,
				nsc=possible_paths[0],
				end_dis=end_dis
			)

			self.one_step_nodes = []
			self.final_step_nodes = []
			self.end_distances = []

			return shortest_path
		
		return """cannot find path for {} cities""".format(self.cities_count)


	def get_path(self, source_city, num_path=False, map_token=None, with_plot=False, with_map=False, with_directions=False):
		"""
		Get the shortes path based on the actual city names
		:param int source_city: 1
		:param bool num_path: Returns a num shortest path if available
		:param NoneType map_token: mapbox API required
		:param bool with_plot: Retursn the normal plot if given True
		:param bool with_map: Returns the map plot in html format if available
		:param bool with_directions: Returns the map plot with mapbox directions if available
		:return string: "{city_name} >> {city_name} >> {city_name} >> {city_name} >> {city_name}"
		"""
		
		path = self.find_shortest_path(source_city)

		# currently limited to any four standard cities of India
		if self.cities_count == 4:

			if not num_path:
				order_places = [self.place_list[int(i)] for i in path.split(' >> ')]
				order_path = self.get_order_path(order_places=order_places)
				place_path = ' >> '.join(order_places)
				
				# write the plot result in html format
				travelling_places = list(self.place_list.values())
				
				if with_plot and map_token:
					if with_directions:
						self.get_route_visuals(
							place_list=travelling_places, order_path=order_path, 
							geo_token=map_token, with_directions=True)
					else:
						self.get_route_visuals(place_list=travelling_places, order_path=order_path, geo_token=map_token)
					print('plot is saved successfully ... ')
				
				elif with_plot:
					if with_map and map_token:
						if with_directions:
							self.get_route_visuals(
								place_list=travelling_places, order_path=order_path, 
								geo_token=map_token, with_directions=True)
						else:
							self.get_route_visuals(place_list=travelling_places, order_path=order_path, geo_token=map_token)
					else:
						print('MapBox API required for getting map result ... ')
						self.get_route_visuals(place_list=travelling_places, order_path=order_path)
					print('plot is saved successfully ... ')

				elif with_map:
					if map_token and with_directions:
						self.get_route_visuals(
							place_list=travelling_places, order_path=order_path, 
							geo_token=map_token, with_directions=True)
					elif map_token and not with_directions:
						self.get_route_visuals(place_list=travelling_places, order_path=order_path, geo_token=map_token)
					else:
						print('MapBox API required for getting map result ... ')
						self.get_route_visuals(place_list=travelling_places, order_path=order_path)
					print('plot is saved successfully ... ')

				elif map_token:
					if with_directions:
						self.get_route_visuals(
							place_list=travelling_places, order_path=order_path, 
							geo_token=map_token, with_directions=True)
					else:
						self.get_route_visuals(place_list=travelling_places, order_path=order_path, geo_token=map_token)
					print('plot is saved successfully ... ')

				elif with_directions:
					if map_token:
						self.get_route_visuals(
							place_list=travelling_places, order_path=order_path, 
							geo_token=map_token, with_directions=True)
					else:
						print('MapBox API required for getting map result ... ')
						self.get_route_visuals(place_list=travelling_places, order_path=order_path)
					print('plot is saved successfully ... ')
				
				return place_path
		return path







if __name__ == '__main__':
	# place_list = ['Punch', 'Zunheboto', 'Zaidpur', 'Bengaluru']
	place_list = ['Bengaluru', 'Mumbai', 'Zunheboto', 'Hindupur']

	explore = DoraTheExplorer(
		place_list=place_list,
	)

	with open('mapbox_token.txt', 'r') as mk:
		map_token = mk.read()


	dis = explore.get_min_dis(source_city=2)
	print(dis)
	print(explore.get_path(source_city=2, num_path=True))
	ft_dis = explore.get_distance(from_='Srinagar', to_='Kanniyakumari')
	print(ft_dis)
	route = explore.get_travel_route(from_='Srinagar', to_='Kanniyakumari', geo_token=map_token)
	print(route)

from dora_explorer.find_path import ShortestPathFinder
from dora_explorer.travel_places import GeoTraveller

class DoraTheExplorer(GeoTraveller, ShortestPathFinder):
	def __init__(self, place_list):
		self.place_list = self._get_noded_places(place_list=place_list)
		self.cities_count = len(self.place_list)
		self.num_cities = self.set_distance_matrix(place_list=self.place_list)
		self.place_values = place_list
		self.place_keys = list(self.place_list.keys())
		
		self.one_step_nodes = []
		self.final_step_nodes = []
		self.end_distances = []

		## validation if the places belong to the same country
		loc_place_coords = self._get_noded_coords(place_list=self.place_values)
		loc_vals = list(loc_place_coords.values())
		country_codes = [loc_[-1] for loc_ in loc_vals]
		self.is_same_country = False if (len(set(country_codes)) != 1) else True


	def get_cost_val(self, row, col, source):
		"""
		Get the corresponding value with respect  to `row` and `col`
		:param int row: index of the row
		:param int col: index of the column
		:parma int source: Source node 
		:return int: corresponding value 
		"""
		
		if isinstance(source, str):
			if source in self.place_values:
				source = self.place_keys[self.place_values.index(source)]
		else:
			source = source

		if isinstance(row, str):
			if row in self.place_values:
				row = self.place_keys[self.place_values.index(row)]
			else:
				row = row
		
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
		:param any(int, str) source_city: Source node
		:return: list[list[int]]
		If `1` is source, then possible paths would be
		[[2, 3, 4]
		 [3, 2, 4]
		 [4, 2, 3]]
		"""
		if isinstance(source_city, int):
			if source_city > self.cities_count:
				return []

		elif isinstance(source_city, str):
			if source_city in self.place_values:
				source_city = self.place_keys[self.place_values.index(source_city)]

		else:
			source_city = source_city

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

	
	def get_min_dis(self, source_city, in_miles=False, in_meters=False, in_feet=False, in_yards=False):
		"""
		Get the possible minimal of minimal values for tsp
		:param any(int, str) source_city:
		:param bool in_miles: Miles
		:param bool in_meters: Meters
		:param bool in_feet: Feet
		:param bool in_yards: Yards
		:return: float
		"""
		if self.is_same_country is False:
			return "Cannot find the minimum distance to cover the cities {}, as they do not belong to the same country.".format(self.place_values)
		possible_paths = self.get_non_source_nodes(source_city)

		if possible_paths:
			self.solve_tsp(
				main_city=source_city,
				dummy_city=source_city,
				cities=possible_paths[0]
			)
			end_dis = self.end_distances[-1]

			self.one_step_nodes = []
			self.final_step_nodes = []
			self.end_distances = []

			min_dist = min(end_dis)
			if in_miles:
				return round((min_dist / 1.609), 2)
			elif in_meters:
				return round((min_dist * 1000), 2)
			elif in_feet:
				return round((min_dist * 3281), 2)
			elif in_yards:
				return round((min_dist * 1094), 2)
			return round(min(end_dis), 2)
		
		return None
	

	def find_shortest_path(self, source_city):
		"""
		Find the shortest path after solving tsp
		:param any(int, str) source_city: 1
		:return string: "1 >> 2 >> 4 >> 3 >> 1"
		"""
		if isinstance(source_city, str):
			if source_city in self.place_values:
				source_city = self.place_keys[self.place_values.index(source_city)]
		else:
			source_city = source_city
		
		if self.cities_count == 4:
			possible_paths = self.get_non_source_nodes(source_city)

			if possible_paths:			
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


	def get_path(self, source_city, num_path=False, geo_token=None, with_plot=False, with_map=False, with_directions=False):
		"""
		Get the shortes path based on the actual city names
		:param any(int, str) source_city:
		:param bool num_path: Returns a num shortest path if available
		:param NoneType geo_token: mapbox API required
		:param bool with_plot: Retursn the normal plot if given True
		:param bool with_map: Returns the map plot in html format if available
		:param bool with_directions: Returns the map plot with mapbox directions if available
		:return string: "{city_name} >> {city_name} >> {city_name} >> {city_name} >> {city_name}"
		"""		
		if self.is_same_country is False:
			return "Cannot find the shortest path, as the cities {} do not belong to the same country.".format(self.place_values)
		
		path = self.find_shortest_path(source_city)
		# currently limited to any four standard cities of India
		if self.cities_count == 4:
			
			if isinstance(source_city, int):
				if source_city > self.cities_count:
					return "Number of cities given - {}.\nFound source_city happened to be {}".format(self.cities_count, source_city)
				else: source_city = source_city

			if isinstance(source_city, str):
				if source_city in self.place_values:
					source_city = self.place_keys[self.place_values.index(source_city)]


			if not num_path:
				order_places = [self.place_list[int(i)] for i in path.split(' >> ')]
				order_path = self.get_order_path(order_places=order_places)
				place_path = ' >> '.join(order_places)
				
				# write the plot result in html format
				travelling_places = self.place_values
				
				if with_plot and geo_token:
					if with_directions:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token, 
							with_directions=True
						)
					else:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token
						)
					print('plot is saved successfully ... ')
				
				elif with_plot:
					if with_map and geo_token:
						if with_directions:
							self.get_route_visuals(
								place_list=travelling_places, 
								order_path=order_path, 
								geo_token=geo_token, 
								with_directions=True
							)
						else:
							self.get_route_visuals(
								place_list=travelling_places, 
								order_path=order_path, 
								geo_token=geo_token
							)
					else:
						print('MapBox API required for getting map result ... ')
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path
						)
					print('plot is saved successfully ... ')

				elif with_map:
					if geo_token and with_directions:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token, 
							with_directions=True
						)
					elif geo_token and not with_directions:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token
						)
					else:
						print('MapBox API required for getting map result ... ')
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path
						)
					print('plot is saved successfully ... ')

				elif geo_token:
					if with_directions:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token, 
							with_directions=True
						)
					else:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token
						)
					print('plot is saved successfully ... ')

				elif with_directions:
					if geo_token:
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path, 
							geo_token=geo_token, 
							with_directions=True
						)
					else:
						print('MapBox API required for getting map result ... ')
						self.get_route_visuals(
							place_list=travelling_places, 
							order_path=order_path
						)
					print('plot is saved successfully ... ')
				
				return place_path
			
			return path







if __name__ == '__main__':
	place_list = ['Bengaluru', 'Mumbai', 'Zunheboto', 'Hindupur']

	explore = DoraTheExplorer(
		place_list=place_list,
	)

	with open('mapbox_token.txt', 'r') as mk:
		geo_token = mk.read()

	dis = explore.get_min_dis(source_city="Mumbai")
	print(dis)
	print(explore.get_path(source_city=1, num_path=True))
	print(explore.get_path(source_city="Mumbai", num_path=False))
	ft_dis = explore.get_distance(from_='Srinagar', to_='Kanniyakumari')
	print(ft_dis)
	route = explore.get_travel_route(from_='Srinagar', to_='Kanniyakumari', geo_token=geo_token)
	print(route)
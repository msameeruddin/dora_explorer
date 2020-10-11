
from dora_explorer.distance_locator import DistanceLocator
from dora_explorer.useful_plots import HTMLPlotter

class GeoTraveller(DistanceLocator, HTMLPlotter):
	def __init__(self):
		pass
	
	def get_coords_joining(self, from_, to_):
		"""
		Get the coordinate values `lats` and `lons`
		:param string from_: from place
		:param string to_: to place
		:return: tuple[list[float]]

		Examples
		--------
		>>> # munich - (48.1372, 11.5756)
		>>> # berlin - (52.5186, 13.4083)
		>>> get_coords_joining('munich', 'berlin')
		([48.1372, 52.5186], [11.5756, 13.4083])
		"""
		place_coords = self._get_noded_coords(place_list=[from_, to_])
		from_coords = place_coords[from_]
		to_coords = place_coords[to_]

		lats = [l[0] for l in [from_coords, to_coords]]
		lons = [l[1] for l in [from_coords, to_coords]]

		return lats, lons


	def get_order_path(self, order_places):
		"""
		Get the order path in the form of [['a', 'b'], ['b', 'c'], ['c', 'a']]
		:param order_places: list
		:return: list[list[string]]
		"""
		order_path = [
			[order_places[i], order_places[i + 1]] 
			for i in range(0, len(order_places) - 1)
		]

		return order_path

	
	def get_travel_route(self, from_, to_, geo_token=None):
		"""
		Get the travel route - coordinates with respect to the mode `driving`
		using `mapbox` API
		:param string from_: from place
		:param string to_: to place
		:param string geo_token: Mapbox API
		:return: tuple[list[float]]

		Examples
		--------
		>>> # 'Red Fort' - [28.6562, 77.2410]
		>>> # 'Pink City' - [26.9124, 75.7873]
		>>> get_travel_route('Red Fort', 'Pink City')
		([28.6562, 26.9124], [77.241, 75.7873])
		>>> get_travel_route('Red Fort', 'Pink City', geo_token='<map_box_api>')
		(	
			[28.65834, 28.657799, 28.655979, ..., 26.912434], 
			[77.238106, 77.236954, 77.236847, ..., 75.78727]
		)
		"""
		if geo_token:
			## get direction route with the mode `driving-traffic`
			import requests

			place_coords = self._get_noded_coords(place_list=[from_, to_])
			from_lat, from_lon, from_country = place_coords[from_]
			to_lat, to_lon, to_country = place_coords[to_]

			map_url = 'https://api.mapbox.com/directions/v5/mapbox/{}/{},{};{},{}?geometries=geojson&access_token={}'.format(
				'driving-traffic', from_lon, from_lat, to_lon, to_lat, geo_token
			)

			open_map = requests.get(url=map_url)
			map_js = open_map.json()

			lats = []; lons = []
			try:
				for ks in map_js['routes']:
					for k, v in ks.items():
						if k == 'geometry':
							for each_k, each_v in v.items():
								if each_k == 'coordinates':
									for each_loc in each_v:
										lons.append(each_loc[0])
										lats.append(each_loc[1])
			except KeyError as e:
				lats.extend([from_lat, to_lat])
				lons.extend([from_lon, to_lon])

			return lats, lons

		# if not geo_token
		# print('MapBox API required for getting the route direction ... ')
		lats, lons = self.get_coords_joining(from_=from_, to_=to_)
		return lats, lons


	def get_route_visuals(self, place_list, order_path, geo_token=None, with_directions=False):
		"""
		Visualize the route direction of the map - html format
		:param list place_list: List of place names
		:param list order_path: Returns in the form [['a', 'b'], ['b', 'c'], ['c', 'a']]
		:param string geo_token: Mapbox API
		:return: bool (after successfully getting the output as html)
		"""
		import plotly.graph_objects as go

		place_coords = self._get_noded_coords(place_list=place_list)
		place_lats = [place_coords[i][0] for i in place_list]
		place_lons = [place_coords[i][1] for i in place_list]
		data = []
		
		if geo_token:
			## Mapbox plot showing the locations and the shortest path
			center_lat = sum(place_lats) / len(place_lats)
			center_lon = sum(place_lons) / len(place_lons)

			for each_join in range(len(order_path)):
				from_, to_ = order_path[each_join]
				if with_directions is True:
					lats_, lons_ = self.get_travel_route(from_=from_, to_=to_, geo_token=geo_token)
				else:
					lats_, lons_ = self.get_travel_route(from_=from_, to_=to_, geo_token=None)
				data.append(self.do_map_line_plot(go=go, lats=lats_, lons=lons_, width=2.5))
			
			data.append(
				self.do_map_marker_plot(
					go=go, 
					lats=place_lats,
					lons=place_lons,
					size=15,
					text_list=place_list
				)
			)
			layout = self.do_map_layout(
				go=go, 
				title='Geo - Explorer', 
				accesstoken=geo_token, 
				center_lat=center_lat, 
				center_lon=center_lon, 
				zoom=3.5, 
				style='outdoors'
			)

		else:
			## normal Scatter plot showing the shortest path
			for each_join in range(len(order_path)):
				from_, to_ = order_path[each_join]
				lats_, lons_ = self.get_travel_route(from_=from_, to_=to_)
				data.append(self.do_line_scatter(go=go, x=lats_, y=lons_, width=2.5))

			data.append(
				self.do_marker_scatter(go=go, x=lats_, y=lons_, size=15)
			)
			layout = self.do_scatter_layout(go=go, title='Geo - Explorer')

		fig = go.Figure(data=data, layout=layout)
		fig.write_html('explore.html')
		fig.show()

		return True












if __name__ == '__main__':
	place_list = ['Punch', 'Zunheboto', 'Zaidpur']

	travel = GeoTraveller(
		place_list=place_list, 
	)

	route = travel.get_travel_route(from_='Punch', to_='Zunheboto')
	print(route)

	print(travel.get_order_path(place_list))

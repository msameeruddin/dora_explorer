import random
import os
import mpu
import requests

from tiny_explore import DoraTheExplorer


class GeoTraveller(object):
	def __init__(self, place_list, place_coords, geo_token):
		self.place_list = place_list
		self.place_coords = place_coords
		self.order_places = []
		self.order_path = []
		self.geo_token = geo_token
		self.travel_mode = 'driving'

	def get_place_path(self):
		"""
		returns a tuple with the shortest path and the minimum distance
		"""
		explore = DoraTheExplorer(
			place_list=self.place_list,
			place_coords=self.place_coords
		)

		path, dis = explore.find_shortest_path(source_city=2)
		self.order_places = [self.place_list[int(i)] for i in path.split(' >> ')]
		self.order_path = self.get_order_path(order_places=self.order_places)
		place_path = ' >> '.join(self.order_places)

		return place_path, dis

	def get_order_path(self, order_places):
		"""returns a list of lists with `from_` and `to_` names"""
		order_path = [
			[order_places[i], order_places[i + 1]] 
			for i in range(0, len(order_places) - 1)
		]

		return order_path

	def get_coords_joining(self, from_, to_):
		"""returns a tuple of `latitudes` and `longitudes` for joining all the coords"""
		from_coords = self.place_coords[from_]
		to_coords = self.place_coords[to_]

		lats = [l[0] for l in [from_coords, to_coords]]
		lons = [l[1] for l in [from_coords, to_coords]]

		return lats, lons

	def get_travel_route(self, from_, to_):
		"""returns a tuple of `latitudes` and `longitudes` showing the exact route"""
		from_lat, from_lon = self.place_coords[from_]
		to_lat, to_lon = self.place_coords[to_]

		map_url = 'https://api.mapbox.com/directions/v5/mapbox/{}/{},{};{},{}?geometries=geojson&access_token={}'.format(
			self.travel_mode, from_lon, from_lat, to_lon, to_lat, self.geo_token
		)

		open_map = requests.get(url=map_url)
		map_js = open_map.json()

		lats = []; lons = []
		for ks in map_js['routes']:
			for k, v in ks.items():
				if k == 'geometry':
					for each_k, each_v in v.items():
						if each_k == 'coordinates':
							for each_loc in each_v:
								lons.append(each_loc[0])
								lats.append(each_loc[1])

		return lats, lons













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

	travel = GeoTraveller(place_list=place_list, place_coords=place_coords)
	place_path, dis = travel.get_place_path()
	print(place_path)
	print(dis)
	print(travel.order_places)
	print(travel.order_path)

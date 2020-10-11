import requests

from dora_explorer.useful_plots import HTMLPlotter

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


	def _get_coords(self, place_name):
		"""
		Get the coordination values for each place
		:parma str place_name: Single place name
		:return: list[float]
		"""
		loc_place = place_name.casefold()
		geocode_url = 'https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/findAddressCandidates?SingleLine={}&outFields=*&f=json'.format(loc_place)

		geocode_req = requests.get(url=geocode_url)
		geocode_json = geocode_req.json()
		
		lat_ = geocode_json['candidates'][0]['location']['y']
		lon_ = geocode_json['candidates'][0]['location']['x']
		country_ = geocode_json['candidates'][0]['attributes']['Country']
		
		return [lat_, lon_, country_]


	def _get_noded_coords(self, place_list):
		"""
		Get the coordination values for each place
		:parma list place_list: List of place names
		:return: dict(str, list[float])
		"""
		coords_dumped = {}
		for place_ in place_list:
			loc_coords = self._get_coords(place_name=place_)
			coords_dumped[place_] = loc_coords

		return coords_dumped


class DistanceLocator(LocationHelper, HTMLPlotter):
	def __init__(self):
		pass

	
	def get_distance(self, from_, to_, in_miles=False, in_meters=False, in_feet=False, in_yards=False):
		"""
		Get the `haversine_distance` from `lat` and `lon`
		:param string from_: from place
		:param string to_: to place
		:param bool in_miles: Miles
		:param bool in_meters: Meters
		:param bool in_feet: Feet
		:param bool in_yards: Yards
		:return: float

		Examples
		--------
		>>> get_distance('munich', 'berlin')
		504.2
		"""
		from mpu import haversine_distance

		from_coords = self._get_coords(place_name=from_)
		to_coords = self._get_coords(place_name=to_)

		dist = haversine_distance(
			origin=from_coords[:2], 
			destination=to_coords[:2]
		)

		if in_miles:
			return round((dist / 1.609), 2)
		elif in_meters:
			return round((dist * 1000), 2)
		elif in_feet:
			return round((dist * 3281), 2)
		elif in_yards:
			return round((dist * 1094), 2)
		return round(dist, 2)


	def get_distance_plot(self, from_, to_, with_map=False, with_directions=False, geo_token=None):
		"""
		Get the distance plot from_ to to_
		:param string from_: from place
		:param string to_: to place
		:param bool with_map:
		:param bool with_directions:
		:param str geo_token: Mapbox API
		:return: bool
		"""
		import plotly.graph_objects as go

		from_lat, from_lon, from_country = self._get_coords(place_name=from_)
		to_lat, to_lon, to_country = self._get_coords(place_name=to_)
		data = []

		if not geo_token:
			lats_ = [from_lat, from_lon]
			lons_ = [to_lat, to_lon]
			data.append(
				self.do_line_scatter(go=go, x=lats_, y=lons_, width=2.5)
			)
			data.append(
				self.do_marker_scatter(go=go, x=lats_, y=lons_, size=15)
			)
			layout = self.do_scatter_layout(go=go, title='Geo - Explorer')
		
		else:
			lats_ = []; lons_ = []
			center_lat = sum([from_lat, to_lat]) / 2
			center_lon = sum([from_lon, to_lon]) / 2
			
			if with_directions is True:
				map_url = 'https://api.mapbox.com/directions/v5/mapbox/{}/{},{};{},{}?geometries=geojson&access_token={}'.format(
					'driving-traffic', from_lon, from_lat, to_lon, to_lat, geo_token)

				open_map = requests.get(url=map_url)
				map_js = open_map.json()

				try:
					for ks in map_js['routes']:
						for k, v in ks.items():
							if k == 'geometry':
								for each_k, each_v in v.items():
									if each_k == 'coordinates':
										for each_loc in each_v:
											lons_.append(each_loc[0])
											lats_.append(each_loc[1])
				except KeyError as e:
					lats_.extend([from_lat, to_lat])
					lons_.extend([from_lon, to_lon])
			else:
				lats_.extend([from_lat, to_lat])
				lons_.extend([from_lon, to_lon])

			data.append(
				self.do_map_line_plot(go=go, lats=lats_, lons=lons_, width=2.5)
			)
			data.append(
				self.do_map_marker_plot(
					go=go, 
					lats=[from_lat, to_lat],
					lons=[from_lon, to_lon],
					size=15,
					text_list=[from_, to_]
				)
			)
			layout = self.do_map_layout(
				go=go, 
				title='Distance plot', 
				accesstoken=geo_token, 
				center_lat=center_lat, 
				center_lon=center_lon, 
				zoom=6, 
				style='outdoors'
			)

		fig = go.Figure(data=data, layout=layout)
		fig.show()

		return True

			
	def set_distance_matrix(self, place_list):
		"""
		Set the distance matrix showing the distance values from `a` to `b`
		:param dict place_list: dict of places - {1 : 'place_name', 2 : 'place_name' ...}
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
	print(dl._get_noded_places(place_list))
	print(dl.set_distance_matrix(dl._get_noded_places(place_list)))
	print(dl.get_distance('bengaluru', 'delhi'))

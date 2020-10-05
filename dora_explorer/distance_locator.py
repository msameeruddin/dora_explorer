import requests

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


class DistanceLocator(LocationHelper):
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

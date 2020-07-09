import geonamescache as geo
import json
from unidecode import unidecode

gc = geo.GeonamesCache()

def identify_indian_cities():
	geo_cities = list(gc.get_cities().values())

	indian_cities = {}
	for meta_city in geo_cities:
		if meta_city['countrycode'] == 'IN':
			city_name = unidecode(meta_city['name'])
			if city_name not in list(indian_cities.keys()):
				indian_cities[city_name] = [meta_city['latitude'], meta_city['longitude']]

	with open('indian_cities_geoloc.json', 'w', encoding='utf-8') as icg:
		json.dump(indian_cities, icg, ensure_ascii=False)

	return True


if __name__ == '__main__':
	# identify_indian_cities()
	print(True)
from dora_explorer.distance_locator import DistanceLocator
from dora_explorer.tiny_explore import DoraTheExplorer
from dora_explorer.travel_places import GeoTraveller

place_list = ['delhi', 'hyderabad', 'hindupur', 'lucknow']

dl = DistanceLocator()
travel = GeoTraveller()
explore = DoraTheExplorer(place_list=place_list)

## distance locator
from_ = 'hindupur'
to_ = 'california'
print(dl.get_distance(from_=from_, to_=to_, in_miles=True))
print(dl.get_distance(from_=from_, to_=to_, in_yards=True))
print(dl.get_distance(from_=from_, to_=to_, in_feet=True))
print(dl.get_distance(from_=from_, to_=to_, in_meters=True))
print(dl.get_distance(from_=from_, to_=to_))


## geo-traveller
# required geo_token
geo_token = ''
route = travel.get_travel_route(from_='lucknow', to_='noida', geo_token=geo_token)
print(route)

## dora the explorer
print(explore.get_path(
	source_city='lucknow', 
	with_map=True, 
	with_directions=False, 
	geo_token=geo_token)
)
print(explore.get_path(source_city=2, num_path=True))
print(explore.get_min_dis(source_city='lucknow', in_miles=True))
print(explore.get_min_dis(source_city='lucknow', in_yards=True))
print(explore.get_min_dis(source_city='lucknow', in_feet=True))
print(explore.get_min_dis(source_city='lucknow', in_meters=True))
print(explore.get_min_dis(source_city='lucknow'))

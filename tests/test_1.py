from dora_explorer.distance_locator import DistanceLocator
from dora_explorer.tiny_explore import DoraTheExplorer
from dora_explorer.travel_places import GeoTraveller

place_list = ['Delhi', 'Hyderabad', 'Hindupur', 'Mumbai']

dl = DistanceLocator()
explore = DoraTheExplorer(place_list=place_list)
travel = GeoTraveller()

from_ = 'Hindupur'
to_ = 'Bengaluru'

# required geo_token
geo_token = ''
# route = travel.get_travel_route(from_='Lucknow', to_='Noida', geo_token=geo_token)

# print(route)
print(dl.get_distance(from_=from_, to_=to_))
# print(explore.get_path(source_city='Mumbai', with_map=True, with_directions=True, geo_token=geo_token))
print(explore.get_path(source_city=4, num_path=True))
# print(explore.get_min_dis(source_city='Mumbai'))

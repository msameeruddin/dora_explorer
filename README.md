# Dora the Explorer

As the name suggests everything, this package is intended for exploring the earth. Imagine you have a set of places (at max 4 places) to vist, how do you know exactly to find the best route to cover all the places? This package helps to find the best route which is pre-planned and displays the route with respect to distance and finally reaching the source place i.e., home.

We have known about one of the famous problems in mathematics - graph theory that is **Travelling Salesman Problem**. To give a simple gist about the problem, basically there is a salesman who has to travel a bunch of places (cities) to deliver the items. There could be so many possibilities to cover all the cities and reach to his/her source place. But it is very important for a salesman to choose the best possible route which gives a minimal distance. By this he/she can save a lot time and deliver the items at the earliest. For this project, I have considered distance as an important factor, later on time and other factors shall be added.

A typical example can be seen below. When selected 4 places that belong to India the result is obtained having the shortest path to cover the places. The path is just a straight line between the cities.

![with_map](https://user-images.githubusercontent.com/63333753/87243481-e4e89980-c453-11ea-8d51-4cd3bad43109.png)

What if we want to get the actual route direction from each city that is joining another city?.

![with_directions](https://user-images.githubusercontent.com/63333753/87244009-72c68380-c458-11ea-964c-99c5f63406c6.png)

For getting the map results, it is important to have Mapbox API which is a free API. To get the API - register on [mapbox website](https://www.mapbox.com/). Once registered, create a secret token by clicking `Create a token` button by navigating to this [page](https://account.mapbox.com/). Save the token as it will be needed for generating the map results.

## Installation

```
pip install dora-explorer --user
```

## Implementation

```python
from dora_explorer.distance_locator import DistanceLocator

dl = DistanceLocator()

from_ = 'Hindupur'
to_ = 'Bengaluru'

distance = dl.get_distance(from_=from_, to_=to_)
print(distance) # 95.84
```

```python
from dora_explorer.tiny_explore import DoraTheExplorer

place_list = ['Delhi', 'Hyderabad', 'Hindupur', 'Mumbai']
explore = DoraTheExplorer(place_list=place_list)

min_dis = explore.get_min_dis(source_city='Mumbai')
print(min_dis) # 3583.36

geo_token = <Mapbox API Token>
path = explore.get_path(source_city='Mumbai', with_map=True, with_directions=True, geo_token=geo_token)
print(path) # Mumbai >> Delhi >> Hyderabad >> Hindupur >> Mumbai
```

**Note:** The `source_city` param can also be given an integer. Either `1` or `2` or `3` or `4` as in a list of four places is passed.

```python
from dora_explorer.tiny_explore import DoraTheExplorer

place_list = ['Delhi', 'Hyderabad', 'Hindupur', 'Mumbai']
explore = DoraTheExplorer(place_list=place_list)

path = explore.get_path(source_city=1, num_path=True)
print(path) # 1 >> 2 >> 3 >> 4 >> 1
```

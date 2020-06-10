distances = [
	[118, 143], 
	[144, 90], 
	[92, 119], 
	[177, 136, 166], 
	[145, 174], 
	[210, 68], 
	[105, 146], 
	[221, 87, 148], 
	[178, 141], 
	[226, 88], 
	[112, 135], 
	[201, 113, 135], 
	[125, 112], 
	[169, 112], 
	[160, 134], 
	[124, 138, 187], 
	[176, 162, 182, 153]
]

one_step_nodes = [
	[4, 5], 
	[5, 4], 
	[3, 5], 
	[5, 3], 
	[3, 4], 
	[4, 3], 
	[4, 5], 
	[5, 4], 
	[2, 5], 
	[5, 2], 
	[2, 4], 
	[4, 2], 
	[3, 5], 
	[5, 3], 
	[2, 5], 
	[5, 2], 
	[2, 3], 
	[3, 2], 
	[3, 4], 
	[4, 3], 
	[2, 4], 
	[4, 2], 
	[2, 3], 
	[3, 2]
]

final_step_nodes = [
	[[3, 4], [3, 5]], 
	[[4, 3], [4, 5]], 
	[[5, 3], [5, 4]], 
	[[2, 3], [2, 4], [2, 5]], 
	[[2, 4], [2, 5]], 
	[[4, 2], [4, 5]], 
	[[5, 2], [5, 4]], 
	[[3, 2], [3, 4], [3, 5]], 
	[[2, 3], [2, 5]], 
	[[3, 2], [3, 5]], 
	[[5, 2], [5, 3]], 
	[[4, 2], [4, 3], [4, 5]], 
	[[2, 3], [2, 4]], 
	[[3, 2], [3, 4]], 
	[[4, 2], [4, 3]], 
	[[5, 2], [5, 3], [5, 4]], 
	[[1, 2], [1, 3], [1, 4], [1, 5]]
]

total_cities = [1, 2, 3, 4, 5]
source = 1
non_source_cities = [2, 3, 4, 5]
end_nodes = final_step_nodes[-1]
end_dis = distances[-1]
non_end_nodes = final_step_nodes[:len(final_step_nodes) - 1]
non_end_dis = distances[:len(distances) - 1]

def make_club(nen, osn, ned):
	osn_len = len(osn)
	nen_len = len(nen)

	if ((osn_len // nen_len) == 2):
		possible_nodes = [osn[i:i + 2] for i in range(0, osn_len, 2)]
	else:
		possible_nodes = []

	clubbed = map(list, zip(possible_nodes, non_end_dis)) if possible_nodes else []
	return clubbed

def get_sub_path(nen, osn, ned, sc, nsc):
	clubbed = make_club(nen=nen, osn=osn, ned=ned)

	min_nodes = []
	for i in clubbed:
		da = i[1]
		min_dis = min(da)
		min_index = da.index(min_dis)
		paired_nodes = i[0][min_index]
		min_nodes.append(paired_nodes)

	sub_paths = []
	for mn in min_nodes:
		smn = set(mn)
		snsc = set(nsc)
		sub_source = (snsc - smn).pop()
		sp = str(sub_source) + ' >'

		for i in mn:
			sp += ' ' + str(i) + ' >'
		
		sp = sp + ' ' + str(sc)
		sub_paths.append(sp)

	return sub_paths

def get_shortest_path(sc):
	if len(total_cities) > 4:
		return None, None

	sp = get_sub_path(
		nen=non_end_nodes, 
		osn=one_step_nodes, 
		ned=non_end_dis, 
		sc=sc, 
		nsc=non_source_cities)

	min_dis_index = end_dis.index(min(end_dis))
	shortest_path = str(sc) + ' > ' + sp[min_dis_index]

	return shortest_path, end_dis[min_dis_index]

path, distance = get_shortest_path(sc=source)
# print(path)
# print(distance)

from math import sin, cos, sqrt, atan2, radians

# approximate radius of earth in km
R = 6373.0

lat1 = radians(28.6562)
lon1 = radians(77.2410)
lat2 = radians(26.9124)
lon2 = radians(75.7873)

dlon = lon2 - lon1
dlat = lat2 - lat1

a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

print("Result:", distance)
# print("Should be:", 278.546, "km")


import mpu

lat1 = 28.6562
lon1 = 77.2410
lat2 = 26.9124
lon2 = 75.7873

dist = mpu.haversine_distance(origin=[lat1, lon1], destination=(lat1, lon1))
print(dist)
print(round(dist))
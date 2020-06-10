
class ShortestPathFinder():
	def __init__(self, source, non_source_cities, non_end_dis):
		self.source = source
		self.non_source_cities = non_source_cities
		self.non_end_dis = non_end_dis


	def get_clubbed(self, nen, osn, ned):
		"""
		returns a list of nodes along with the corresponding distances
		"""
		osn_len = len(osn)
		nen_len = len(nen)

		if ((osn_len // nen_len) == 2):
			possible_nodes = [osn[i:i + 2] for i in range(0, osn_len, 2)]
		else:
			possible_nodes = []

		clubbed = map(list, zip(possible_nodes, self.non_end_dis)) if possible_nodes else []
		return clubbed


	def get_sub_paths(self, nen, osn, ned):
		"""
		returns a string which is the sub_path of the minimal distance 
		"""
		clubbed = self.get_clubbed(nen=nen, osn=osn, ned=ned)

		if clubbed:
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
				snsc = set(self.non_source_cities)
				sub_source = (snsc - smn).pop()
				sp = str(sub_source) + ' >>'
				for i in mn:
					sp += ' ' + str(i) + ' >>'
				sp = sp + ' ' + str(self.source)
				sub_paths.append(sp)

			return sub_paths

		return []


	def get_shortest_path(self, nen, osn, ned, end_dis):
		"""
		returns a tuple showing the exact shortest path and 
		the minimal distance required to travel all the cities
		exactly once
		"""
		sub_paths = self.get_sub_paths(nen=nen, osn=osn, ned=ned)
		min_dis_index = end_dis.index(min(end_dis))
		shortest_path = str(self.source) + ' >> ' + sub_paths[min_dis_index]
		return shortest_path, end_dis[min_dis_index]
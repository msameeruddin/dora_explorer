
class ShortestPathFinder():
	def __init__(self):
		pass

	
	def get_clubbed(self, nen, osn, ned):
		"""
		Get the zip of nodes and the distances that is obtained
		:param list nen: Stands for non_end_nodes - [[[3, 4], [3, 5]], [[4, 3], [4, 5]], [] ...]
		:param list osn: Stands for one_step_nodes - [[4, 5], [5, 4], [3, 5], [5, 3], [], []]
		:param list ned: Stands for non_end_distances  - [[1, 1.3], [3, 21.2], [], []]
		:return: list[list, list] - [[], []]
		"""
		osn_len = len(osn)
		nen_len = len(nen)

		if ((osn_len // nen_len) == 2):
			possible_nodes = [osn[i:i + 2] for i in range(0, osn_len, 2)]
		else:
			possible_nodes = []

		clubbed = map(list, zip(possible_nodes, ned)) if possible_nodes else []
		return clubbed


	def get_sub_paths(self, sc, nen, osn, ned, nsc):
		"""
		Get the sub-path without the source node
		:param int sc: Source node
		:param list nen: Stands for non_end_nodes - [[[3, 4], [3, 5]], [[4, 3], [4, 5]], [] ...]
		:param list osn: Stands for one_step_nodes - [[4, 5], [5, 4], [3, 5], [5, 3], [], []]
		:param list ned: Stands for non_end_distances  - [[1, 1.3], [3, 21.2], [], []]
		:param list nsc: Stands for non_source - [2, 3, 4, 5]
		:return: string - '1 >> 2 >> 3'
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
				snsc = set(nsc)
				sub_source = (snsc - smn).pop()
				sp = str(sub_source) + ' >>'
				for i in mn:
					sp += ' ' + str(i) + ' >>'
				sp = sp + ' ' + str(sc)
				sub_paths.append(sp)

			return sub_paths

		return []


	def get_shortest_path(self, sc, nen, osn, ned, nsc, end_dis):
		"""
		Get the shortest path including the source node
		::param int sc: Source node
		:param list nen: Stands for non_end_nodes - [[[3, 4], [3, 5]], [[4, 3], [4, 5]], [] ...]
		:param list osn: Stands for one_step_nodes - [[4, 5], [5, 4], [3, 5], [5, 3], [], []]
		:param list ned: Stands for non_end_distances  - [[1, 1.3], [3, 21.2], [], []]
		:param list nsc: Stands for non_source - [2, 3, 4, 5]
		:param list end_dis: End distances - [12.3, 2, 32.1]
		:return: string - '1 >> 2 >> 3'
		"""
		sub_paths = self.get_sub_paths(sc=sc, nen=nen, osn=osn, ned=ned, nsc=nsc)
		min_dis_index = end_dis.index(min(end_dis))
		shortest_path = str(sc) + ' >> ' + sub_paths[min_dis_index]
		return shortest_path
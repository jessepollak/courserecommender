from itertools import groupby

def clusterize(items, k, similarity_function):
	centroids = random.sample(items, k)
	clusters = []
	
	for i in xrange(0, k):
		clusters.append([])
		
	for i in xrange(0, 5):
		for item in items:
			cluster_index = 0
			similarity = 1
			for centroid in centroids:
				c_sim = similarity_function(item, centroid)
				if c_sim < similarity:
					simarilty  = c_sim
					cluster_index = i
			clusters[cluster_index].append(item)
		centroids = centroidfiy(cluster) for cluster in clusters
		
		
def centroidify(cluster):
	cluster_size = len(cluster)
	cluster_courses = Ranking.find_all_by_user_ids(u.id for u in cluster)
	groups = []
	centroid = []
	
	for k, g in groupby(cluster_courses, lamdbda r : r.course_id):
		groups.append(list(g))
	
	for group in groups:
		val = sum(r.value in r in group) / cluster_size
		centroid.append(Ranking(course_id = group[0].course_id, value))
		
	return centroid
		
				
def cos_similarity(one, two):
	a_rankings = a.rankings
	b_rankings = b.rankings
	dot_product = 0
	a_mag = 0
	b_mag = 0
	for a_rank in a_rankings:
		for b_rank in b_rankings:
			if a_rank.course_id == b_rank.course_id:
				dot_product += b_rank.value*a_rank.value
				
	for a_rank in a_rankings:
		a_mag += a_rank ** 2
		
	for b_rank in b_rankings:
		b_mag += b_rank ** 2
		
	return dot_product / (a_mag + b_mag)

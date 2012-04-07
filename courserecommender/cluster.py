from itertools import groupby
from random import sample
from models import Ranking, User
		
		
def centroidify(cluster): 
	cluster_size = len(cluster)
	centroid = []
	if cluster_size != 0:
		cluster_courses = Ranking.find_all_by_user_ids(u.id for u in cluster)
		groups = []
		
		cluster_courses = sorted(cluster_courses, key=(lambda r: r.course_id))
		
		for k, g in groupby(cluster_courses, lambda r : r.course_id):
			groups.append(list(g))
	
		for group in groups:
			val = sum(r.value for r in group) / float(cluster_size)
			centroid.append(Ranking(course_id = group[0].course_id, value = val, user_id = None))
			
	centroid_user = User(id = None, rankings = centroid)
	return centroid_user
		
				
def cos_similarity(a, b):
	a_rankings = a.rankings
	b_rankings = b.rankings
	if len(a_rankings) == 0 or len(b_rankings) == 0:
		return 0
	dot_product = 0
	a_mag = 0
	b_mag = 0
	for a_rank in a_rankings:
		for b_rank in b_rankings:
			if a_rank.course_id == b_rank.course_id:
				dot_product += b_rank.value*a_rank.value
				
	for a_rank in a_rankings:
		a_mag += a_rank.value ** 2
	a_mag = a_mag**.5
		
	for b_rank in b_rankings:
		b_mag += b_rank.value ** 2
	b_mag = b_mag**.5

	return dot_product / float(a_mag*b_mag)
	
	
def clusterize(items, k, similarity_function): #temp for testing
	centroids = sample(items, k)
	clusters = []
	temp_items = items
	for i in xrange(0, k):
		clusters.append([centroids[i]])
		temp_items.remove(centroids[i])
	for item in temp_items:
		cluster_index = 0
		similarity = -1
		loop_index = 0
		for centroid in centroids:
			c_sim = similarity_function(item, centroid)
			if c_sim > similarity:
				simarilty  = c_sim
				cluster_index = loop_index
			loop_index += 1 
		clusters[cluster_index].append(item)
	centroids = [centroidify(cluster) for cluster in clusters]

	for i in xrange(0, 4):
		for cluster in clusters:
			del cluster[:]
		for item in items:
			cluster_index = 0
			similarity = -1
			loop_index = 0
			for centroid in centroids:
				c_sim = similarity_function(item, centroid)
				if c_sim > similarity:
					simarilty  = c_sim
					cluster_index = loop_index
				loop_index += 1
			clusters[cluster_index].append(item)
		centroids = [centroidify(cluster) for cluster in clusters]

	return clusters

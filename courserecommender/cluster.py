from itertools import groupby
from random import sample
import math
from models import Ranking, User		
		
def centroidify(cluster): 
	cluster_size = len(cluster)
	if cluster_size == 0:
		return User(rankings=[])
	
	average_rankings = []
	rankings = Ranking.find_all_by_user_ids(u.id for u in cluster)
	
	key = lambda r: r.course_id
	for course_id, group in groupby(sorted(rankings, key=key), key):
		average = sum(r.value for r in group) / float(cluster_size)
		average_rankings.append(Ranking(course_id = course_id, value = average))
			
	return User(rankings = average_rankings)
		
				
def cos_similarity(a, b):
	a_rankings = a.rankings
	b_rankings = b.rankings
	if len(a_rankings) == 0 or len(b_rankings) == 0:
		return 0.0
		
	dot_product = 0
	a_mag = 0
	b_mag = 0
	
	for a_rank in a_rankings:
		for b_rank in b_rankings:
			if a_rank.course_id == b_rank.course_id:
				dot_product += b_rank.value*a_rank.value
				
	for a_rank in a_rankings:
		a_mag += float(a_rank.value) ** 2
	a_mag = math.sqrt(a_mag)
		
	for b_rank in b_rankings:
		b_mag += float(b_rank.value) ** 2
	b_mag = math.sqrt(b_mag)
	
	if b_mag == 0 or a_mag == 0:
		return 0.0

	return dot_product / float(a_mag*b_mag)
	
	
def clusterize(items, k, similarity_function, iterations):
	centroids = sample(items, k)
	
	for i in xrange(iterations):
		clusters = [[] for i in xrange(k)]
		for item in items:
			cluster_index, similarity = max(
				enumerate(similarity_function(item, centroid) for centroid in centroids), 
				key=lambda (index,similarity): similarity
			)
			clusters[cluster_index].append(item)
		centroids = [centroidify(cluster) for cluster in clusters]

	return clusters

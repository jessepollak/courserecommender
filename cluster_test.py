import sys, os.path
project_parent = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_parent)

from courserecommender import cluster
from courserecommender import server
from courserecommender.models import *
from random import randint, choice

Base._session = server.db()

r1 = Ranking(course_id = 1, value = 2, user_id = 1)
r2 = Ranking(course_id = 2, value = -2, user_id = 1)
r3 = Ranking(course_id = 3, value = 1, user_id = 1)
r4 = Ranking(course_id = 4, value = 0, user_id = 1)
r5 = Ranking(course_id = 5, value = 1, user_id = 1)

user_1 = User(id = 1, rankings = [r1, r2, r3, r4, r5])

r6 = Ranking(course_id = 1, value = 1, user_id = 2)
r7 = Ranking(course_id = 2, value = 1, user_id = 2)
r8 = Ranking(course_id = 3, value = -2, user_id = 2)
r9 = Ranking(course_id = 4, value = 2, user_id = 2)
r10 = Ranking(course_id = 5, value = -1, user_id = 2)
r11 = Ranking(course_id = 6, value = 2, user_id = 2)

user_2 = User(id = 2, rankings = [r6, r7, r8, r9, r10, r11])

#user_store.save([user_1, user_2])
#ranking_store.save([r1, r2, r3, r4,r5,r6,r7,r8,r9,r10,r11])

for i in xrange(0, 20):
	user = User()
	user.save()
	
	
	r = list(xrange(1, 20))
	for i in xrange(1, randint(2, 20)):
		c = choice(r)
		r.remove(c)
		rank = Ranking(course_id = c, user_id = user.id, value = randint(-2,2))
		rank.save()
	print user
	

	
print len(User.all())
clusters = cluster.clusterize(User.all(), 5, cluster.cos_similarity, 5)
for c in clusters:
	print "Cluster: "
	for item in c:
		print item
		print [(r.value, r.course_id) for r in item.rankings]
			
	
	

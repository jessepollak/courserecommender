import flask
from itertools import groupby
import math
import random
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
import pickle

Base = declarative_base()
from sqlalchemy import Column, ForeignKey, Integer, String, Text

def init(url, echo=True):
	engine = create_engine(url, echo=echo)
	return sessionmaker(bind=engine)

class Store:
	_session = None
	@classmethod
	def session(klass):
		return klass._session or flask.g.db
	@classmethod
	def all(klass):
		return klass.session().query(klass).all()
	def save(self):
		self.__class__.session().add(self)
		self.__class__.session().commit()


class User(Base, Store):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String)
	cluster_id = Column(Integer, ForeignKey("clusters.id"))
	cluster = relationship("Cluster", backref=backref("users"))

	def recommended_courses(self):
		users_in_cluster = self.cluster.users[:]
		users_in_cluster.remove(self)
		random_users = random.sample(users_in_cluster, min(5, len(users_in_cluster)))

		good_courses = [u.good_courses() for u in random_users]
		course_recommendations = []
		for courses in good_courses:
			for course in courses:
				if not course in self.courses() and not course in course_recommendations:
					course_recommendations.append(course)
		
		return random.sample(course_recommendations, min(5, len(course_recommendations)))

	def courses(self):
		return self.__class__.session().query(Course).join("rankings", "user").filter(User.id == self.id).all()

	def good_courses(self):
		return self.__class__.session().query(Course).join("rankings", "user").filter(User.id == self.id).filter(Ranking.value > 0).all()

	@classmethod
	def similarity(klass, a, b):
		# Cosine Similarity
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

	def __repr__(self):
		return "<User id=%s, username=%s>" % (self.id, self.username)

class Ranking(Base, Store):
	__tablename__ = 'rankings'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	course_id = Column(Integer, ForeignKey('courses.id'))
	value = Column(Integer)
	user = relationship("User", backref=backref("rankings"))
	course = relationship("Course", backref=backref("rankings"))

	@classmethod
	def find_all_by_user_ids(klass, user_ids):
		return klass.session().query(Ranking).filter(Ranking.user_id.in_(user_ids)).all()
		
class Course(Base, Store):
	__tablename__ = 'courses'

	id = Column(Integer, primary_key=True)
	name = Column(String)

class Cluster(Base, Store):
	__tablename__ = 'clusters'

	id = Column(Integer, primary_key=True)
	centroid = Column(Text)
	
	def get_centroid(self):
		return pickle.loads(self.centroid)
		
	def set_centroid(self, rankings):
		self.centroid = pickle.dumps(self.centroid)
	
	@classmethod
	def make_clusters(klass):
		clusters = Cluster.clusterize(User.all(), 5, User.similarity, 5)
		klass.session().execute("DELETE FROM 'clusters'")
		# TODO LATER: RACE CONDITIONS. What happens if a user is added right now?
		for users, centroid in clusters:
			c = Cluster()
			c.set_centroid(centroid)
			c.save()
			for user in users:
				user.cluster_id = c.id
				user.save()

	@classmethod
	def add_user(klass, user):
		clusters = klass.all()
		centroids = [cluster.get_centroid() for cluster in clusters]
		cluster_index, similarity = max(
			enumerate(User.similarity(item, centroid) for centroid in centroids), 
			key=lambda (index,similarity): similarity
		)
		best_cluster = clusters[cluster_index]
		user.cluster_id = best_cluster.id
		user.save()

	@classmethod
	def centroidify(klass, cluster): 
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
		
	@classmethod
	def clusterize(klass, items, k, similarity_function, iterations):
		centroids = random.sample(items, k)
		
		for i in xrange(iterations):
			clusters = [[] for i in xrange(k)]
			for item in items:
				cluster_index, similarity = max(
					enumerate(similarity_function(item, centroid) for centroid in centroids), 
					key=lambda (index,similarity): similarity
				)
				clusters[cluster_index].append(item)
			centroids = [Cluster.centroidify(cluster) for cluster in clusters]

		return zip(clusters, centroids)
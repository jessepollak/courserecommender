import flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
import pickle

Base = declarative_base()
from sqlalchemy import Column, ForeignKey, Integer, String, Text

def init(url, echo=False):
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

	def __repr__(self):
		return "<User id=%s, username=%s>" % (self.id, self.username)

class Ranking(Base, Store):
	__tablename__ = 'rankings'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	course_id = Column(Integer, ForeignKey('courses.id'))
	value = Column(Integer)
	user = relationship("User", backref=backref("rankings"))

	@classmethod
	def find_all_by_user_ids(klass, user_ids):
		return klass.session().query(Ranking).filter(Ranking.user_id.in_(user_ids)).all()
		
class Course(Base, Store):
	__tablename__ = 'courses'

	id = Column(Integer, primary_key=True)

class Cluster(Base, Store):
	__tablename__ = 'clusters'

	id = Column(Integer, primary_key=True)
	centroid = Column(Text)
	
	def get_centroid(self):
		return pickle.loads(self.centroid)
		
	def set_centroid(self, rankings):
		self.centroid = pickle.dumps(self.rankings)
	
	@classmethod
	def add_user(klass, user):
		clusters = klass.all()
		centroids = [cluster.get_centroid() for cluster in clusters]
		cluster_index, similarity = max(
			enumerate(similarity_function(item, centroid) for centroid in centroids), 
			key=lambda (index,similarity): similarity
		)
		best_cluster = clusters[cluster_index]
		user.cluster_id = best_cluster.id
		user.save()
			
		

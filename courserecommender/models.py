import flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()
from sqlalchemy import Column, ForeignKey, Integer, String

def init(url):
	engine = create_engine(url, echo=True)
	return sessionmaker(bind=engine)

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	username = Column(String)

class UserStore:
	def __init__(self, session):
		self.session = session
	def all(self):
		return self.session.query(User).all()
	def save(self, user):
		self.session.add(user)
		self.session.commit()

class Ranking(Base):
	__tablename__ = 'rankings'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	user = relationship("User", backref=backref("rankings"))

class RankingStore:
	def __init__(self, session):
		self.session = session
	def find_all_by_user_ids(self, user_ids):
		return self.session.query(Ranking).filter(Ranking.user_id.in_(user_ids)).all()

"""
class CourseStore:
	def __init__(self, session):
		self.session = session
	def all(self):
		return self.session.query(Course).all()

class Course(Model):
	__
	fields = ["id", "title"]

class CourseStore(Store):
	model = Course
	table_name = "courses"

class Ranking(Model):
	fields = ["id", "value", "course_id", "user_id"]

class RankingStore(Store):
	model = Ranking
	table_name = "rankings"
	def find_all_by_user_ids(self, user_ids):
		return self.select_where_in('user_id', user_ids)

class User(Model):
	fields = ["id", "username", "cluster_id"]
	rankings = False

class UserStore(Store):
	model = User
	table_name = "users"

	def all_with_rankings(self):


class Cluster(Model):
	fields = ["id"]

class ClusterStore(Store):
	model = Cluster
	table_name = "clusters"
"""
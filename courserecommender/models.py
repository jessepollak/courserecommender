import flask
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker

Base = declarative_base()
from sqlalchemy import Column, ForeignKey, Integer, String

def init(url):
	engine = create_engine(url, echo=True)
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

	
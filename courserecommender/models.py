from contextlib import closing

class Store:
	def __init__(self, connection, strategy):
		self.connection = connection
		self.strategy = strategy
	def cursor(self):
		return closing(self.connection.cursor())
	def commit(self):
		self.connection.commit()
	def to_models(self, seq):
		return map(
			lambda row: self.model(**self.tuple_to_dict(row)),
			seq
		)
	def tuple_to_dict(self, tuple):
		return { key: value for key, value in zip(self.model.fields, tuple) }
	def select(self, suffix="", values=[]):
		with self.cursor() as c:
			return self.to_models(
				c.execute("SELECT * FROM '%s' %s" % (self.table_name, suffix), values)
			)
	def select_where_in(self, field, values):
		parameters = ", ".join(["?"] * len(values))
		return self.select("WHERE '%s'.'%s' IN (%s)" % (self.table_name, field, parameters), values)
	def all(self):
		return self.select()
	def save(self, instances):
		new = [i for i in instances if i.id == None]
		old = [i for i in instances if i.id != None]

		# HACKY HACKY HACKY
		pk = self.model.fields[0]
		with self.cursor() as c:
			for i in new:
				rowid = self.strategy.insert(c, self.table_name, pk, i.to_list())
				setattr(i, pk, rowid)
			for i in old:
				set_template = ", ".join("'%s'=?" % f for f in self.model.fields)
				values = i.to_list() + [getattr(i, pk)]
				c.execute("UPDATE '%s' SET %s WHERE '%s'=?" % (self.table_name, set_template, pk), values)
			self.commit()

class Model:
	def __init__(self, **opts):
		for field in self.fields:
			setattr(self, field, opts.get(field, None))
	def __repr__(self):
		attributes = [field + "=" + str(getattr(self, field)) for field in self.fields]
		return "<" + self.__class__.__name__ + " " + ", ".join(attributes) + ">"
	def to_list(self):
		return [getattr(self, field) for field in self.fields]

class Course(Model):
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

class UserStore(Store):
	model = User
	table_name = "users"

class Cluster(Model):
	fields = ["id"]

class ClusterStore(Store):
	model = Cluster
	table_name = "clusters"
class Ranking:
	
	def __init__(self, **opts):
		self.course_id = opts['course_id']
		self.value = opts['value']
		self.user_id = opts['user_id']
	
	
class User:
	
	def __init__(self, **opts):
		self.id = opts['id']
		self.rankings = opts.get('rankings', [])
import sys
import os
import string
parent = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent)

course_file = os.path.join(parent, 'tasks', 'unique_course_names.txt')

import courserecommender.server
session = courserecommender.server.db()
from courserecommender.models import *

Store._session = session

f = open(course_file, 'r')
line = f.readline()
while(line != ""):
	title = line.replace("\n", "")
	c = Course()
	c.name = title
	c.save()
	line = f.readline()
f.close()

	
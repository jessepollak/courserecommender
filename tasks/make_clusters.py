import sys
import os
parent = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent)

import courserecommender.server
session = courserecommender.server.db()
from courserecommender.models import *

Store._session = session

k = int(sys.argv[1])
Cluster.make_clusters(k)

print [len(c.users) for c in Cluster.all()]
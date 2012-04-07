import sys
import os
parent = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent)

import courserecommender.server
session = courserecommender.server.db()
from courserecommender.models import *

Store._session = session
Base.metadata.create_all(session.get_bind())
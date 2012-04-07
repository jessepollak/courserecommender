CREATE TABLE 'courses' ('id' integer primary key, 'title' string);
CREATE TABLE 'users' ('id' integer primary key, 'username' string, 'cluster_id' integer);
CREATE TABLE 'rankings' ('id' integer primary key, 'value' integer, 'course_id' integer, 'user_id' integer);
CREATE TABLE 'clusters' ('id' integer primary key);
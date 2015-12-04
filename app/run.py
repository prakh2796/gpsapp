
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, jsonify
import json
import MySQLdb
import MySQLdb.cursors
from settings import *
import requests
from math import radians, asin, sin, cos,sqrt

app = Flask(__name__)

def get_db():
    """Initializes the database."""
    db = MySQLdb.connect(DB_CONN['HOST'], DB_CONN['USERNAME'], DB_CONN['PASSWORD'], DB_CONN['DATABASE'])
    return db, db.cursor()

def is_inside(lat1, lon1, lat2, lon2, radius=10):
	# Haversine
	lat1, lon1, lat2, lon2 = map(radians, [lat1,lon1,lat2,lon2])
	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
	c = 2 * asin(sqrt(a))
	km = 6367 * c
	if km <= radius:
		return True
	else:
		return False


@app.route('/', methods=['GET','POST'])
def calc():
	print 'x'
	x = []
	y = []
	item_id = []
	item_list = []
	db,cursor=get_db()
	request.form = json.loads(request.data)
	latitude = float(request.form['latitude'])
	longitude = float(request.form['longitude'])
	# print latitude
	# print longitude
	cursor.execute('SELECT id,lat,longi FROM item')
	entries = cursor.fetchall()
	for a,b,c in entries:
		item_id.append(a)
		x.append(float(b))
		y.append(float(c))
	for i in range(0,len(item_id)):
		status = is_inside(latitude,longitude,x[i],y[i])
		if status:
			cursor.execute('SELECT name FROM item WHERE id="{0}"'.format(item_id[i]))
			entries = cursor.fetchall()
			# print entries
			item_list.append(str(entries[0]))
		# else:
		# 	print'No items found'
	print item_list
	return jsonify(status='success', msg='Done', item_list=item_list)
	"""
	return 'a'
	# cursor.execute('SELECT * FROM item')
	# entries = cursor.fetchall()
	# print entries
	# return 'a'
	"""


if __name__=='__main__':
    app.run(debug=True)


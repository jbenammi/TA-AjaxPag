from flask import Flask, render_template, request
import math, datetime
import decimal
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app, 'lead_gen_business')

@app.route('/')
def main():
	return render_template('main.html')

@app.route('/leads', methods = ['GET', 'POST'])
def leadLinks():
	query2 = "SELECT count(id) AS numLeads FROM leads WHERE (first_name LIKE concat('%',:search,'%') OR last_name LIKE concat('%',:search,'%')) AND (registered_datetime > :dateFrom AND registered_datetime < :dateTo)"
	info2 = {
		'search': request.form['name'],
		'dateFrom': request.form['dateFrom']+'%',
		'dateTo': request.form['dateTo']+ 'null'
	}
	numLeads = mysql.query_db(query2, info2);
	numLeads = math.ceil(float(numLeads[0]['numLeads'])/5);
	links = [];
	num = 0;
	for x in xrange(0,int(numLeads)):
		links.append("/leads/show/"+str(num))
		num += 5
	return render_template('links.html', links = links)

@app.route('/leads/show/<num>', methods = ['GET','POST'])
def showLeads(num):
	query1 = "SELECT * FROM leads WHERE (first_name LIKE concat('%',:search,'%') OR last_name LIKE concat('%',:search,'%')) AND (registered_datetime > :dateFrom AND registered_datetime < :dateTo) LIMIT :num, 5"
	info1 = {
		'search': request.form['name'],
		'dateFrom': request.form['dateFrom']+'%',
		'dateTo': request.form['dateTo']+'null',
		'num': int(num)
	}
	leads = mysql.query_db(query1, info1)
	return render_template('table.html', leads = leads)

app.run(debug=True)
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
	query1 = "SELECT count(id) AS numLeads FROM leads"
	query2 = "SELECT count(id) AS numLeads FROM leads WHERE (first_name LIKE concat('%',:search,'%') OR last_name LIKE concat('%',:search,'%')) AND (registered_datetime BETWEEN :dateFrom AND :dateTo)"
	query3 = "SELECT registered_datetime FROM leads ORDER BY registered_datetime LIMIT 1"
	dateFrom = mysql.query_db(query3)
	dateTo = datetime.datetime.now().strftime('%Y-%m-%d')
	if request.method == 'POST':
		if len(request.form['dateFrom']) == 0:
			dFrom = dateFrom[0]['registered_datetime'].strftime('%Y-%m-%d')
		else:
			dFrom = request.form['dateFrom']
		if len(request.form['dateTo']) == 0:
			dTo = dateTo
		else:
			dTo = request.form['dateTo']
		info2 = {
			'search': request.form['name'],
			'dateFrom': dFrom,
			'dateTo': dTo
		}
		numLeads = mysql.query_db(query2, info2);
	else:
		numLeads = mysql.query_db(query1);
	numLeads = float(numLeads[0]['numLeads']);
	numLeads = math.ceil(numLeads/5);
	numLeads = int(numLeads);
	links = [];
	num = 0;
	for x in xrange(0,numLeads):
		links.append("/leads/show/"+str(num))
		num += 5
	return render_template('links.html', links = links)


@app.route('/leads/show/<num>', methods = ['GET','POST'])
def showLeads(num):
	query1 = "SELECT DISTINCT * FROM leads WHERE (first_name LIKE concat('%',:search,'%') OR last_name LIKE concat('%',:search,'%')) AND (registered_datetime BETWEEN :dFrom AND :dTo) LIMIT :num, 5"
	query2 = "SELECT * FROM leads LIMIT :num, 5"
	query3 = "SELECT registered_datetime FROM leads ORDER BY registered_datetime LIMIT 1"
	dateFrom = mysql.query_db(query3)
	dateTo = datetime.datetime.now().strftime('%Y-%m-%d')
	if request.method == 'POST':
		if len(request.form['dateFrom']) == 0:
			dFrom = dateFrom[0]['registered_datetime'].strftime('%Y-%m-%d')
		else:
			dFrom = request.form['dateFrom']
		if len(request.form['dateTo']) == 0:
			dTo = dateTo
		else:
			dTo = request.form['dateTo']
		info1 = {
			'search': request.form['name'],
			'dFrom': dFrom,
			'dTo': dTo,
			'num': int(num)
		}
		leads = mysql.query_db(query1, info1)
	else:
		info2 = {
			'num': int(num)
		}
		leads = mysql.query_db(query2, info2)
	return render_template('table.html', leads = leads)


app.run(debug=True)
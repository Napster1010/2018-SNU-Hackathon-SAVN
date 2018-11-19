from flask import Flask, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from flask import json
import os
mysql = MySQL()
app = Flask(__name__)

#database configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'dell_database'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#check case for authentication
@app.route('/Authenticate')
def Authenticate():
    id = request.args.get('id')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from product_details where ID=" + id)
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

#search inventory based on product id
@app.route('/inventory/search')
def inventory_search():
    product_Id = request.args.get('product_Id')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from product_details where product_serial_number = " + product_Id)
    row_headers=[x[0] for x in cursor.description]
    data = cursor.fetchall()
    json_data = []
    for result in data:
        json_data.append(dict(zip(row_headers,result)))
    return json.dumps(json_data)

#login page
@app.route('/user/login')
def verify_user():
    user = request.args.get('userId')
    password = request.args.get('password')
    if (user == 'u101' and password == 'pass@123'):
        return 'success'

#add 3PL logistics
@app.route('/logistics', methods = ['POST'])
def add_logistics():
    cursor = mysql.connect().cursor()
    req_data = request.get_json()
    location_id = req_data['location_id']
    location_name = req_data['location_name']
    location_loc = req_data['location_loc']
    cursor.execute("INSERT into logistics_details values(location_id, location_name, location_loc)")

#move product based on forecast
@app.route('/inventory/move', methods = ['POST'])
def move_product():
    product_id = request.form['product_id']
    src_log_id = request.form['src_log_id']
    des_log_id = request.form['des_log_id']
    quantity = request.form['quantity']

if __name__ == '__main__':
    app.run(debug = True, port = 7000)

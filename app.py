import json
from flask import Flask, request, render_template, jsonify
import mysql.connector
from threading import Thread
app = Flask(__name__)

# db connection details change later depending on how ronald configs 
db_name = "db_name"
username = "username"
password = "password"

#example db schema 
# id 
# time taken time/day/month/year
# people
# total chair 
# taken chair
# total table 
# taken table 

# Issue - need to implement some thing to only pull the mot recent information 
# otherwise we would lose PAST data 
data = dict()

# Database connection details (replace with yours)
db_name = "your_database_name"
username = "your_username"
password = "your_password"

try:
    connection = mysql.connector.connect(
        host="localhost",
        user=username,
        password=password,
        database=db_name
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM occupancy ORDER BY created_at DESC LIMIT 3")
    cursor.fetchall()
    # (data) should be a dictionary formatted -> 'location name' = (dict) column name : column information
    # it would be nice to have a time taken in the data base 
    cols = [description[0] for description in cursor.description]
    for row in cursor: 
        location = row[0]
        location_info = dict(zip(cols[1:], row[1:])) 
        data[location] = location_info

except mysql.connector.Error as err:
    print("Error connecting to database:", err)

finally:
    if connection:
        connection.close()
    print("Connection closed.")


# the rendered template takes a dictionary of element id's and values 
# e.g. {{ population }}  --> value for population will be put in that space 
# THERE IS PROBABLY A BETTER WAY TO DO THIS BUT IT WOULD REQUIRE MORE COMPLEX FLASK
        # total population
        # population, open tables and chairs on each floor 
context = {}
context['total_population'] = data[1]['population'] + data[2]['population'] + data[3]['population']
for floor in (1, 2, 3):
    open_tables = data[floor]['total_tables'] - data[floor]['taken_tables']
    open_chairs = data[floor]['total_chairs'] - data[floor]['taken_chairs']
    context['floor_' + str(floor) + '_otables'] = open_tables
    context['floor_' + str(floor) + '_ochairs'] = open_chairs

# access in html template as floor_#_otables 


@app.route('/', methods = ['GET', 'POST'])
def display_home():
    if request.method == 'GET':
        return render_template('index.html', **context) 
    else:
        pass # idk what to put here 
        



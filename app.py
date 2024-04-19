# HTML RENDERING IS READY TO GO WE JUST NEED TO FORMAT THE WEBSITE AND ILL CHANGE THE VARIABLE NAMES 
# 


import json
from flask import Flask, request, render_template, jsonify
import pymssql
from threading import Thread
app = Flask(__name__)

# Issue - need to implements
#  some thing to only pull the mot recent information 
# otherwise we would lose PAST data 
data = dict()

with open('login.json') as f:
    db_config = json.load(f)
    conn = pymssql.connect(
        server=db_config['server'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        as_dict = True
    )         
    cursor = conn.cursor()
    cursor.execute("SELECT TOP 3 * FROM [dbo].[occupancy] ORDER BY time DESC, id;")
    rdata = cursor.fetchall()

    # (data) should be a dictionary formatted -> 'location name' = (dict) column name : column information
    cols = [description[0] for description in cursor.description] #first col is id or floor number 

    for row in rdata:
        location = row['id']
        data[location] = {key: value for key, value in row.items() if key != 'id'}

print(data)
conn.close()
# the rendered template takes a dictionary of element id's and values 
# e.g. {{ population }}  --> value for population will be put in that space 
# THERE IS PROBABLY A BETTER WAY TO DO THIS BUT IT WOULD REQUIRE MORE COMPLEX FLASK
        # total population
#         # population, open tables and chairs on each floor 
context = {}
context['total_population'] = data.get(1).get('population')+ data.get(2).get('population') + data.get(3).get('population')
for floor in (1, 2, 3):



    floor_row  = data.get(floor)
    print(floor_row)
    print(floor_row.get('total_table'))
    #open_tables = int(data.get(floor).get('total_tables')) - int(data.get(floor).get('taken_tables'))
    #open_chairs = int(data.get(floor).get('total_chairs')) - int(data.get(floor).get('taken_chairs'))
    #context['floor_' + str(floor) + '_otables'] = open_tables
    #context['floor_' + str(floor) + '_ochairs'] = open_chairs

# access in html template as floor_#_otables 
@app.route('/', methods = ['GET', 'POST'])
def display_home():
    if request.method == 'GET':
        return render_template('index.html', **context) 
    else:
        pass # idk what to put here 
        



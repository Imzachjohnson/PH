from flask import Flask, jsonify, request, render_template,jsonify,make_response,redirect
import requests
import json
import humanize
from datetime import datetime
import time
import dateparser
import os
import pandas as pd
from io import StringIO
import io
import csv
from geojson import MultiPoint
from geojson import Feature, Point,FeatureCollection
import geojson
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
from flask_caching import Cache



app = Flask(__name__, static_url_path='/static')
api_url = 'http://localhost:5000/create-row-in-gs'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SECRET_KEY'] = '2343252341231232342'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


#API Constants
API_URL = "https://kc.humanitarianresponse.info/api/v1/data/"
API_SECRET="3c167da4420aa1f521081213e969cb40f4d3dad8"
FORM_ID = "361960"


config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}


app.config.from_mapping(config)
cache = Cache(app)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')

#Change tag text to human readable
def tagconversion(tagtext):
    if tagtext == "red__unsafe":
        tagtext = "Unsafe"
    elif tagtext == "yellow__restri":
        tagtext = "Restricted"
    elif tagtext == "green__no_even":
        tagtext = "Safe"
    else:
        tagtext = "Unknown"
    return tagtext

def damageconversion(tagtext):
    if tagtext == "none_minor__0_":
        tagtext = "None/Minor"
    elif tagtext == "moderate__10_5":
        tagtext = "Moderate"
    elif tagtext == "severe__50_100":
        tagtext = "Severe"
    else:
        tagtext = "Unknown"
    return tagtext




#Main index route
@app.route('/')
@login_required
def index():

    return render_template('dashboard.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['user']).first()
        if user:
                if user.password == request.form['password']:
                    login_user(user)
                    return redirect('/')

    return render_template('login.html')

#Main index route
@app.route('/download', methods=['GET', 'POST']) 
def download():
   
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID ,  headers={'Authorization': 'Token ' + API_SECRET})
    response = r.text
    data = pd.read_json(StringIO(response))
    # header = ["InviteTime (Oracle)", "Orig Number", "Orig IP Address", "Dest Number"]
   # columns = header

    return str(data.to_csv())

@app.route('/geojson')
def convertogeojson():
    data = []
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID ,  headers={'Authorization': 'Token ' + API_SECRET})
    response = r.json()
    for item in response:
         image = ""
         if "assessment_result/GPS_Coordinates" in item:
            coordinates = item['assessment_result/GPS_Coordinates'].split(" ")

            if "_attachments" in item and len(item["_attachments"]) > 0:
                image = item["_attachments"][0]['download_large_url']
            else:
                image = "No Image"
            
            itemid = item['_id']

            latitude = coordinates[0]
            longitude = coordinates[1]
            my_point = Point((float(longitude), float(latitude)))
            my_feature = Feature(geometry=Point(my_point), properties={'name':item['identifiers/Building_ID'], 'id':itemid, 'image':image})
            data.append(my_feature)
    feature_collection = FeatureCollection(data)
    return str(feature_collection)


#Assessment list route
@app.route('/assessments')
@cache.cached(timeout=50)
@login_required
def assessmentlist():
    return render_template('assessment-list.html')





    
#Return all report instances from a form id and process JSON
@app.route('/all-data', methods = ['GET'])
def all_data_request():
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID ,  headers={'Authorization': 'Token ' + API_SECRET})
    response = r.json()
    finalresponse = []
    image = ""
    offoundation = ""

    for item in response:
       estimateddamagesingle = ""
       leaning = ""
       collapse = ""
       ptoa = ""
       damageother = ""

       if "_attachments" in item and len(item["_attachments"]) > 0:
            image = item["_attachments"][0]['download_medium_url']
       else:
            image = "/static/images/no-image-wide.jpg"
            
       if "assessment_result/GPS_Coordinates" in item:

        if "Summary_of_findings/Estimated_Building_Damage" in item:    
           estimateddamagesinglelist = item['Summary_of_findings/Estimated_Building_Damage'].split("_")
           if len(estimateddamagesinglelist) > 0:
            try:
                estimateddamagesingle = estimateddamagesinglelist[1]
            except:
                estimateddamagesingle = estimateddamagesinglelist[0]


        coordinates = item['assessment_result/GPS_Coordinates'].split(" ")
        tag = tagconversion(item['Assessment_Result_001/Assessment_Result_002'])
        if "total_damage_status/Building_off_foundation" in item:
            offoundation = damageconversion(item['total_damage_status/Building_off_foundation'])
        
        if "total_damage_status/Building_or_storey_leaning" in item:
            leaning = damageconversion(item['total_damage_status/Building_or_storey_leaning'])
        
        if "total_damage_status/Collapse_or_partial_collapse" in item:
            collapse = damageconversion(item['total_damage_status/Collapse_or_partial_collapse'])
        
        if "total_damage_status/Pounding_to_adjecent" in item:
            ptoa = damageconversion(item['total_damage_status/Pounding_to_adjecent'])

        if "total_damage_status/Other_damage_status" in item:
            damageother = damageconversion(item['total_damage_status/Other_damage_status'])

        assessment =  {'id':item['_id'],
        'latitude': coordinates[0],
        'longitude': coordinates[1],
        'tag': tag,
        'buildingname': item['identifiers/Building_ID'],
        'image': image,
        'estimateddamage': item['Summary_of_findings/Estimated_Building_Damage'].replace("_","-") + "%",
        'estimateddamagesingle': estimateddamagesingle,
        'occupants' : item['assessment_result/Number_of_occupants'],
        'primaryoccupancy': item['Primary_Occupancy'].replace("_"," ").capitalize(),
        'offoundation': offoundation,
        'leaning': leaning,
        "collapse" : collapse,
        "ptoa" :ptoa,
        'damageother' : damageother
        }
        finalresponse.append(assessment)

    return  json.dumps(finalresponse)


#return a single report instance from an instance id
@app.route('/<id>')
@login_required
def single_data_request(id):
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID + '/' + id ,  headers={'Authorization': 'Token ' + API_SECRET})

    response = r.json()
    
    coordinates = response['assessment_result/GPS_Coordinates'].split(" ")
    area = response['identifiers/Inspected_area'].replace("_"," ")
    rooftype = response['type_roof/Type_of_Roof'].replace("_"," ").capitalize()
    primaryoccupancy = response['Primary_Occupancy'].replace("_"," ").capitalize()
    soil = response['soil_slope/Soil_Description'].replace("_"," ").capitalize()
    estimateddamage = response['Summary_of_findings/Estimated_Building_Damage'].replace("_","-") + "%"
    if "_attachments" in response and len(response["_attachments"]) > 0:
        image = response["_attachments"][0]['download_medium_url']
    else:
        image = "/static/images/no-image.jpg"

    tag = response['Assessment_Result_001/Assessment_Result_002']  
    my_time = dateparser.parse(response['identifiers/Date_Time'])
    date = humanize.naturaldate(my_time)

    builtresponse= {
        'id':response['_id'],
        'BuildingName': response['identifiers/Building_ID'],
        'inspector': response['Inspector_ID'],
        'contact': response['assessment_result/Contact_person'],
        'phone': response['assessment_result/Phone_number'],
        'address': response['assessment_result/Address'],
        'assessmenttype': response['Assessment_Type'].capitalize(),
        'latitude': coordinates[0],
        'longitude': coordinates[1],
        'cost': response['Summary_of_findings/Estimated_Repair_Cost_Dollars'],
        'occupants' : response['assessment_result/Number_of_occupants'],
        'yearbuilt' : response['assessment_result/Building_built_in_year'],
        'storiesabove' : response['assessment_result/Number_of_stories_above_ground'],
        'storiesbelow' : response['assessment_result/Number_of_stories_below_ground'],
        'submitedby' : response['_submitted_by'],
        'inspectedarea' : area.capitalize(),
        'approxarea' : response['assessment_result/Approximate_footprint_area_sq_m'],
        'tag' : tagconversion(response['Assessment_Result_001/Assessment_Result_002']),
        'inspectorid' : response['Inspector_ID'], 
        'assessmentdate' : date.capitalize(),
        'rooftype' :rooftype,
        'primaryoccupancy': primaryoccupancy,
        'estimateddamage': estimateddamage,
        'soil':  soil,
        'thumbnail':image
    }

    return render_template('details.html', data = builtresponse)



if __name__ == '__main__':
    
    app.run(debug=True)
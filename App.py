from flask import Flask, jsonify, request, render_template, make_response, redirect
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
from geojson import Feature, Point, FeatureCollection
import geojson
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask
from flask_caching import Cache
from datetime import datetime
from uuid import UUID
from typing import List, Any
from Assessments import Assessment


app = Flask(__name__, static_url_path='/static')
api_url = 'http://localhost:5000/create-row-in-gs'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/login.db'
app.config['SECRET_KEY'] = '2343252341231232342'


db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


# API Constants
API_URL = "https://kc.humanitarianresponse.info/api/v1/data/"
API_SECRET = "3c167da4420aa1f521081213e969cb40f4d3dad8"
FORM_ID = "361960"

# Cache config
config = {
    "DEBUG": True,
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 300
}


app.config.from_mapping(config)
cache = Cache(app)

# Pandas config
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


def create_assessment_list():

    try:

        data = []
        request_data = {'Authorization': 'Token ' + API_SECRET}
        r = requests.get(url=API_URL + FORM_ID,
                         headers={'Authorization': 'Token ' + API_SECRET})
        response = r.json()
    except:
        return

    # Initialize variables and final list for storage of parsed/validated assessments

    final_list = []
    uniqueid = "No Data"
    start = "No Data"
    end = "No Data"
    today = "No Data"
    inspector_id = "No Data"
    latitude = ""
    longitude = ""
    assessment_type = "No Data"
    identifiers_building_id = "No Data"
    identifiers_inspected_area = "No Data"
    identifiers_date_time = "No Data"
    assessment_result_building_name = "No Data"
    assessment_result_contact_person = "No Data"
    assessment_result_first_name = "No Data"
    assessment_result_phone_number = "No Data"
    assessment_result_address = "No Data"
    assessment_result_number_of_occupants = "No Data"
    assessment_result_building_built_in_year = "No Data"
    assessment_result_number_of_stories_above_ground = "No Data"
    assessment_result_number_of_stories_below_ground = "No Data"
    assessment_result_gps_coordinates = "No Data"
    assessment_result_approximate_footprint_area_sq_m = "No Data"
    soil_slope_soil_description = "No Data"
    soil_slope_site_slope_description = "No Data"
    type_construction_type_of_construction = "No Data"
    type_roof_type_of_roof = "No Data"
    building_shape_plan = "No Data"
    observed_irregularities_001_soft_story = "No Data"
    observed_irregularities_001_set_backs = "No Data"
    observed_irregularities_001_coupled_shear_walls = "No Data"
    observed_irregularities_001_shortened_columns = "No Data"
    observed_irregularities_001_pounding = "No Data"
    primary_occupancy = "No Data"
    total_damage_status_collapse_or_partial_collapse = "No Data"
    total_damage_status_building_or_storey_leaning = "No Data"
    total_damage_status_pounding_to_adjecent = "No Data"
    total_damage_status_building_off_foundation = "No Data"
    total_damage_status_other_damage_status = "No Data"
    structural_hazards_foundations = "No Data"
    structural_hazards_roof_floor_vertical_load_capacity = "No Data"
    structural_hazards_columns_pillasters_crack_spalled = "No Data"
    structural_hazards_slab_beam_joist_crack_spalled = "No Data"
    structural_hazards_walls_int_ext_cracking_collapse = "No Data"
    structural_hazards_other_damage_status_001 = "No Data"
    non_structural_hazards_parapet_canopy_or_stair_damage = "No Data"
    non_structural_hazards_cladding_and_window_systems = "No Data"
    non_structural_hazards_ceilings_and_lights_fixtures = "No Data"
    non_structural_hazards_interior_walls_partition = "No Data"
    non_structural_hazards_elevators = "No Data"
    non_structural_hazards_stairs_exits = "No Data"
    non_structural_hazards_electricity_gas_fuel = "No Data"
    non_structural_hazards_other_damage_status_002 = "No Data"
    geotechnical_slope_failure = "No Data"
    geotechnical_ground_movement_fissures = "No Data"
    geotechnical_liquefaction = "No Data"
    geotechnical_subterranean_structure_damage = "No Data"
    geotechnical_other_damage_status_003 = "No Data"
    summary_of_findings_annotate_image_widget = "No Data"
    summary_of_findings_estimated_building_damage = "No Data"
    summary_of_findings_estimated_repair_cost_dollars = "No Data"
    assessment_result_001_assessment_result_002 = "No Data"
    assessment_result_001_description = "No Data"
    version = "No Data"
    meta_instance_id = "No Data"
    xform_id_string = "No Data"
    uuid = "No Data"
    status = "No Data"
    geolocation = "No Data"
    submission_time = "No Data"
    tags = "No Data"
    notes = "No Data"
    validation_status = "No Data"
    submitted_by = "No Data"
    leaning = "No Data"
    collapse = "No Data"
    ptoa = "No Data"
    damageother = "No Data"
    largeimage = "No Image"
    mediumimage = "No Image"
    smallimage = "No Image"

    #Loop through JSON response and add key values to an Assessment object

    for a in response:

        if "_id" in a:
            uniqueid = a['_id']

        if "start" in a:
            start = a['start']

        if "end" in a:
            end = a['end']

        if "today" in a:
            collapse = a['today']

        if "inspector_id" in a:
            inspector_id = a['inspector_id']

        if "Assessment_Type" in a:
            assessment_type = a['Assessment_Type']

        if "identifiers/Building_ID" in a:
            identifiers_building_id = a['identifiers/Building_ID']

        if "identifiers/Inspected_area" in a:
            identifiers_inspected_area = a['identifiers/Inspected_area'].replace(
                "_", " ")

        if "identifiers/Date_Time" in a:
            try:
                my_time = dateparser.parse(response['identifiers/Date_Time'])
                identifiers_date_time = humanize.naturaldate(my_time)
            except:
                identifiers_date_time = "No Data"

        if "assessment_result/Building_Name" in a:
            assessment_result_building_name = a['assessment_result/Building_Name']

        if "assessment_result/Contact_person" in a:
            assessment_result_contact_person = a['assessment_result/Contact_person']

        if "assessment_result/First_Name" in a:
            assessment_result_first_name = a['assessment_result/First_Name']

        if "assessment_result/Phone_number" in a:
            assessment_result_phone_number = a['assessment_result/Phone_number']

        if "assessment_result/Address" in a:
            assessment_result_address = a['assessment_result/Address']

        if "assessment_result/Number_of_occupants" in a:
            assessment_result_number_of_occupants = a['assessment_result/Number_of_occupants']

        if "assessment_result/Building_built_in_year" in a:
            assessment_result_building_built_in_year = a['assessment_result/Building_built_in_year']

        if "assessment_result/Number_of_stories_above_ground" in a:
            assessment_result_number_of_stories_above_ground = a[
                'assessment_result/Number_of_stories_above_ground']

        if "assessment_result/Number_of_stories_below_ground" in a:
            assessment_result_number_of_stories_below_ground = a[
                'assessment_result/Number_of_stories_below_ground']

        if "assessment_result/GPS_Coordinates" in a:
            assessment_result_gps_coordinates = a['assessment_result/GPS_Coordinates']
            try:
                coordinates = assessment_result_gps_coordinates.split(" ")
                latitude = coordinates[0]
                longitude = coordinates[1]
            except:
                latitude = None
                longitude = None

        if "assessment_result/Approximate_footprint_area_sq_m" in a:
            assessment_result_approximate_footprint_area_sq_m = a[
                'assessment_result/Approximate_footprint_area_sq_m']

        if "soil_slope/Soil_Description" in a:
            soil_slope_soil_description = a['soil_slope/Soil_Description']

        if "soil_slope/Site_Slope_Description" in a:
            soil_slope_site_slope_description = a['soil_slope/Site_Slope_Description']

        if "type_construction/Type_of_Construction" in a:
            type_construction_type_of_construction = a['type_construction/Type_of_Construction']

        if "type_roof/Type_of_Roof" in a:
            type_roof_type_of_roof = a['type_roof/Type_of_Roof']

        if "Building_Shape_Plan" in a:
            building_shape_plan = a['Building_Shape_Plan']

        if "observed_irregularities_001/Soft_Story" in a:
            observed_irregularities_001_soft_story = a['observed_irregularities_001/Soft_Story']

        if "observed_irregularities_001/Set_Backs" in a:
            observed_irregularities_001_set_backs = a['observed_irregularities_001/Set_Backs']

        if "observed_irregularities_001/Coupled_Shear_Walls" in a:
            observed_irregularities_001_coupled_shear_walls = a[
                'observed_irregularities_001/Coupled_Shear_Walls']

        if "observed_irregularities_001/Shortened_Columns" in a:
            observed_irregularities_001_shortened_columns = a[
                'observed_irregularities_001/Shortened_Columns']

        if "observed_irregularities_001/Pounding" in a:
            observed_irregularities_001_pounding = a['observed_irregularities_001/Pounding']

        if "Primary_Occupancy" in a:
            primary_occupancy = a['Primary_Occupancy'].replace(
                "_", " ").capitalize()

        if "total_damage_status/Collapse_or_partial_collapse" in a:
            total_damage_status_collapse_or_partial_collapse = a[
                'total_damage_status/Collapse_or_partial_collapse']

        if "total_damage_status/Building_or_storey_leaning" in a:
            total_damage_status_building_or_storey_leaning = a[
                'total_damage_status/Building_or_storey_leaning']

        if "total_damage_status/Pounding_to_adjecent" in a:
            total_damage_status_pounding_to_adjecent = a['total_damage_status/Pounding_to_adjecent']

        if "total_damage_status/Building_off_foundation" in a:
            total_damage_status_building_off_foundation = a['total_damage_status/Building_off_foundation']

        if "total_damage_status/Other_damage_status" in a:
            total_damage_status_other_damage_status = a['total_damage_status/Other_damage_status']

        if "structural_hazards/Foundations" in a:
            structural_hazards_foundations = a['structural_hazards/Foundations']

        if "structural_hazards/Roof_Floor_Vertical_Load_Capacity" in a:
            structural_hazards_roof_floor_vertical_load_capacity = a[
                'structural_hazards/Roof_Floor_Vertical_Load_Capacity']

        if "structural_hazards/Columns_Pillasters_Crack_Spalled" in a:
            structural_hazards_columns_pillasters_crack_spalled = a[
                'structural_hazards/Columns_Pillasters_Crack_Spalled']

        if "structural_hazards/Slab_Beam_Joist_Crack_Spalled" in a:
            structural_hazards_slab_beam_joist_crack_spalled = a[
                'structural_hazards/Slab_Beam_Joist_Crack_Spalled']

        if "structural_hazards/Walls_Int_Ext_Cracking_Collapse" in a:
            structural_hazards_walls_int_ext_cracking_collapse = a[
                'structural_hazards/Walls_Int_Ext_Cracking_Collapse']

        if "structural_hazards/Other_Damage_Status_001" in a:
            structural_hazards_other_damage_status_001 = a['structural_hazards/Other_Damage_Status_001']

        if "non_structural_hazards/Parapet_Canopy_or_Stair_Damage" in a:
            non_structural_hazards_parapet_canopy_or_stair_damage = a[
                'non_structural_hazards/Parapet_Canopy_or_Stair_Damage']

        if "non_structural_hazards/Cladding_and_Window_Systems" in a:
            non_structural_hazards_cladding_and_window_systems = a[
                'non_structural_hazards/Cladding_and_Window_Systems']

        if "non_structural_hazards/Ceilings_and_Lights_Fixtures" in a:
            non_structural_hazards_ceilings_and_lights_fixtures = a[
                'non_structural_hazards/Ceilings_and_Lights_Fixtures']

        if "non_structural_hazards/Interior_Walls_Partition" in a:
            non_structural_hazards_interior_walls_partition = a[
                'non_structural_hazards/Interior_Walls_Partition']

        if "non_structural_hazards/Elevators" in a:
            non_structural_hazards_elevators = a['non_structural_hazards/Elevators']

        if "non_structural_hazards/Stairs_Exits" in a:
            non_structural_hazards_stairs_exits = a['non_structural_hazards/Stairs_Exits']

        if "non_structural_hazards/Electricity_Gas_Fuel" in a:
            non_structural_hazards_electricity_gas_fuel = a['non_structural_hazards/Electricity_Gas_Fuel']

        if "non_structural_hazards/Other_Damage_Status_002" in a:
            non_structural_hazards_other_damage_status_002 = a[
                'non_structural_hazards/Other_Damage_Status_002']

        if "geotechnical/Slope_Failure" in a:
            geotechnical_slope_failure = a['geotechnical/Slope_Failure']

        if "geotechnical/Ground_Movement_Fissures" in a:
            geotechnical_ground_movement_fissures = a['geotechnical/Ground_Movement_Fissures']

        if "geotechnical/Liquefaction" in a:
            geotechnical_liquefaction = a['geotechnical/Liquefaction']

        if "geotechnical/Subterranean_Structure_Damage" in a:
            geotechnical_subterranean_structure_damage = a['geotechnical/Subterranean_Structure_Damage']

        if "geotechnical/Other_Damage_Status_003" in a:
            geotechnical_other_damage_status_003 = a['geotechnical/Other_Damage_Status_003']

        if "Summary_of_findings/annotate_image_widget" in a:
            summary_of_findings_annotate_image_widget = a['Summary_of_findings/annotate_image_widget']

        if "Summary_of_findings/Estimated_Building_Damage" in a:
            summary_of_findings_estimated_building_damage = a[
                'Summary_of_findings/Estimated_Building_Damage']

        if "Summary_of_findings/Estimated_Repair_Cost_Dollars" in a:
            summary_of_findings_estimated_repair_cost_dollars = a[
                'Summary_of_findings/Estimated_Repair_Cost_Dollars']

        if "Assessment_Result_001/Assessment_Result_002" in a:
            assessment_result_001_assessment_result_002 = a['Assessment_Result_001/Assessment_Result_002']

        if "Assessment_Result_001/Description" in a:
            assessment_result_001_description = a['Assessment_Result_001/Description']

        if "_submitted_by" in a:
            submitted_by = a['_submitted_by']

        if "_attachments" in a and len(a["_attachments"]) > 0:
            largeimage = a["_attachments"][0]['download_large_url']
            mediumimage = a["_attachments"][0]['download_medium_url']
            smallimage = a["_attachments"][0]['download_small_url']
        else:
            largeimage = "No Image"
            mediumimage = "No Image"
            smallimage = "No Image"

        assessment = Assessment(uniqueid=uniqueid, largeimage=largeimage, smallimage=smallimage, mediumimage=mediumimage, start=start, latitude=latitude, longitude=longitude, end=end, today=today, inspectorid=inspector_id, assessmenttype=assessment_type, identifiersbuildingid=identifiers_building_id, identifiersinspectedarea=identifiers_inspected_area,
                                identifiersdatetime=identifiers_date_time, assessmentresultbuildingname=assessment_result_building_name, assessmentresultcontactperson=assessment_result_contact_person, assessmentresultfirstname=assessment_result_first_name, assessmentresultphonenumber=assessment_result_phone_number,
                                assessmentresultaddress=assessment_result_address, assessmentresultnumberofoccupants=assessment_result_number_of_occupants, assessmentresultbuildingbuiltinyear=assessment_result_building_built_in_year, assessmentresultnumberofstoriesaboveground=assessment_result_number_of_stories_above_ground,
                                assessmentresultnumberofstoriesbelowground=assessment_result_number_of_stories_below_ground, assessmentresultgpscoordinates=assessment_result_gps_coordinates, assessmentresultapproximatefootprstrareasqm=assessment_result_approximate_footprint_area_sq_m, soilslopesoildescription=soil_slope_soil_description,
                                soilslopesiteslopedescription=soil_slope_site_slope_description, typeconstructiontypeofconstruction=type_construction_type_of_construction, typerooftypeofroof=type_roof_type_of_roof, buildingshapeplan=building_shape_plan, observedirregularities001softstory=observed_irregularities_001_soft_story, observedirregularities001setbacks=observed_irregularities_001_set_backs,
                                observedirregularities001coupledshearwalls=observed_irregularities_001_coupled_shear_walls, observedirregularities001shortenedcolumns=observed_irregularities_001_shortened_columns, observedirregularities001pounding=observed_irregularities_001_pounding, primaryoccupancy=primary_occupancy,
                                totaldamagestatuscollapseorpartialcollapse=total_damage_status_collapse_or_partial_collapse, totaldamagestatusbuildingorstoreyleaning=total_damage_status_building_or_storey_leaning, totaldamagestatuspoundingtoadjecent=total_damage_status_pounding_to_adjecent, totaldamagestatusbuildingofffoundation=total_damage_status_building_off_foundation,
                                totaldamagestatusotherdamagestatus=total_damage_status_other_damage_status, structuralhazardsfoundations=structural_hazards_foundations, structuralhazardsrooffloorverticalloadcapacity=structural_hazards_roof_floor_vertical_load_capacity, structuralhazardscolumnspillasterscrackspalled=structural_hazards_columns_pillasters_crack_spalled,
                                structuralhazardsslabbeamjoistcrackspalled=structural_hazards_slab_beam_joist_crack_spalled, structuralhazardswallsstrextcrackingcollapse=structural_hazards_walls_int_ext_cracking_collapse, structuralhazardsotherdamagestatus001=structural_hazards_other_damage_status_001, nonstructuralhazardsparapetcanopyorstairdamage=non_structural_hazards_parapet_canopy_or_stair_damage,
                                nonstructuralhazardscladdingandwindowsystems=non_structural_hazards_cladding_and_window_systems, nonstructuralhazardsceilingsandlightsfixtures=non_structural_hazards_ceilings_and_lights_fixtures, nonstructuralhazardsstreriorwallspartition=non_structural_hazards_interior_walls_partition,
                                nonstructuralhazardselevators=non_structural_hazards_elevators, nonstructuralhazardsstairsexits=non_structural_hazards_stairs_exits, nonstructuralhazardselectricitygasfuel=non_structural_hazards_electricity_gas_fuel, nonstructuralhazardsotherdamagestatus002=non_structural_hazards_other_damage_status_002,
                                geotechnicalslopefailure=geotechnical_slope_failure, geotechnicalgroundmovementfissures=geotechnical_ground_movement_fissures, geotechnicalliquefaction=geotechnical_liquefaction, geotechnicalsubterraneanstructuredamage=geotechnical_subterranean_structure_damage, geotechnicalotherdamagestatus003=geotechnical_other_damage_status_003,
                                summaryoffindingsannotateimagewidget=summary_of_findings_annotate_image_widget, summaryoffindingsestimatedbuildingdamage=summary_of_findings_estimated_building_damage, summaryoffindingsestimatedrepaircostdollars=summary_of_findings_estimated_repair_cost_dollars, assessmentresult001assessmentresult002=assessment_result_001_assessment_result_002,
                                assessmentresult001description=assessment_result_001_description, version="", metainstanceid="", xformidstring="", uuid="", status="", geolocation=[], submissiontime=datetime.utcnow(), tags=[], notes=[], validationstatus="", submittedby=submitted_by)

        if latitude and longitude:
            final_list.append(assessment)

    return final_list

# Define user structure for authentication system
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(30))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout authenticated users


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

# Redirect visitors to login page if not authenticated


def unauthorized_callback():
    return redirect('/login')


# Change tag text to human readable format

def allassessmentsapirequeststring():
    try:
        request_data = {'Authorization': 'Token ' + API_SECRET}
        r = requests.get(url=API_URL + FORM_ID,
                         headers={'Authorization': 'Token ' + API_SECRET})
        response = r.text
        return response
    except:
        return None


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


def damageconversionnumber(tagtext):
    if tagtext == "none_minor__0_":
        tagtext = "0"
    elif tagtext == "moderate__10_5":
        tagtext = "1"
    elif tagtext == "severe__50_100":
        tagtext = "2"
    else:
        tagtext = "0"
    return tagtext


# Main index route
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


@app.route('/download', methods=['GET', 'POST'])
def download():
    response = allassessmentsapirequeststring()

    if response:
        data = pd.read_json(StringIO(response))
        return str(data.to_csv())
    else:
        return None


# Convert all assessment data to GEOJson format

@app.route('/geojson')
def convertogeojson():
    data = []
    assessments = create_assessment_list()
    for assessment in assessments:
        my_point = Point((float(assessment.longitude),
                         float(assessment.latitude)))
        my_feature = Feature(geometry=Point(my_point), properties={
                             'name': assessment.identifiersbuildingid, 'id': assessment.uniqueid, 'image': assessment.largeimage})
        data.append(my_feature)

    feature_collection = FeatureCollection(data)

    return str(feature_collection)


@app.route('/damage/<id>', methods=['GET'])
def getdamage(id):

    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID,
                     headers={'Authorization': 'Token ' + API_SECRET})
    response = r.json()
    finalresponse = []

    if "total_damage_status/Building_off_foundation" in item:
        offoundation = damageconversionnumber(
            item['total_damage_status/Building_off_foundation'])

    if "total_damage_status/Building_or_storey_leaning" in item:
        leaning = damageconversionnumber(
            item['total_damage_status/Building_or_storey_leaning'])

    if "total_damage_status/Collapse_or_partial_collapse" in item:
        collapse = damageconversionnumber(
            item['total_damage_status/Collapse_or_partial_collapse'])

    if "total_damage_status/Pounding_to_adjecent" in item:
        ptoa = damageconversionnumber(
            item['total_damage_status/Pounding_to_adjecent'])

    if "total_damage_status/Other_damage_status" in item:
        damageother = damageconversionnumber(
            item['total_damage_status/Other_damage_status'])

    damage = {
        'offoundation': offoundation,
        'leaning': leaning,
        "collapse": collapse,
        "ptoa": ptoa,
        'damageother': damageother
    }

    return json.dumps(finalresponse)


# Assessment list route
@app.route('/assessments')
@cache.cached(timeout=50)
@login_required
def assessmentlist():
    return render_template('assessment-list.html')


# Return all report instances from a form id and process JSON
@app.route('/all-data', methods=['GET'])
def all_data_request():
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID,
                     headers={'Authorization': 'Token ' + API_SECRET})
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
                estimateddamagesinglelist = item['Summary_of_findings/Estimated_Building_Damage'].split(
                    "_")
                if len(estimateddamagesinglelist) > 0:
                    try:
                        estimateddamagesingle = estimateddamagesinglelist[1]
                    except:
                        estimateddamagesingle = estimateddamagesinglelist[0]

            coordinates = item['assessment_result/GPS_Coordinates'].split(" ")
            tag = tagconversion(
                item['Assessment_Result_001/Assessment_Result_002'])
            if "total_damage_status/Building_off_foundation" in item:
                offoundation = damageconversion(
                    item['total_damage_status/Building_off_foundation'])

            if "total_damage_status/Building_or_storey_leaning" in item:
                leaning = damageconversion(
                    item['total_damage_status/Building_or_storey_leaning'])

            if "total_damage_status/Collapse_or_partial_collapse" in item:
                collapse = damageconversion(
                    item['total_damage_status/Collapse_or_partial_collapse'])

            if "total_damage_status/Pounding_to_adjecent" in item:
                ptoa = damageconversion(
                    item['total_damage_status/Pounding_to_adjecent'])

            if "total_damage_status/Other_damage_status" in item:
                damageother = damageconversion(
                    item['total_damage_status/Other_damage_status'])

            assessment = {'id': item['_id'],
                          'latitude': coordinates[0],
                          'longitude': coordinates[1],
                          'tag': tag,
                          'buildingname': item['identifiers/Building_ID'],
                          'image': image,
                          'estimateddamage': item['Summary_of_findings/Estimated_Building_Damage'].replace("_", "-") + "%",
                          'estimateddamagesingle': estimateddamagesingle,
                          'occupants': item['assessment_result/Number_of_occupants'],
                          'primaryoccupancy': item['Primary_Occupancy'].replace("_", " ").capitalize(),
                          'offoundation': offoundation,
                          'leaning': leaning,
                          "collapse": collapse,
                          "ptoa": ptoa,
                          'damageother': damageother
                          }
            finalresponse.append(assessment)

    return json.dumps(finalresponse)


@app.route('/all-data2', methods=['GET'])
def all_data_request2():
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID,
                     headers={'Authorization': 'Token ' + API_SECRET})
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
                estimateddamagesinglelist = item['Summary_of_findings/Estimated_Building_Damage'].split(
                    "_")
                if len(estimateddamagesinglelist) > 0:
                    try:
                        estimateddamagesingle = estimateddamagesinglelist[1]
                    except:
                        estimateddamagesingle = estimateddamagesinglelist[0]

            coordinates = item['assessment_result/GPS_Coordinates'].split(" ")
            tag = tagconversion(
                item['Assessment_Result_001/Assessment_Result_002'])
            if "total_damage_status/Building_off_foundation" in item:
                offoundation = damageconversion(
                    item['total_damage_status/Building_off_foundation'])

            if "total_damage_status/Building_or_storey_leaning" in item:
                leaning = damageconversion(
                    item['total_damage_status/Building_or_storey_leaning'])

            if "total_damage_status/Collapse_or_partial_collapse" in item:
                collapse = damageconversion(
                    item['total_damage_status/Collapse_or_partial_collapse'])

            if "total_damage_status/Pounding_to_adjecent" in item:
                ptoa = damageconversion(
                    item['total_damage_status/Pounding_to_adjecent'])

            if "total_damage_status/Other_damage_status" in item:
                damageother = damageconversion(
                    item['total_damage_status/Other_damage_status'])

            assessment = {'id': item['_id'],
                          'latitude': coordinates[0],
                          'longitude': coordinates[1],
                          'tag': tag,
                          'buildingname': item['identifiers/Building_ID'],
                          'image': image,
                          'estimateddamage': item['Summary_of_findings/Estimated_Building_Damage'].replace("_", "-") + "%",
                          'estimateddamagesingle': estimateddamagesingle,
                          'occupants': item['assessment_result/Number_of_occupants'],
                          'primaryoccupancy': item['Primary_Occupancy'].replace("_", " ").capitalize(),
                          'offoundation': offoundation,
                          'leaning': leaning,
                          "collapse": collapse,
                          "ptoa": ptoa,
                          'damageother': damageother
                          }
            finalresponse.append(assessment)

    return json.dumps(finalresponse)
    


# Return a single report instance from an instance id
@app.route('/<id>')
@login_required
def single_data_request(id):
    request_data = {'Authorization': 'Token ' + API_SECRET}
    r = requests.get(url=API_URL + FORM_ID + '/' + id,
                     headers={'Authorization': 'Token ' + API_SECRET})

    response = r.json()

    coordinates = response['assessment_result/GPS_Coordinates'].split(" ")
    area = response['identifiers/Inspected_area'].replace("_", " ")
    rooftype = response['type_roof/Type_of_Roof'].replace(
        "_", " ").capitalize()
    primaryoccupancy = response['Primary_Occupancy'].replace(
        "_", " ").capitalize()
    soil = response['soil_slope/Soil_Description'].replace(
        "_", " ").capitalize()
    estimateddamage = response['Summary_of_findings/Estimated_Building_Damage'].replace(
        "_", "-") + "%"
    if "_attachments" in response and len(response["_attachments"]) > 0:
        image = response["_attachments"][0]['download_medium_url']
    else:
        image = "/static/images/no-image.jpg"

    tag = response['Assessment_Result_001/Assessment_Result_002']
    my_time = dateparser.parse(response['identifiers/Date_Time'])
    date = humanize.naturaldate(my_time)
    leaning = ""
    collapse = ""
    ptoa = ""
    damageother = ""

    if "total_damage_status/Building_off_foundation" in response:
        offoundation = damageconversionnumber(
            response['total_damage_status/Building_off_foundation'])

    if "total_damage_status/Building_or_storey_leaning" in response:
        leaning = damageconversionnumber(
            response['total_damage_status/Building_or_storey_leaning'])

    if "total_damage_status/Collapse_or_partial_collapse" in response:
        collapse = damageconversionnumber(
            response['total_damage_status/Collapse_or_partial_collapse'])

    if "total_damage_status/Pounding_to_adjecent" in response:
        ptoa = damageconversionnumber(
            response['total_damage_status/Pounding_to_adjecent'])

    if "total_damage_status/Other_damage_status" in response:
        damageother = damageconversionnumber(
            response['total_damage_status/Other_damage_status'])

    builtresponse = {
        'id': response['_id'],
        'BuildingName': response['identifiers/Building_ID'],
        'inspector': response['Inspector_ID'],
        'contact': response['assessment_result/Contact_person'],
        'phone': response['assessment_result/Phone_number'],
        'address': response['assessment_result/Address'],
        'assessmenttype': response['Assessment_Type'].capitalize(),
        'latitude': coordinates[0],
        'longitude': coordinates[1],
        'cost': response['Summary_of_findings/Estimated_Repair_Cost_Dollars'],
        'occupants': response['assessment_result/Number_of_occupants'],
        'yearbuilt': response['assessment_result/Building_built_in_year'],
        'storiesabove': response['assessment_result/Number_of_stories_above_ground'],
        'storiesbelow': response['assessment_result/Number_of_stories_below_ground'],
        'submitedby': response['_submitted_by'],
        'inspectedarea': area.capitalize(),
        'approxarea': response['assessment_result/Approximate_footprint_area_sq_m'],
        'tag': tagconversion(response['Assessment_Result_001/Assessment_Result_002']),
        'inspectorid': response['Inspector_ID'],
        'assessmentdate': date.capitalize(),
        'rooftype': rooftype,
        'primaryoccupancy': primaryoccupancy,
        'estimateddamage': estimateddamage,
        'soil':  soil,
        'thumbnail': image,
        'offoundation': offoundation,
        'leaning': leaning,
        "collapse": collapse,
        "ptoa": ptoa,
        'damageother': damageother
    }

    return render_template('details.html', data=builtresponse)


if __name__ == '__main__':

    app.run(debug=True)

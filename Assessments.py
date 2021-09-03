from datetime import datetime
from uuid import UUID
from typing import List, Any
import requests
import json
import humanize

class ValidationStatus:
    pass

    def __init__(self, ) -> None:
        pass


class Assessment:
    uniqueid: str
    start: datetime
    end: datetime
    today: datetime
    inspectorid: str
    latitude: str
    longitude: str
    largeimage: str
    mediumimage: str
    smallimage: str
    assessmenttype: str
    identifiersbuildingid: str
    identifiersinspectedarea: str
    identifiersdatetime: datetime
    assessmentresultbuildingname: str
    assessmentresultcontactperson: str
    assessmentresultfirstname: str
    assessmentresultphonenumber: str
    assessmentresultaddress: str
    assessmentresultnumberofoccupants: str
    assessmentresultbuildingbuiltinyear: datetime
    assessmentresultnumberofstoriesaboveground: str
    assessmentresultnumberofstoriesbelowground: str
    assessmentresultgpscoordinates: str
    assessmentresultapproximatefootprstrareasqm: str
    soilslopesoildescription: str
    soilslopesiteslopedescription: str
    typeconstructiontypeofconstruction: str
    typerooftypeofroof: str
    buildingshapeplan: str
    observedirregularities001softstory: str
    observedirregularities001setbacks: str
    observedirregularities001coupledshearwalls: str
    observedirregularities001shortenedcolumns: str
    observedirregularities001pounding: str
    primaryoccupancy: str
    totaldamagestatuscollapseorpartialcollapse: str
    totaldamagestatusbuildingorstoreyleaning: str
    totaldamagestatuspoundingtoadjecent: str
    totaldamagestatusbuildingofffoundation: str
    totaldamagestatusotherdamagestatus: str
    structuralhazardsfoundations: str
    structuralhazardsrooffloorverticalloadcapacity: str
    structuralhazardscolumnspillasterscrackspalled: str
    structuralhazardsslabbeamjoistcrackspalled: str
    structuralhazardswallsstrextcrackingcollapse: str
    structuralhazardsotherdamagestatus001: str
    nonstructuralhazardsparapetcanopyorstairdamage: str
    nonstructuralhazardscladdingandwindowsystems: str
    nonstructuralhazardsceilingsandlightsfixtures: str
    nonstructuralhazardsstreriorwallspartition: str
    nonstructuralhazardselevators: str
    nonstructuralhazardsstairsexits: str
    nonstructuralhazardselectricitygasfuel: str
    nonstructuralhazardsotherdamagestatus002: str
    geotechnicalslopefailure: str
    geotechnicalgroundmovementfissures: str
    geotechnicalliquefaction: str
    geotechnicalsubterraneanstructuredamage: str
    geotechnicalotherdamagestatus003: str
    summaryoffindingsannotateimagewidget: str
    summaryoffindingsestimatedbuildingdamage: str
    summaryoffindingsestimatedrepaircostdollars: str
    assessmentresult001assessmentresult002: str
    assessmentresult001description: str
    version: str
    metainstanceid: str
    xformidstring: str
    uuid: UUID
    status: str
    geolocation: List[float]
    submissiontime: datetime
    tags: List[Any]
    notes: List[Any]
    validationstatus: str
    submittedby: str

    def __init__(self, uniqueid: str, largeimage: str, mediumimage: str, smallimage: str, start: datetime, end: datetime, latitude: str, longitude: str, today: datetime, inspectorid: str,
                 assessmenttype: str, identifiersbuildingid: str, identifiersinspectedarea: str, identifiersdatetime: datetime, assessmentresultbuildingname: str, assessmentresultcontactperson: str,
                 assessmentresultfirstname: str, assessmentresultphonenumber: str, assessmentresultaddress: str, assessmentresultnumberofoccupants: str, assessmentresultbuildingbuiltinyear: datetime, assessmentresultnumberofstoriesaboveground: str,
                 assessmentresultnumberofstoriesbelowground: str, assessmentresultgpscoordinates: str, assessmentresultapproximatefootprstrareasqm: str, soilslopesoildescription: str, soilslopesiteslopedescription: str,
                 typeconstructiontypeofconstruction: str, typerooftypeofroof: str, buildingshapeplan: str, observedirregularities001softstory: str, observedirregularities001setbacks: str, observedirregularities001coupledshearwalls: str,
                 observedirregularities001shortenedcolumns: str, observedirregularities001pounding: str, primaryoccupancy: str, totaldamagestatuscollapseorpartialcollapse: str, totaldamagestatusbuildingorstoreyleaning: str,
                 totaldamagestatuspoundingtoadjecent: str, totaldamagestatusbuildingofffoundation: str, totaldamagestatusotherdamagestatus: str, structuralhazardsfoundations: str, structuralhazardsrooffloorverticalloadcapacity: str,
                 structuralhazardscolumnspillasterscrackspalled: str, structuralhazardsslabbeamjoistcrackspalled: str, structuralhazardswallsstrextcrackingcollapse: str, structuralhazardsotherdamagestatus001: str,
                 nonstructuralhazardsparapetcanopyorstairdamage: str, nonstructuralhazardscladdingandwindowsystems: str, nonstructuralhazardsceilingsandlightsfixtures: str, nonstructuralhazardsstreriorwallspartition: str, nonstructuralhazardselevators: str,
                 nonstructuralhazardsstairsexits: str, nonstructuralhazardselectricitygasfuel: str, nonstructuralhazardsotherdamagestatus002: str, geotechnicalslopefailure: str, geotechnicalgroundmovementfissures: str, geotechnicalliquefaction: str,
                 geotechnicalsubterraneanstructuredamage: str, geotechnicalotherdamagestatus003: str, summaryoffindingsannotateimagewidget: str, summaryoffindingsestimatedbuildingdamage: str, summaryoffindingsestimatedrepaircostdollars: str,
                 assessmentresult001assessmentresult002: str, assessmentresult001description: str, version: str, metainstanceid: str, xformidstring: str, uuid: UUID, status: str, geolocation: List[float], submissiontime: datetime, tags: List[Any], notes:
                 List[Any], validationstatus: str, submittedby: str) -> None:
        self.uniqueid = uniqueid
        self.start = start
        self.end = end
        self.today = today
        self.latitude = latitude
        self.longitude = longitude
        self.largeimage = largeimage
        self.mediumimage = mediumimage
        self.smallimage = smallimage
        self.inspectorid = inspectorid
        self.assessmenttype = assessmenttype
        self.identifiersbuildingid = identifiersbuildingid
        self.identifiersinspectedarea = identifiersinspectedarea
        self.identifiersdatetime = identifiersdatetime
        self.assessmentresultbuildingname = assessmentresultbuildingname
        self.assessmentresultcontactperson = assessmentresultcontactperson
        self.assessmentresultfirstname = assessmentresultfirstname
        self.assessmentresultphonenumber = assessmentresultphonenumber
        self.assessmentresultaddress = assessmentresultaddress
        self.assessmentresultnumberofoccupants = assessmentresultnumberofoccupants
        self.assessmentresultbuildingbuiltinyear = assessmentresultbuildingbuiltinyear
        self.assessmentresultnumberofstoriesaboveground = assessmentresultnumberofstoriesaboveground
        self.assessmentresultnumberofstoriesbelowground = assessmentresultnumberofstoriesbelowground
        self.assessmentresultgpscoordinates = assessmentresultgpscoordinates
        self.assessmentresultapproximatefootprstrareasqm = assessmentresultapproximatefootprstrareasqm
        self.soilslopesoildescription = soilslopesoildescription
        self.soilslopesiteslopedescription = soilslopesiteslopedescription
        self.typeconstructiontypeofconstruction = typeconstructiontypeofconstruction
        self.typerooftypeofroof = typerooftypeofroof
        self.buildingshapeplan = buildingshapeplan
        self.observedirregularities001softstory = observedirregularities001softstory
        self.observedirregularities001setbacks = observedirregularities001setbacks
        self.observedirregularities001coupledshearwalls = observedirregularities001coupledshearwalls
        self.observedirregularities001shortenedcolumns = observedirregularities001shortenedcolumns
        self.observedirregularities001pounding = observedirregularities001pounding
        self.primaryoccupancy = primaryoccupancy
        self.totaldamagestatuscollapseorpartialcollapse = totaldamagestatuscollapseorpartialcollapse
        self.totaldamagestatusbuildingorstoreyleaning = totaldamagestatusbuildingorstoreyleaning
        self.totaldamagestatuspoundingtoadjecent = totaldamagestatuspoundingtoadjecent
        self.totaldamagestatusbuildingofffoundation = totaldamagestatusbuildingofffoundation
        self.totaldamagestatusotherdamagestatus = totaldamagestatusotherdamagestatus
        self.structuralhazardsfoundations = structuralhazardsfoundations
        self.structuralhazardsrooffloorverticalloadcapacity = structuralhazardsrooffloorverticalloadcapacity
        self.structuralhazardscolumnspillasterscrackspalled = structuralhazardscolumnspillasterscrackspalled
        self.structuralhazardsslabbeamjoistcrackspalled = structuralhazardsslabbeamjoistcrackspalled
        self.structuralhazardswallsstrextcrackingcollapse = structuralhazardswallsstrextcrackingcollapse
        self.structuralhazardsotherdamagestatus001 = structuralhazardsotherdamagestatus001
        self.nonstructuralhazardsparapetcanopyorstairdamage = nonstructuralhazardsparapetcanopyorstairdamage
        self.nonstructuralhazardscladdingandwindowsystems = nonstructuralhazardscladdingandwindowsystems
        self.nonstructuralhazardsceilingsandlightsfixtures = nonstructuralhazardsceilingsandlightsfixtures
        self.nonstructuralhazardsstreriorwallspartition = nonstructuralhazardsstreriorwallspartition
        self.nonstructuralhazardselevators = nonstructuralhazardselevators
        self.nonstructuralhazardsstairsexits = nonstructuralhazardsstairsexits
        self.nonstructuralhazardselectricitygasfuel = nonstructuralhazardselectricitygasfuel
        self.nonstructuralhazardsotherdamagestatus002 = nonstructuralhazardsotherdamagestatus002
        self.geotechnicalslopefailure = geotechnicalslopefailure
        self.geotechnicalgroundmovementfissures = geotechnicalgroundmovementfissures
        self.geotechnicalliquefaction = geotechnicalliquefaction
        self.geotechnicalsubterraneanstructuredamage = geotechnicalsubterraneanstructuredamage
        self.geotechnicalotherdamagestatus003 = geotechnicalotherdamagestatus003
        self.summaryoffindingsannotateimagewidget = summaryoffindingsannotateimagewidget
        self.summaryoffindingsestimatedbuildingdamage = summaryoffindingsestimatedbuildingdamage
        self.summaryoffindingsestimatedrepaircostdollars = summaryoffindingsestimatedrepaircostdollars
        self.assessmentresult001assessmentresult002 = assessmentresult001assessmentresult002
        self.assessmentresult001description = assessmentresult001description
        self.version = version
        self.metainstanceid = metainstanceid
        self.xformidstring = xformidstring
        self.uuid = uuid
        self.status = status
        self.geolocation = geolocation
        self.submissiontime = submissiontime
        self.tags = tags
        self.notes = notes
        self.validationstatus = validationstatus
        self.submittedby = submittedby

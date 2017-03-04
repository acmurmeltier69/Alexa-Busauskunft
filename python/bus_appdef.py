# coding: utf-8
#-------------------------------------------------------------------------------
#
# This file contains the application definition for the Alexa bas skill (for Aseag Aachen)
# The application definition is specified as python file in global variables 
# rather than as JSON object to 
# - ensure fast loading for individual user utterances when run on the server
# -avoid parsing issued in the online system
# - allow import of custom slot types from external files (e.g. station names)
#-------------------------------------------------------------------------------

import aseag_data

APPNAME = "aseag"
#APPID   = "amzn1.ask.skill.a5cea9e0-a824-45e6-830f-5e048085f85d" # andi
APPID   = "amzn1.ask.skill.f83ddc70-f70f-40de-aa46-8d966907d8f3" # mankei
INTENTS = {
            "GetDeparturesFromFavorite":  ["Direction", "Busline", "Next", "Transport"],
            "GetDeparturesFromOther":     ["Origin", "Direction", "Busline", "Next", "Transport"],
#            "GetFavConnecionDepartures" : ["FavConnection"],
            "FindConnectionFromFavorite": ["Destination", "Next", "Transport"],
            "FindConnectionFromOther":    ["Origin", "Destination", "Next", "Transport"],
            "ChangeDefaultStation":       ["Origin"],
            "AMAZON.YesIntent" : [],
            "AMAZON.NoIntent" : [],
            "AMAZON.HelpIntent"  : []
           }

SLOTS = {
            "Direction" :       "LIST_OF_DIRECTIONS",
            "Busline" :         "LIST_OF_ASEAG_LINES",
            "Next" :            "MODIFIER_NEXT",
            "Transport" :       "LIST_OF_TRANSPORT",
            "Origin" :          "LIST_OF_STATIONS",
            "Destination" :     "LIST_OF_STATIONS",
            "FavConnection" :   "LIST_OF_FAVORITE_CONNECTIONS"
         }

SLOTTYPES = {
            "LIST_OF_DIRECTIONS":[
                ["DIR_INWARD", [u"stadteinwärts", u"richtung stadt", u"richtung innenstadt", u"in die stadt", u"richtung aachen", u"richtung zentrum"]],
                ["DIR_OUTWARD", [u"stadtauswärts"]]
            ],
            "LIST_OF_TRANSPORT" :[
                ["DEPARTURE", [u"abfahrt", u"abfahrten"]],
                ["BUS", [u"bus", u"busabfahrt", u"busabfahrten", u"busverbindung", u"busverbindungen"]],
                ["ZUG", [u"zug", u"bahn", u"bahnverbindungen", u"zugverbindungen"]],
                ["SCHNELLBUS", [u"schnellbus"]],
                ["DIRECT", [u"direktverbindung"]],
                ["ANY", [u"verbindung"]]
            ],
            "MODIFIER_NEXT" :[
                ["ANY",   [u"der", u"die", u"ein", u"eine", u"irgendein", u"irgendeine"]],
                ["NEXT",  [u"der nächste", u"die nächste"]],
                ["NEXT5", [u"die nächsten fünf"]]
            ],
            "LIST_OF_FAVORITE_CONNECTIONS" : [
                ["SCHOOL", [u"der schulbus", 
                            u"mein schulbus", u"mein bus in die schule", u"mein bus zur schule"]],
                ["WORK", [u"mein bus in die arbeit", u"mein bus zur arbeit", u"mein bus in die firma"]],
            ],
            "LIST_OF_ASEAG_LINES" : aseag_data.BUSLINES, # import from external file
            "LIST_OF_STATIONS" : aseag_data.STATIONLIST # import from external file
   }

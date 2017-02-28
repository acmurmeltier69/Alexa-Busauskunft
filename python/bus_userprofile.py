# coding: utf-8

from myask import myask_log, myask_dynamodb

#-----------------------------------------------------------------------
# Dummy profile for offline testing without any db
#-----------------------------------------------------------------------
HARDCODED_PROFILES= {
            "TESTUSER":{
                "Name" : u"Hardcoded",
                "DefaultStop": 210705,
                "FavoriteConnections" : {
                    "SCHOOL" : {
                        "OrgID" : 210705, # Technologiepark
                        "DestID"  : 100016, # Driescher Gäßchen
                        "PreferredLine" : 147,
                        "DepTimeWindowStart" : "07:15",
                        "DepTimeWindowEnd"   : "07:45",
                        },
                    "WORK": {
                        "OrgID" : 210705, # Technologiepark
                        "DestID"  : 100813, # Lukasstrasse
                        "PreferredLine" : 34,
                        "DepTimeWindowStart" : "07:20",
                        "DepTimeWindowEnd"   : "08:00",
                        }
                }
            },
        }

class userProfile:
    #---------------------------------------------------------------------------
    # class for storing user profiles for the aseag app
    
    _profile_data = {}
    _profile_name = "TESTUSER"
    _profiletable = ""
    _user_id = ""
    
    def __init__(self, userID):
        self._user_id = userID
        if userID == "FAKE":
            #Found profile of "diekellnerfamilie"
            self._profile_data = HARDCODED_PROFILES['TESTUSER']
        else:
            self._profiletable = myask_dynamodb.dynamoDB("aseag_userprofile")
            myask_log.debug(0,"GetTable: "+str(self._profiletable.GetStatus()))
            profile_data = self._profiletable.FetchUserProfile(userID)
            if profile_data == {}:
                myask_log.warning("Could not locate user profile. Creating new one. User: "+str(userID))
                self._profiletable.CreateNewUserProfile(userID, {})
                self._profile_data = {}
            else:
                self._profile_data = profile_data
            
  
    def isKnownUser(self):
        if self._profile_data == {}:
            return False
        else:
            return True

    def HasDefaultStop(self):
        if self._profile_data != {} and "DefaultStop" in self._profile_data: 
            return True
        else:
            return False
            
    def GetProfile(self):
        return self._profile_data
    
    def getUserName(self):
        return self._profile_name
    
    def GetDefaultStopId(self):
        if "DefaultStop" in self._profile_data:
            return int(self._profile_data["DefaultStop"])
        return 0

    def SetDefaultStopId(self, station_id):
        self._profile_data["DefaultStop"] = station_id
        self._profiletable.UpdateUserProfile(self._user_id, self._profile_data)

        return True
                        
    
    def GetFavoriteConnection(self, favcon):
        #-----------------------------------------------------------------------
        # Gets favorite connection 'favcon' from the user profile
        # The favorite is a dictionary containing
        #   "StartID" : (int) bus stop ID for starting stop
        #   "StopID"  : (int) bus stop ID for destination stop
        #   "PreferredLines" : (list of integers) preferred buslines
        #   "DepTimeWindowStart" : (time str) "07:15"
        #   "DepTimeWindowEnd"   : (time str) "07:35"
        # If 'favcon' is not found in the user profile, returns an empty dictionary {}
        #----------------------------------------------------------------------
        
        if "FavoriteConnections" in self._profile_data:
            if favcon in self._profile_data["FavoriteConnections"]:
                fav = self._profile_data["FavoriteConnections"][favcon]
                return fav
            else:
                myask_log.warning("FavoriteConnection '"+favcon+"' not found for user"+ self._profile_name)
                return {}               
        else:
            myask_log.warning("No favorite connections found for user" + self._profile_name)
            return {}
    
    def DeleteUserProfile(self):
        self._profiletable.DeleteUserProfile(self._user_id)
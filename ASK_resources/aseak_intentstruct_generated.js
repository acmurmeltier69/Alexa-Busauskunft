{
   "intents": [
        {
         "intent": "AMAZON.YesIntent"
        },
        {
         "intent": "GetDeparturesFromOther",
         "slots": [
            {
               "name": "Origin",
               "type": "LIST_OF_STATIONS"
            },
            {
               "name": "Direction",
               "type": "LIST_OF_DIRECTIONS"
            },
            {
               "name": "Busline",
               "type": "AMAZON.NUMBER"
            },
            {
               "name": "Next",
               "type": "MODIFIER_NEXT"
            },
            {
               "name": "Transport",
               "type": "LIST_OF_TRANSPORT"
            }         ]
        },
        {
         "intent": "FindConnectionFromOther",
         "slots": [
            {
               "name": "Origin",
               "type": "LIST_OF_STATIONS"
            },
            {
               "name": "Destination",
               "type": "LIST_OF_STATIONS"
            },
            {
               "name": "Next",
               "type": "MODIFIER_NEXT"
            },
            {
               "name": "Transport",
               "type": "LIST_OF_TRANSPORT"
            }         ]
        },
        {
         "intent": "GetFavConnecionDepartures",
         "slots": [
            {
               "name": "FavConnection",
               "type": "LIST_OF_FAVORITE_CONNECTIONS"
            }         ]
        },
        {
         "intent": "AMAZON.NoIntent"
        },
        {
         "intent": "GetDeparturesFromFavorite",
         "slots": [
            {
               "name": "Direction",
               "type": "LIST_OF_DIRECTIONS"
            },
            {
               "name": "Busline",
               "type": "AMAZON.NUMBER"
            },
            {
               "name": "Next",
               "type": "MODIFIER_NEXT"
            },
            {
               "name": "Transport",
               "type": "LIST_OF_TRANSPORT"
            }         ]
        },
        {
         "intent": "FindConnectionFromFavorite",
         "slots": [
            {
               "name": "Destination",
               "type": "LIST_OF_STATIONS"
            },
            {
               "name": "Next",
               "type": "MODIFIER_NEXT"
            },
            {
               "name": "Transport",
               "type": "LIST_OF_TRANSPORT"
            }         ]
        },
        {
         "intent": "AMAZON.HelpIntent"
        },
        {
         "intent": "ChangeDefaultStation",
         "slots": [
            {
               "name": "Origin",
               "type": "LIST_OF_STATIONS"
            }         ]
        }   ]
}

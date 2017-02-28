# Alexa-Busauskunft
Alexa Skill für Buauskunfts  
Geschriebe nfür Nahverkehr im Raum Aachen (ASEAG), kann aber leicht für andere Städte angepasst werden.

Der Skill benutzt die ASEAG Unified realtime api (URA) (Base URL:  http://ivu.aseag.de/interfaces/ura/instant_V1)
Siehe z.B http://content.tfl.gov.uk/tfl-live-bus-river-bus-arrivals-api-documentation.pdf 

## Requires
Der Skill benutztz die folgenden "externen" Pakete:
- package "requests"
- package "myask" from https://github.com/acmurmeltier69/myask.git
Diese Pakete müssen als Unterverzeichnisse eingebunden werden, wenn der Handler als aws Lambda hochgeladen wird.


# Funktionalität
Dieser Skill bietet Live Abfahrts- und Verbindungsinformationen für den Nahverkehr der ASEAG im Raum Aachen.

Sofern der Benutzer einmalig eine Haltestelle als bevorzugeten Abfahrtspunkt festgelegt hat, 
können Abfahrten und Verbindungen von dieser Haltestelle vereinfacht abgefragt werden. 

Unterstützte Kommandos (Intents):
 - **GetDeparturesFromFavorite** : Zeige Live-Abfahrtszeiten der Busse von der bevorzugten Haltestelle
 
   Beispiele:
>  "Wann fährt der nächste Bus"

>  "Wann geht der nächste Bus der Line 47"

>  "Wann kommt der nächste Bus stadteinwärts"

 - **GetDeparturesFromOther** :  Zeige Live-Abfahrtszeiten ab einer anderen Haltestelle

   Beispiele:
>  "Wann fährt der nächste Bus ab Richterich Rathaus"

>  "Zeige die Abfahrten die Linie 11 ab Elisenbrunnen"

 - **GetFavConnecionDepartures** : Suche Verbindungen von der bevorzugten Haltestelle zu anderen Zielen

   Beispiele:
>  "Wann kommt der nächste Bus zum Hauptbahnhof"

>  "Wann geht ein Bus in die Liebigstraße"
     
- **FindConnectionFromOther** : Suche Verbindungen zwischen zwei beliebigen Haltestellen

   Beispiele:
>  "Wann geht der nächste Bus vom Ponttor zum Hauptbahnhof"

>  "Wann geht ein Bus von Richterich rathaus in die Liebigstraße"
 
- **ChangeDefaultStation** : Ändere die bevorzugte Haltestelle für den Benutzer

   Beispiel:
>  "Ändere die_bevorzugte_haltestelle zu Kohlscheid Markt"

    Die bevorzugte Haltestelle für den benutzer wird anhand der Amazon UserID in einer DynamoDB Datenbank abgelegt


- 

'''
Requirements: geopy
> sudo pip3 install geopy
> sudo pip3 install FlightRadar24API
'''


import os
os.system('cls||clear')

import requests
import json
import time
import pprint as pp
import geopy.distance
import LEDarcade as LED
from configparser import ConfigParser
from datetime import datetime

from FlightRadar24.api import FlightRadar24API 


fr_api = FlightRadar24API()




#---------------------------------------
#Variable declaration section
#---------------------------------------
ScrollSleep         = 0.010
TerminalTypeSpeed   = 0  #pause in seconds between characters
TerminalScrollSpeed = 0  #pause in seconds between new lines
CursorRGB           = (0,0,0)
CursorDarkRGB       = (0,0,0)
LastGetFlightsTime  = time.time()
GetFlightsWaitMinutes = 5

TitleRGB = (0,150,0)
ValueRGB = (150,75,0)
ValueRGB2 = (75,0,200)
ScrollingRGB = (100,150,0)

TitleUpdating = LED.CreateBannerSprite("updating...")

DetailedFlightList = []

#Files
ConfigFileName = "FlightConfig.ini" 

#----------------------------------------
#-- FILE ACCESS Functions              --
#----------------------------------------

def LoadConfigFile():

  global BaseLat
  global BaseLon
  global Radius
  global GetFlightsWaitMinutes
  global InFlight


  print ("--Load Config values--")
  if (os.path.exists(ConfigFileName)):

    print ("Config file (",ConfigFileName,"): found")
    KeyFile = ConfigParser()
    KeyFile.read(ConfigFileName)

    #Get tokens
    BaseLat         = float(KeyFile.get("FLIGHT","BaseLat"))
    BaseLon         = float(KeyFile.get("FLIGHT","BaseLon"))
    Radius          = int(KeyFile.get("FLIGHT","Radius"))
    GetFlightsWaitMinutes = int(KeyFile.get("FLIGHT","UpdateTime"))
    InFlight        = bool(int(KeyFile.get("FLIGHT","InFlight")))

    print (" ")

    print ("---------------------------------------------")
    print("BaseLat:        ",BaseLat)   
    print("BaseLon:        ",BaseLon)   
    print("Radius:         ",Radius)
    print("UpdateTime:     ",GetFlightsWaitMinutes)
    print("InFlight:       ",InFlight)
    print ("---------------------------------------------")
    print (" ")

  else:
    #To be finished later
    print ("ERROR: Could not locate Key file (",ConfigFileName,"). Create a file and make sure to pupulate it with your own keys.")







#Get a list of flights in a lat/lon box
def GetFlightsInBounds():
  print("")
  print("--GetFlightsInBounds--")
  print("Bounds:",BaseLat, BaseLon, Radius)
  bounds = fr_api.get_bounds_by_point(BaseLat, BaseLon, Radius)
  FlightList = fr_api.get_flights(airline= None, bounds=bounds)
  print("Flights:"+str(len(FlightList)))
  
  # print("****************************************")
  # pp.pprint(FlightList)
  # print("****************************************")
  
  time.sleep(2)
  
  return FlightList




def GetFlightDetails(FlightList):
  print("")
  print("--GetFlightDetails-")
  print("FlightList length: ",len(FlightList))
  
  #reset list
  DetailedFlightList = []
  
  for flight in FlightList:
    print(flight)
    details = fr_api.get_flight_details(flight)
    # print("****************************************")
    # pp.pprint(details)
    # print("****************************************")
    try:
      flight.set_flight_details(details)
    except:
      print("not a valid flight object")
   
    try:
      DetailedFlightList.append(flight)
      print("Appending flight")
    except:
      print("Processing",end='\r')


  return DetailedFlightList


def GetAirportList():
  global AirportList
  
  print("")
  print("--GetAirportList--")
  AirportList = fr_api.get_airports()
  print("Airports:",len(AirportList))
  print ("-----------------")
  print("")



  #for Airport in AirportList:
  #  print("===============================")
  #  pp.pprint(Airport)


def GetAirport(AirportIata):
  print("")
  print("--GetAirport--")  
  print("Searching for:",AirportIata)
  

  AirportName = ""

  try:
    #Search a list of dictionairies 
    Index = (next((i for i, x in enumerate(AirportList) if x['iata'] == AirportIata), None))
    print("Index:",Index)
    if(Index != None):
      pp.pprint(AirportList[Index])
      AirportName = AirportList[Index]["name"]
  except:
    print("Airport not found")
  return AirportName



def GetNearbyFlight(Flights):
  
  global AircraftCount
  
  print("")
  print("--GetNearbyFlight--")
  
  i = 0
  ShortestDistance = Radius
  ClosestFlight = -1
  TheWinner = ''

  if len(Flights) > 0:
    for flight in Flights:
      try:

        lat = flight.latitude
        lon = flight.longitude
        alt = flight.altitude

        print("")
        print("Analyzing flight data: ",i)
        print(flight)
        print("Lat:",lat)
        print("Lon:",lon)
        print("Alt:",alt)

        distance = geopy.distance.geodesic((lat,lon), (BaseLat, BaseLon)).m / 1000
        flight.distance = distance
        flight.record = i
        print("Distance:",flight.distance)
        if InFlight:
          if (distance <= ShortestDistance and alt > 0):
            ShortestDistance = distance
            ClosestFlight = i
        else:
          if (distance <= ShortestDistance):
            ShortestDistance = distance
            ClosestFlight = i
    
      except:
        print("Record:",i,"no flight info found")

      i = i + 1

  AircraftCount = i  

  if(ClosestFlight >= 0) :
    TheWinner = Flights[ClosestFlight]
    # print("****************************************")
    # pp.pprint(dir(TheWinner))
    # print("****************************************")
    
    DisplayFlight(TheWinner)

  else:
    print("**No flight data found**")
    return None

  return TheWinner

def DisplayFlight(Flight):

  global OriginAirport
  global DestinationAirport
  global OriginAirportName
  global DestinationAirportName
  global AircraftType 
  global AirlineName
  global AirlineShortName

  Flight              = Flight
  Record              = Flight.record
  Heading             = Flight.heading
  Distance            = Flight.distance
  Speed               = Flight.ground_speed #* 1.8520
  Messages            = '' 
  Altitude            = Flight.altitude
  Hex                 = Flight.icao_24bit.upper()
  AircraftType        = Flight.aircraft_model
  OriginAirport       = Flight.origin_airport_iata
  DestinationAirport  = Flight.destination_airport_iata
  OriginAirportName       = Flight.origin_airport_name
  DestinationAirportName  = Flight.destination_airport_name
  AirlineName         = Flight.airline_name
  AirlineShortName    = Flight.airline_short_name
  TimeDetails         = Flight.time_details
  TimeScheduled       = TimeDetails.get('scheduled')
  TimeEstimated       = TimeDetails.get('estimated')
  Departure           = "0"
  Arrival             = "0"
  Estimated           = "0"
  OriginDestination   = OriginAirport + " --> " + DestinationAirport

  DepartureTS         = TimeScheduled.get('departure')
  ArrivalTS           = TimeScheduled.get('arrival')
  EstimatedTS         = TimeEstimated.get('arrival')

  if DepartureTS != None:
    Departure = datetime.fromtimestamp(DepartureTS).strftime("%H:%M")

  if ArrivalTS != None:
    Arrival = datetime.fromtimestamp(ArrivalTS).strftime("%H:%M")

  if EstimatedTS != None:
    Estimated = datetime.fromtimestamp(EstimatedTS).strftime("%H:%M")
  else:
    Estimated = Arrival
  
  print("")
  print("")
  print("")
  print("** Closest Aircraft **")
  print('Record:   ',Record)
  print('Hex:      ',Hex)
  print('Flight:   ',Flight)
  print('Heading:  ',Heading)
  print('Distance: ',Distance)
  print('Speed:    ',Speed)
  print('Altitude: ',Altitude)
  print('Messages: ',Messages)
  print('Aircraft: ',AircraftCount)
  print('ORIG:     ',OriginAirportName)
  print('DEST:     ',DestinationAirportName)
  # print('time_data:',TimeDetails)
  print('departure:',Departure)
  print('arrival:  ',Arrival)
  print('estimated:',Estimated)

  TitleFlight        = LED.CreateBannerSprite("Flight")
  TitleDistance      = LED.CreateBannerSprite("Dist")
  TitleSpeed         = LED.CreateBannerSprite("Spd")
  TitleAlt           = LED.CreateBannerSprite("Alt")
  TitleAircraftCount = LED.CreateBannerSprite("UP")
  TitleAircraftType  = LED.CreateBannerSprite("Type")
  TitleHeading       = LED.CreateBannerSprite("HDG")
  TitleDeparture     = LED.CreateBannerSprite("DEP")
  TitleArrival       = LED.CreateBannerSprite("ARR")
  TitleEstimated     = LED.CreateBannerSprite("EST")
  TitleOriginDestination = LED.CreateBannerSprite("FROM --> TO")
  
  ValueFlight        = LED.CreateBannerSprite(Flight.number)
  ValueDistance      = LED.CreateBannerSprite(str(Distance)[0:4] + ' km')
  ValueSpeed         = LED.CreateBannerSprite(str(Speed) + ' kt')
  ValueAlt           = LED.CreateBannerSprite(str(Altitude) + ' ft')
  ValueAircraftCount = LED.CreateBannerSprite(str(AircraftCount))
  ValueAircraftType  = LED.CreateBannerSprite(AircraftType)
  ValueAirlineShort  = LED.CreateBannerSprite(AirlineShortName)
  ValueHeading       = LED.CreateBannerSprite(str(Heading) + '°')
  ValueDeparture     = LED.CreateBannerSprite(Departure)
  ValueArrival       = LED.CreateBannerSprite(Arrival)
  ValueEstimated     = LED.CreateBannerSprite(Estimated)
  ValueOriginDestination = LED.CreateBannerSprite(OriginDestination)

  LED.Canvas.Clear()    
  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleFlight,0,0,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueFlight,28,0,ValueRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleDistance,0,6,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueDistance,28,6,ValueRGB,(0,5,0),1,False,LED.Canvas)
  
  H = LED.HatWidth - (ValueAircraftCount.width + TitleAircraftCount.width + 1)
  V = 0
  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleAircraftCount,H,V,TitleRGB,(0,5,0),1,False,LED.Canvas)
  H = LED.HatWidth - ValueAircraftCount.width
  V = 0
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueAircraftCount,H,V,ValueRGB,(0,5,0),1,False,LED.Canvas)


  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleHeading,63,0,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueHeading,81,0,ValueRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleSpeed,63,6,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueSpeed,81,6,ValueRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleAlt,63,12,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueAlt,81,12,ValueRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleDeparture,0,12,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueDeparture,28,12,ValueRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleArrival,0,18,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueArrival,28,18,ValueRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleEstimated,63,18,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueEstimated,81,18,ValueRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleAircraftType,0,28,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueAircraftType,0,34,ValueRGB2,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueAirlineShort,0,40,ValueRGB2,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleOriginDestination,0,48,TitleRGB,(0,5,0),1,False,LED.Canvas)
  LED.Canvas = LED.CopySpriteToCanvasZoom(ValueOriginDestination,63,48,ScrollingRGB,(0,5,0),1,False,LED.Canvas)

  LED.Canvas = LED.TheMatrix.SwapOnVSync(LED.Canvas)



def Update():
  print("******** UPDATING LIST ********")
  LED.Canvas = LED.CopySpriteToCanvasZoom(TitleUpdating,0,56,ScrollingRGB,(0,5,0),1,False,LED.Canvas)
  FlightList = GetFlightsInBounds()
  DetailedFlightList = GetFlightDetails(FlightList)
  ClosestFlight = GetNearbyFlight(DetailedFlightList)
  LastGetFlightsTime = time.time()
  return ClosestFlight, LastGetFlightsTime

def DisplayNextFlight(record = 0):
  if record < len(DetailedFlightList)-1:
    record = record + 1
  else:
    record = 0
  print("Displaying next flight - record: ", record)
  NextFlight = DetailedFlightList[record]
  DisplayFlight(NextFlight)
  return NextFlight

#------------------------------------------------------------------------------
# MAIN SECTION                                                               --
#------------------------------------------------------------------------------

print ("")
print ("")
print ("---------------------------------------------------------------")
print ("Flight - Display nearby aircraft using FlightRadar24 API       ")
print ("")
print ("BY DATAGOD - revised by RiZ@L72")
print ("")
print ("KEYBOARD SHORTCUTS:")
print ("'U' - Update Flights list")
print ("'N' - Show Next Flight in the list")
print ("---------------------------------------------------------------")
print ("")
print ("")

LED.ClearBigLED()
LED.ClearBuffers()
CursorH = 0
CursorV = 0

LED.ScreenArray,CursorH,CursorV = LED.TerminalScroll(LED.ScreenArray,"LOADING CONFIG FILES",CursorH=CursorH,CursorV=CursorV,MessageRGB=(0,150,0),CursorRGB=(0,255,0),CursorDarkRGB=(0,50,0),StartingLineFeed=1,TypeSpeed=TerminalTypeSpeed,ScrollSpeed=TerminalScrollSpeed)
LoadConfigFile()
#LED.ScreenArray,CursorH,CursorV = LED.TerminalScroll(LED.ScreenArray,"RETREIVING LIST OF AIRPORTS",CursorH=CursorH,CursorV=CursorV,MessageRGB=(0,150,0),CursorRGB=(0,255,0),CursorDarkRGB=(0,50,0),StartingLineFeed=1,TypeSpeed=TerminalTypeSpeed,ScrollSpeed=TerminalScrollSpeed)
# GetAirportList()

#pp.pprint(AirportList)

if InFlight:
  LED.ScreenArray,CursorH,CursorV = LED.TerminalScroll(LED.ScreenArray,"GETTING A LIST OF NEARBY FLIGHTS, THAT ARE IN FLIGHT",CursorH=CursorH,CursorV=CursorV,MessageRGB=(0,150,0),CursorRGB=(0,255,0),CursorDarkRGB=(0,50,0),StartingLineFeed=1,TypeSpeed=TerminalTypeSpeed,ScrollSpeed=TerminalScrollSpeed)
else:
  LED.ScreenArray,CursorH,CursorV = LED.TerminalScroll(LED.ScreenArray,"GETTING A LIST OF NEARBY FLIGHTS, ON THE GROUND OR IN FLIGHT",CursorH=CursorH,CursorV=CursorV,MessageRGB=(0,150,0),CursorRGB=(0,255,0),CursorDarkRGB=(0,50,0),StartingLineFeed=1,TypeSpeed=TerminalTypeSpeed,ScrollSpeed=TerminalScrollSpeed)

FlightList = GetFlightsInBounds()

LED.ScreenArray,CursorH,CursorV = LED.TerminalScroll(LED.ScreenArray,"RETRIEVING FLIGHT DETAILS",CursorH=CursorH,CursorV=CursorV,MessageRGB=(0,150,0),CursorRGB=(0,255,0),CursorDarkRGB=(0,50,0),StartingLineFeed=1,TypeSpeed=TerminalTypeSpeed,ScrollSpeed=TerminalScrollSpeed)
DetailedFlightList = GetFlightDetails(FlightList)
LastGetFlightsTime = time.time()


# an example "flight"
# [<(B350) C-GSYC - Altitude: 4375 - Ground Speed: 206 - Heading: 129>
#details = fr_api.get_flight_details('B350')
#pp.pprint(details)
#time.sleep(2)

LED.ClearBigLED()
LED.ClearBuffers()

### HERE IS WHERE THE MAGIC HAPPENS

CurrentFlight = GetNearbyFlight(DetailedFlightList)

while(1==1):
  h,m,s = LED.GetElapsedTime(LastGetFlightsTime,time.time())
  
  #update master list of flights every X minutes
  print("HMS",h,m,s)
  print("LastGetFlightsTime",LastGetFlightsTime)
  if (m >= GetFlightsWaitMinutes):
    CurrentFlight, LastGetFlightsTime = Update()

  ### CHECK KEYBOARD: 'u' for Update, 'n' for next Flight
  #Key = LED.PollKeyboard()
  if (LED.KeyPressed == 'u'):
    LED.KeyPressed = ''
    CurrentFlight, LastGetFlightsTime = Update()

  if (LED.KeyPressed == 'n'):
    LED.KeyPressed = ''
    CurrentFlight = DisplayNextFlight(CurrentFlight.record)

  #--------------------------------------------------
  #Create scrolling text with additional information
  #--------------------------------------------------
  
  try:
    ScrollText = OriginAirport + " - " + DestinationAirport + " : " + OriginAirportName.rsplit(' ', 1)[0] + " --> " + DestinationAirportName.rsplit(' ', 1)[0]

    LED.ShowScrollingBanner2(ScrollText,ScrollingRGB,ScrollSpeed=ScrollSleep,v=56)
  except:
    ScrollText="No flights in range! Next update in " + str(GetFlightsWaitMinutes) + " minutes."
    print(ScrollText)
    LED.ShowScrollingBanner2(ScrollText,ScrollingRGB,ScrollSpeed=ScrollSleep,v=56)
  
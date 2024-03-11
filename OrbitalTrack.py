from skyfield.api import load, wgs84
import threading

lock = threading.Lock()
myPos = wgs84.latlon(+43.901, -78.976, elevation_m = 98)

def findAltAzDist(objPos, obsPos, time):
    difference = objPos - obsPos
    altitude, azimuth, distance = difference.at(time).altaz()
    return azimuth.degrees, altitude.degrees, distance.km

def satPosNow(sat, satName):
    print("\n" + satName + " update has been acquired.")
    ts = load.timescale()
    timeNow = ts.now()
    geocentricPos = sat.at(timeNow)
    geographicPos = wgs84.geographic_position_of(geocentricPos)
    kmElevation = geographicPos.elevation.km
    return geographicPos, kmElevation

def removeSpace(value):
    newString = ""
    ifBreak = False
    for i in value:
        if i == " " and not ifBreak:
            ifBreak = True
        else:
            newString += i
    return newString

def handleResponse(message):
    url = 'https://celestrak.org/NORAD/elements/stations.txt'
    allSat = load.tle_file(url)
    print("\nTLE sets installed.")
    name = {sat.name: sat for sat in allSat}
    userInput = message.upper()

    if userInput[0:4] == "?GET":
        userInput = removeSpace(userInput)[4:]
        satName = userInput
        if userInput == "CSS":
            userInput = "CSS (TIANHE)"
            satName = "CSS"
        elif userInput == "ISS":
            userInput = "ISS (ZARYA)"
            satName = "ISS"
        if userInput in name:
            altAzDist = findAltAzDist(name[userInput], myPos, load.timescale().now())
            satPos = satPosNow(name[userInput], satName)
            azimuth, altitude, distance = [round(i, 2) for i in list(altAzDist)]
            geographicPos = satPos[0]
            kmElevation = round(satPos[1], 2)
            return f"{satName} Update: \n{geographicPos} or {kmElevation} km\n\tAzimuth: {azimuth}°\n\tElevation angle: {altitude}°\n\tDistance: {distance} km\n"
        else:
            return f"Such satellite ({removeSpace(message)[4:]}) doesn't exist!"
    
    if userInput == "HELLO" or userInput == "HI" or userInput == "HEY" or userInput == "YO":
        return "Hello!!"
    
    if userInput == "?COMMANDS":
        return "***Commands:***\n\t\- *`?get`*  followed by the name of a satellite finds the position of that satellite\n\t\- *`?syntax`*  lists the `?get` command syntax for all available satellites\n\t\- *`?info`*  provides you some information about this bot\n\t\- *`?commands`*  you are already here, aren't you? : )"

    if userInput == "?SYNTAX":
        return "***Syntax (Updated 2024/03/10):***\n\t\- International Space Station: *`ISS`*\n\t\- China Space Station (Tiangong): *`CSS`*\n\t\- Tianzhou-7: *`TIANZHOU-7`*\n\t\- Shenzhou-17: *`SHENZHOU-17 (SZ-17)`*\n\t\- Progress MS-25: *`PROGRESS-MS 25`*\n\t\- Progress MS-26: *`PROGRESS-MS 26`*\n\t\- Soyuz MS-24: *`SOYUZ-MS 24`*\n\t\- Crew Dragon 7: *`CREW DRAGON 7`* \n\t\- Crew Dragon 8: *`CREW DRAGON 8`*\n\t\- Cygnus NG-20: *`CYGNUS NG-20`*\n\n\t**Note: The syntaxes are NOT case sensitive, but are character sensitive!*"
    
    if userInput == "?INFO":
        return "The positional information of the satellites are calculated with TLE (Two-Line Element) files using Python's skyfield library!"
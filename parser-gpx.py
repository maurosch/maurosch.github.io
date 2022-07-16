import gpxpy
import gpxpy.gpx

# Parsing an existing file:
# -------------------------

gpx_file = open(input("File: "), 'r')

gpx = gpxpy.parse(gpx_file)

fileOutput = open(input("Output File: "), "w")
first = True
fileOutput.write(f'[\n')
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            if first: 
                first = False
            else:
                fileOutput.write(',\n')
            fileOutput.write(f'[{point.latitude},{point.longitude}]')
            print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))

fileOutput.write(f']\n')
fileOutput.close()

#for waypoint in gpx.waypoints:
#    print('waypoint {0} -> ({1},{2})'.format(waypoint.name, waypoint.latitude, waypoint.longitude))

#for route in gpx.routes:
#    print('Route:')
#    for point in route.points:
#        print('Point at ({0},{1}) -> {2}'.format(point.latitude, point.longitude, point.elevation))
import VehicleCSV as v
import FileCSV as f
import sys

file = sys.argv[1]

vehiclex = v.vehicle()
vehiclex.setdatafile(file)
vehiclex.create()

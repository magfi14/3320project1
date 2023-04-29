import FileCSV as f
import sys


class vehicle:
    CLASSES = ["MICRO", "SUBCOMPACT", "COMPACT",
               "MIDSIZE", "FULLSIZE", "EXTENDED"]
    TYPES = ["SEDAN", "COUPE", "WAGON", "SUV", "MINIVAN", "VAN", "PICKUP"]

    CLASS = ""
    TYPE = ""
    YEAR = 0
    MAKE = ""
    MODEL = ""
    TRIM = ""
    POWERTRAIN = ""
    FLEET = 0

    FILE = None
    DATAMANAGER = None

    keys = ["CLASS", "TYPE", "YEAR", "MAKE",
            "MODEL", "TRIM", "POWERTRAIN", "FLEET"]

    def __init__(self):
        self.CLASS = ""
        self.TYPE = ""
        self.YEAR = 0
        self.MAKE = ""
        self.MODEL = ""
        self.TRIM = ""
        self.POWERTRAIN = ""
        self.FLEET = 0
        pass

    def setdatafile(self, name):
        self.FILE = f.file()
        self.FILE.setfilename(name)
        self.DATAMANAGER = f.datamanager(self.FILE)

    def getkeys(self):
        return list(self.keys)

    def getlist(self):
        return [self.CLASS, self.TYPE, self.YEAR, self.MAKE, self.MODEL, self.TRIM, self.POWERTRAIN, self.FLEET]

    def setlist(self, lst):
        self.CLASS = lst[0]
        self.TYPE = lst[1]
        self.YEAR = lst[2]
        self.MAKE = lst[3]
        self.MODEL = lst[4]
        self.TRIM = lst[5]
        self.POWERTRAIN = lst[6]
        self.FLEET = lst[7]

    def createx(self, key="CLASS", step=1, prompt="C", rowno=-1):
        if prompt == "U":
            row = int(input("Row to change: "))
            if row < 0 or row >= self.DATAMANAGER.nrows():
                print(
                    "ERROR: ROW {rowx} DOES NOT EXIST! TRY AGAIN!".format(rowx=row))
                self.createx(prompt='U', rowno=row)
            else:
                self.createx(self.keys[step - 1], step, "C", rowno)
        elif prompt == "C":
            if step == 1:
                vclass = str(input("{keyx}: ".format(keyx=key))).upper()
                if vclass in self.CLASSES:
                    self.CLASS = vclass.upper()
                    self.createx(self.keys[step], step + 1, "C", rowno)
                else:
                    print("DOES NOT EXIST!")
                    self.createx(self.keys[step - 1], step, "C", rowno)
            elif step == 2:
                vtype = str(input("{keyx}: ".format(keyx=key))).upper()
                if vtype in self.TYPES:
                    self.TYPE = vtype.upper()
                    self.createx(self.keys[step], step + 1, "C", rowno)
                else:
                    print("DOES NOT EXIST!")
                    self.createx(self.keys[step - 1], step, "C", rowno)
            elif step == 3:
                self.YEAR = int(input("{keyx}: ".format(keyx=key)))
                self.createx(self.keys[step], step + 1, "C", rowno)
            elif step == 4:
                self.MAKE = str(input("{keyx}: ".format(keyx=key))).upper()
                self.createx(self.keys[step], step + 1, "C", rowno)
            elif step == 5:
                self.MODEL = str(input("{keyx}: ".format(keyx=key))).upper()
                self.createx(self.keys[step], step + 1, "C", rowno)
            elif step == 6:
                self.TRIM = str(input("{keyx}: ".format(keyx=key))).upper()
                self.createx(self.keys[step], step + 1, "C", rowno)
            elif step == 7:
                self.POWERTRAIN = str(
                    input("{keyx}: ".format(keyx=key))).upper()
                self.createx(self.keys[step], step + 1, "C", rowno)
            elif step == 8:
                self.FLEET = str(input("{keyx}: ".format(keyx=key))).upper()
        return rowno

    def create(self, prx=''):
        acceptables = ['C', 'R', 'U', 'D', 'N', 'W']
        removables = ['D', 'W']
        datamanipulation = ['R', 'N', 'U']
        datax = {
            "C": "CREATE A NEW VEHICLE: ",
            "R": "RETRIEVE VEHICLES FROM THE FILE: ",
            "U": "UPDATE VEHICLE: ",
            "D": "DELETE VEHICLE FROM FILE: ",
            "N": "RETRIEVE NUMBER OF VEHICLES FROM FILE: ",
            "W": "WIPE FILE CLEAN: ",
            "Q": "DATA MANIPULATION STOPPPED!"
        }
        if prx == '':
            prompt = str(input(
                "Type C for Create, R for Retrieve, U for Update, D for Delete, N for Number of Entries, W for wipe file clean or Q for Quit: ")).upper()
            self.create(prx=str(prompt))
        else:
            print(datax[prx])
        if prx in acceptables:
            if not prx in removables:
                if prx == 'R':
                    print(self.DATAMANAGER.retrieve())
                elif prx == 'U':
                    if self.DATAMANAGER.nrows() > 0:
                        rowno = self.createx(prompt='U')
                        self.DATAMANAGER.update(rowno, self.getlist())
                    else:
                        print("NOTHING TO UPDATE!")
                        self.create('C')
                elif prx == 'N':
                    print("THERE ARE {n} VEHICLES IN THE SELECTION!".format(
                        n=self.DATAMANAGER.nrows()))
                if not prx in datamanipulation:
                    self.createx()
                    if prx == 'C':
                        self.DATAMANAGER.create(self.getlist())
            else:
                if self.DATAMANAGER.nrows() > 0:
                    if prx == 'D':
                        row = int(input("Row to delete: "))
                        self.DATAMANAGER.delete(row)
                    elif prx == 'W':
                        self.DATAMANAGER.clear()
                else:
                    print("NOTHING TO DELETE!")
                    self.create()
            if not prx == 'Q':
                self.create()
        else:
            if not prx.upper() == 'Q':
                print(
                    "DID NOT TYPE C [CREATE], R [RETRIEVE], U [UPDATE], D [DELETE], W [WIPE FILE CLEAN] OR N [FILE SIZE]. TRY AGAIN, OR TYPE [Q] TO STOP!\n")
            if not prx.upper() == 'Q':
                self.create()
            else:
                sys.exit()

    def __str__(self):
        string = "{vclass} {vtype} {vyear} {vmake} {vmodel} {vtrim} {vpower} {vfleet}".format(
            vclass=self.CLASS, vtype=self.TYPE, vyear=self.YEAR, vmake=self.MAKE, vmodel=self.MODEL, vtrim=self.TRIM, vpower=self.POWERTRAIN, vfleet=self.FLEET)
        return string

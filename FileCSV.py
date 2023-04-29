import Manager as fm  # import the data management module
import os


class datamanager:
    filex = None
    filepath = None

    def __init__(self, filex):
        self.filex = filex
        self.filepath = filex.getfullpath()

    def getheaders(self):
        return fm.readheadersw(self.filepath)

    def create(self, values, code='C'):
        return fm.addrowfile(self.filepath, values, code)

    def retrieve(self, rowid=-1):
        return fm.readfromw(self.filepath, rowid)

    def update(self, rowid, values, code='U'):
        return fm.upfile(self.filepath, rowid, values, code)

    def delete(self, rowid=-1):
        self.filex.duplicate()
        return fm.delfile(self.filepath, rowid)

    def nrows(self):
        return fm.numrowsif(self.filepath)

    def clear(self):
        return fm.clearfile(self.filepath)


class file:
    filename = ""
    extension = ".csv"
    fullpath = ""
    prelimfilename = ""
    path = ""

    def __init__(self):
        pass

    def setfilename(self, fname, includeext=True, path=""):
        self.prelimfilename = str(fname)
        self.path = path
        if includeext:
            if len(path) > 0:
                self.filename = self.path + "/" + \
                    self.prelimfilename + str(self.extension)
            else:
                self.filename = self.prelimfilename + str(self.extension)
        else:
            if len(path) > 0:
                self.filename = self.path + "/" + self.prelimfilename
            else:
                self.filename = self.prelimfilename

    def getfilename(self, includepath=False, includeext=False):
        if not includepath:
            if includeext:
                return str(self.prelimfilename) + str(self.extension)
            else:
                return str(self.prelimfilename)
        else:
            return self.getfullpath()

    def getdupfilename(self):
        return str(self.prelimfilename) + "_copy" + str(self.extension)

    def getfullpath(self):
        fullpath = "{f}".format(f=self.filename)
        return str(fullpath)

    def fixdirectory(self, directory):
        newdirectory = directory.replace(chr(92), chr(47))
        return newdirectory

    def getfiles(self, path=False):
        pathx = ""
        if path:
            pathx = self.path
        else:
            pathx = "."
        return [filex for filex in os.listdir(pathx) if filex.endswith('.csv')]

    def filenamepartial(self, filenamez, path=False):
        filelist = self.getfiles(path)
        fileexists = False
        for filex in filelist:
            if filenamez in filex:
                fileexists = True
                break
        return fileexists

    def delete(self, filenamez="", includepath=False, dup=False, path=False):
        fname = ""
        if not dup:
            if len(filenamez) > 0:
                fname = filenamez
            else:
                fname = self.getfilename(includepath)
        else:
            fname = self.getdupfilename()
        if self.filenamepartial(fname):
            try:
                os.remove(fname)
                return "Successfully deleted {f} from the directory.".format(f=fname)
            except OSError as o:
                return "File could not be deleted. It does not exist."
        else:
            return "Preliminary examination failed. File does not exist in the list."

    def copycontents(self, s="", d="", showcontents=False, clear=False, path=False):
        sourcefile = ""
        if len(s) > 0:
            sourcefile = s
        else:
            sourcefile = self.getfilename(includeext=True)
        if len(d) > 0:
            dx = d
        else:
            dx = self.getdupfilename()
        destfile = file()
        destfile.setfilename(dx, False)
        if self.filenamepartial(sourcefile, path) and not self.filenamepartial(destfile.getfilename(), path):
            try:
                with open(sourcefile, 'r') as source:
                    c = source.read()
                with open(destfile.getfilename(), 'w') as dest:
                    dest.write(c)
            except FileNotFoundError:
                return "The source file {sourcefilex} or duplicate file {duplicatefilex} does not exist in the directory {directory}".format(sourcefilex=sourcefile, duplicatefilex=destfile.getfilename(), directory=self.path)
            if showcontents:
                man = datamanager(destfile)
                if clear:
                    man.clear()
                return man.retrieve()
            else:
                return "File copied!"
        else:
            if not sourcefile in self.getfiles():
                return "{source} does not exist in the desired directory. Files in directory: {list}".format(source=sourcefile, list=self.getfiles())
            elif self.filenamepartial(destfile.getfilename()):
                return "{duplicate} exists in the desired directory.".format(duplicate=destfile.getfilename())

    def duplicate(self, showcontents=False, clear=False):
        originalfile = self.getfilename()
        newfile = self.getdupfilename()
        return self.copycontents(originalfile, newfile, showcontents, clear)

    def __str__(self):
        return self.getfullpath()

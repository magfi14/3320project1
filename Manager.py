import pandas as p

def readfrom(file, *series) :
    data = p.read_csv(file, usecols = series)
    return data

def readheadersfromframe(frame) :
    return frame.columns

def readheadersw(file) :
    data = p.read_csv(file)
    return data.columns

def readfromw(file, rowid=-1) :
    data = None
    if rowid == -1 or rowid >= numrows(p.read_csv(file)):
        data = p.read_csv(file)
    else :
        data = p.read_csv(file).loc[rowid]
    return data

def numrows(frame) :
    return frame.shape[0]

def numrowsif(file) :
    return numrows(readfromw(file))

def upframew(frame, rowid, values, code='C') :
    if code == 'C' :
        frame.loc[rowid] = values
    elif code == 'U' :
        frame.iloc[rowid] = values
    return frame

def upfile(file, rowid, values, code='C') :
    frame = readfromw(file)
    frame = upframew(frame, rowid, values, code)
    frame.to_csv(file, index = False)
    return frame

def addrowframe(frame, values, rowid=-1, code='C') :
    return upframew(frame, numrows(frame), values, code)

def addrowfile(file, values, code='C') :
    return upfile(file, numrows(readfromw(file)), values, code)

def delrow(frame, rowid=-1) :
    if rowid == -1 or rowid >= numrows(frame) :
        frame = frame.drop(numrows(frame) - 1)
    else :
        frame = frame.drop(rowid)
    return frame

def delfile(file, rowid=-1) :
    return delrow(readfromw(file), rowid).to_csv(file, index = False)

def clearframe(frame) :
    while numrows(frame) > 0 :
        frame = delrow(frame)
    return frame

def clearfile(file) :
    return clearframe(readfromw(file)).to_csv(file, index = False)

def createdictionaryfrom(file) :
    data = {}
    for headername in readheadersw(file) :
        data[headername] = None
    return data

def extractkeys(dictionary) :
    listofkeys = dictionary.keys()
    keylist = []
    for key in listofkeys :
        keylist.append(key)
    return keylist

def extractkeysff(file) :
    dictionary = createdictionaryfrom(file)
    return extractkeys(dictionary)

def find(frame, column, keyword) :
    headers = readheadersfromframe(frame)
    return frame[frame[column].str.contains(keyword.upper())] if column in headers else frame

def findbulksc(frame, column, keywords) :
    framelist = []
    for keywordx in keywords :
        framex = find(frame, column, keywordx)
        framelist.append(framex)
    return p.concat(framelist)

def sortframe(frame, columnlist, ascend=[]) :
    return frame.sort_values(by=columnlist, ascending=ascend)

#file = "Project 1 CSV\ds1.csv"
#frame = readfromw(file)
#print(findbulksc(frame, "MAKE", ["TOYOTA", "SUBARU"]))
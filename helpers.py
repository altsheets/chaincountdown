#!/usr/bin/python
"""
@title:   helpers.py 

@summary: all those little tools that have no other home

@author:  AltSheets
@version: v10

@license  Giveback license v05 http://altsheets.ddns.net/give/

@requires only stuff from python itself
@see      chaincountdown.py for explanations & donation addresses
"""

from time import gmtime, strftime
import os, tempfile, getpass, sys, datetime

def theNowInReadable():
    return strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())


def dirnames():
    currentDir = os.path.join(os.path.dirname(__file__),"")
    tempDir    = os.path.join(tempfile.mkdtemp(),       "")
    return currentDir, tempDir  

def username():
    """Try to get the real username (not the environment variable).
       Only in Linux - for that 'import pwd'. 
       If that fails (i.e. Windows), use getpass.
    """
    try:
        import pwd 
        username = pwd.getpwuid( os.getuid() )[ 0 ]
    except (ImportError, AttributeError):
        # for Windows:
        username = getpass.getuser()
    return username

def suffix(f):
    return os.path.splitext(f)[1]

def nameWOsuffix(f):
    return os.path.splitext(f)[0] 

def filesInFolder(path, suffixlist=None):
    files=os.listdir(path)
    if suffixlist!=None:
        files=[f for f in files if suffix(f) in suffixlist]
    return files

def test_filesInFolder():
    print filesInFolder("html")
    fonts = os.path.join(dirnames()[0], "fonts")
    print filesInFolder(fonts, (".ttf",))# ".css") )

def replacedInDict(defaults, overwrite):
    "to take default values unless options are specified"
    result=defaults.copy()
    for k,v in overwrite.items():
        result[k]=v
    return result

def cutUpText(text, maxLen):
    "cuts each line at max length"
    resultText=""
    for line in text.split("\n"):
        while True:
            resultText += line[:maxLen] + "\n"
            line = line[maxLen:]
            if len(line) <=maxLen:
                break
        if line!="": resultText += line + "\n"
    return resultText

def mkdirIfNotExist(dirname):
    try:
        os.mkdir(dirname)
    except:
        return False
    return True


if __name__ == "__main__":
    print theNowInReadable()
    print dirnames()
    print username()
    print 
    test_filesInFolder()
    
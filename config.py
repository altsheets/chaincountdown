#!/usr/bin/python
'''
@title:   config.py
@summary: Change these defaults - if you know what you are doing

@author:  AltSheets
@version: v10

@TODO:    needs re-ordering to be more logical
'''

PORT_NUMBER = 8888
TIMEOUT     = 3

# coins specifics:

SERVER ={
         "nxt" : "http://jnxt.org:7876/nxt",
         # "nxt" : "http://localhost:7876/nxt",
         
         "nhz" : "http://api.nhzcrypto.org:7776/nhz",
         # "nhz":  "http://localhost:7776/nhz",
         }

BLOCKSPERMINUTE = {"nxt": 1 / 1.9005,
                   "nhz": 1 / 1.7861}
GENESIS = {"nhz": 1395526942.22, 
           "nxt": 1385294400}


# subfolders:
FONTFOLDER = "fonts"
FONTSUFFIX = (".ttf", ".otf",)

STATICFOLDER = "static"
STATICSUFFICES = (".html", ".htm", ".css", ".png", ".ico")


# text webserver:

EXAMPLE     = "http://%s/nxt/600000.png?heading=nxthacks&color=00affe&fontsize=20"
SUGGESTION  = "Your URL should look like: | %s |" % EXAMPLE

INFOPAGE    ="index.html"
STYLESHEET  ="yo.css"

TEXTSAMPLE="""4465 blocks left to target.
From current block 491532
~5.9 days. My best guess:
13 Aug 2015 03:09:37 UTC"""


# date, path and OS operations:
import helpers
import os, sys

STARTED_AT  = helpers.theNowInReadable()
USERNAME    = helpers.username()
BASEDIR, TEMPDIRNAME = helpers.dirnames()

FONTDIR = os.path.join(BASEDIR, FONTFOLDER )
FONTS   = helpers.filesInFolder(FONTDIR, FONTSUFFIX ) + ["",] # for default font
# FONTS = map(helpers.nameWOsuffix, FONTS) # strip the suffix

STATICDIR = os.path.join(BASEDIR, STATICFOLDER)
PAGES   = helpers.filesInFolder(STATICDIR, STATICSUFFICES )

MIMETYPE = {".html" : "text/html",
            ".css"  : "text/css",
            ".png"  : "image/png",
            ".ico"  : "image/x-icon"}

# picture defaults:

FOOTER = "#chaincountdown.py by @AltSheets "
FONTSIZEFOOTER_MIN=9 # or fontsize/2 or:

# fonts become unreadable below certain sizes,
# this is used for the footer line
# can be easily decided with the help of 
# imaging_tests.test_FontSizes()

FONTMINIMA = {"Pecita.otf"      : 13, 
              "AndBasR.ttf"     : 10,
              "arial.ttf"       : 9,
              "comic.ttf"       : 9,
              "cour.ttf"        : 11,
              "DejaVuSans.ttf"  : 9,
              "Furore.otf"      : 13,
              "Gidole-Regular.otf" : 13}

IMAGETYPES = ("jpg", "gif", "png")
FILENAMEPIC = "temp"

FONTDEFAULT = "DejaVuSans.ttf" # or take the first one found:
FONTDEFAULT = FONTDEFAULT if FONTDEFAULT in FONTS else FONTS[0]  

IMAGEDEFAULTS = {"color"            : "#111111",
                 "bgcolor"          : "#eeeeee",
                 "font"             : FONTDEFAULT,
                 "fontsize"         : 24,
                 "linedistanceratio": 0.2,
                 "headingfontsize"  : 36,
                 "heading"          : "",
                 "footerfontsize"   : 9,
                 "footer"           : FOOTER,
                 "maxcharsperline"  : 58,
                 "jpgquality"       : 99}

ALLFONTSIMAGEDEFAULTS = {"file"       :"allfonts.png",
                         "fontsize"   : 20,
                         "lineHeight" : 1.3, 
                         "border"     : 10,
                         "color"      : "#336699",
                         "bgcolor"    : "#DCDCDC"}

TESTTEXT = "The quick brown fox jumps over the lazy dog! 1234567890 :?!.@#"



# print a status to stderr (because that gets daemon logged perfectly)
 
print >> sys.stderr,  "Static pages from '%s'\nTemp files into '%s'" % (STATICDIR, TEMPDIRNAME)
print >> sys.stderr,  "Static files available: %s" % ", ".join(PAGES)
if len(FONTS)==1: 
    print >> sys.stderr,  "no fonts found, sorry exiting."
    exit(1)
# print >> sys.stderr,  "fonts available: %s" % ", ".join([helpers.nameWOsuffix(f) for f in FONTS[:-1]])
print >> sys.stderr,  "Fonts available: %s" % ", ".join(FONTS[:-1])
print >> sys.stderr,  "Default font: %s" % FONTDEFAULT
print >> sys.stderr,  "Time now: %s\nRunning this as: '%s'" % (STARTED_AT, USERNAME)

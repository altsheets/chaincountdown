#!/usr/bin/python
'''
@title:   imaging_tests.py 

@summary: writes one image for each font, with increasing fontsizes
          + all the tests for imaging.py

@author:  AltSheets
@version: v10

@license  Giveback license v05 http://altsheets.ddns.net/give/

@requires config.py, imaging.py, helpers.py
@see      chaincountdown.py for explanations & donation addresses
 
'''

from imaging import textToImage, manyFontSizes_image, showAllFonts_image, findMatchingFont
from config import TEXTSAMPLE, FONTS
import helpers

import timeit, os

def testFontFinder():
    print findMatchingFont("cour", FONTS)
    print findMatchingFont("cour.ttf", FONTS)
    print findMatchingFont("Furore.otf", FONTS)

def test_Image(folder, font, filename="test3.png", ):
    "generate image, with overwriting default options"
    options = {"headingfontsize" : 50,
               "heading"         : "heading",
               "fontsize"        : 100,
               "font"            : font }
    textToImage(os.path.join(folder,filename), "testline1\ntestline2", **options)
 
 
def test_textSampleToImage(folder, font=None, filenames=("test4.png","test5.png"), text=TEXTSAMPLE):
    "generate an image with header, and one without."

    bef=timeit.default_timer()
    
    textToImage(os.path.join(folder, filenames[0]), text) # ALL defaults

    options= {"color"   : "ff2277",
              "bgcolor" : "00ff44",
              "heading" : "nxthacks VOTING"}
    if font!=None: options["font"] = font
    textToImage(os.path.join(folder, filenames[1]), text, **options)

    print "Generating 2 images took %.3f seconds" % (timeit.default_timer()-bef)
 
   

def test_FontSizes(dirname="samples"):
    """very useful for deciding what is the minimum size,
       then put it into config.FONTMINIMA"""
    
    for font in FONTS[:-1]:
        print "%s --> " % font,  
        outfile=os.path.join(dirname, helpers.nameWOsuffix(font)+ ".png")
        bef=timeit.default_timer()
        manyFontSizes_image(fontfilename=font, filename=outfile,
                            fontsizes=range(5,20,1))
        print "%s  (generated in %.3f seconds)" % (outfile, timeit.default_timer()-bef)



if __name__ == "__main__":
    folder="samples"
    helpers.mkdirIfNotExist(folder)
    
    # testFontFinder()

    # fontfilename="Furore.otf"
    # test_Image(folder, fontfilename, )              # simple text
    # test_textSampleToImage(folder, fontfilename)    # text sample like countdown text
    
    # showAllFonts_image(filename=os.path.join(folder, "allfonts.png"))
    
    test_FontSizes(dirname="samples")

    
    
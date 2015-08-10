#!/usr/bin/python
'''
@title:   imaging.py 
@summary: make image from text

@author:  AltSheets
@version: v10

@license  Giveback license v05 http://altsheets.ddns.net/give/

@requires config.py
@see      chaincountdown.py for explanations & donation addresses
 
'''

from config import IMAGEDEFAULTS, TEXTSAMPLE, FONTDIR, FONTS, FONTMINIMA
from config import STATICDIR, ALLFONTSIMAGEDEFAULTS, TESTTEXT

from helpers import nameWOsuffix, replacedInDict, cutUpText
import timeit, os

import PIL 
## sudo pip install Pillow
## sudo aptitude install libfreetype6-dev
from PIL import ImageFont, Image, ImageDraw



def manyFontSizes_image(textline=TESTTEXT, filename="sizes.png", 
                  fontfilename="Pecita.otf", fontsizes=range(10,30,2),
                  lineHeight = 1.5, border = 10):
    """Says what it does. Generates image with different fontsizes."""
       
    fontface=os.path.join(FONTDIR, fontfilename)

    width = ImageFont.truetype(fontface, max(fontsizes)).getsize("123"+textline)[0] + 2*border
    height = int(sum(fontsizes) * lineHeight + 2 * border)
    # print width, height
    
    img  = Image.new("RGBA", (width, height), "#dddddd")
    draw = ImageDraw.Draw(img)
    
    # fontname:
    font = ImageFont.truetype(fontface, max(fontsizes) )
    textwidth=font.getsize(fontfilename)[0]
    draw.text((width-textwidth-10, 10), fontfilename, "#333333", font=font)
    
    startPos = border  
    for fontsize in fontsizes:
        font = ImageFont.truetype(fontface, fontsize)
        draw.text((border, startPos),("%2d "%fontsize) + textline, "#333333", font=font)
        startPos+= int(lineHeight * fontsize) 
    
    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)
    
    img.save(filename)

def showAllFonts_image(textline=TESTTEXT, filename="allfonts.png", 
                  fontfilenames=FONTS[:-1], fontsize=20,
                  lineHeight = 1.3, border = 10,
                  color="#333333", bgcolor="#dddddd"):
    """Says what it does. Generates image with all known fonts."""

    def text(fname):
        "one line printer"
        return "%s    "%nameWOsuffix(fname) + textline

    # generate fonts & widths & width & height
    font={}
    widths={}
    for fname in fontfilenames:
        fname = findMatchingFont( fname, FONTS)
        font[fname]  = ImageFont.truetype( os.path.join(FONTDIR, fname), fontsize) 
        widths[fname] = font[fname].getsize(text(fname))[0] + 2*border
    width=max(widths.values())
    height = int(len(fontfilenames) * fontsize* lineHeight + 2 * border)
    # print width, height
    
    # new canvas:
    img  = Image.new("RGBA", (width, height), bgcolor)
    draw = ImageDraw.Draw(img)
    
    # sort by width:
    sortedByWidth=widths.items()
    sortedByWidth.sort(key=lambda x: x[1])
    sortedByWidth=zip(*sortedByWidth)[0]
    
    # draw the text lines:
    startPos = border
    for fname in sortedByWidth:
        draw.text((border, startPos), text(fname), 
                  color, font=font[fname])
        startPos+= int(lineHeight * fontsize) 
    
    # finish the image
    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)
    img.save(filename)

def putAllFontsImageIntoFolder(dirname, **o):
    filepath=os.path.join(dirname, o["file"])
    
    showAllFonts_image(textline=TESTTEXT, filename=filepath, 
                 fontsize=o["fontsize"], lineHeight=o["lineHeight"], 
                 border = o["border"],
                 color=o["color"], bgcolor=o["bgcolor"])
    
    print "Ready. New font file with all %d available fonts shown exists now: \n%s" % (len(FONTS[:-1]), filepath)

#### here comes the main 'textToImage' routine

def correctTheTypes(options):
    "the options arrive in type string, so correct them here"
    for k in ("color", "bgcolor"): 
        options[k] = options[k] if options[k][0] =="#" else "#" + options[k]
        # print options[k]
    for k in ("fontsize", "headingfontsize", "footerfontsize", "maxcharsperline"):
        options[k] = int (options[k] )
    

def findMatchingFont(wanted, searchlist):
    hits=[f for f in searchlist if f.startswith(wanted)]
    if hits==[]: return None
    return hits[0]

def minFooter(wish, filename, minima=FONTMINIMA):
    return max(wish, minima.get(filename, 0))

def textToImage(filename, text, **options):
    """Says what it does. 
       One long subroutine only because it is a simply a serial process.
       N.B. filetype polymorphism depending on suffix of filename"""
       
    # defaults are overwritten by user choices
    o = replacedInDict(IMAGEDEFAULTS, options)
    correctTheTypes(o) # type string to whatever needed here.
    
    # get the fontface:
    fontfilename = findMatchingFont( o["font"], FONTS)
    fontface=os.path.join(FONTDIR, fontfilename)
    
    # allow empty heading
    if o["heading"]!="":
        fontHeading = ImageFont.truetype(fontface, o["headingfontsize"])
        headingLength=fontHeading.getsize(o["heading"])[0]
    else:
        headingLength=0
        o["headingfontsize"]=0

    # footer font & length:
    #print o["footerfontsize"]
    o["footerfontsize"] = minFooter(o["footerfontsize"], fontfilename) 
    #print o["footerfontsize"]
    fontFooter = ImageFont.truetype(fontface,o["footerfontsize"])
    footerLength = fontFooter.getsize(o["footer"])[0]
    
    # prepare text
    text  = cutUpText(text, o["maxcharsperline"])
    lines = text.rstrip().split("\n")
    
    # font -> line lengths -> pixel width & height
    font = ImageFont.truetype(fontface, o["fontsize"])
    lineDistance        = int ( o["fontsize"]         * o["linedistanceratio"] )
    lineDistanceHeading = int ( o["headingfontsize"]  * o["linedistanceratio"] )
    border       = lineDistance
    lineWidths = [font.getsize(line)[0] for line in lines]

    width=max(max(lineWidths), headingLength, footerLength) + 2 * border
    
    # this reflects the line structure of the image:  
    height =  border
    height += (o["headingfontsize"] + lineDistanceHeading) if o["heading"]!="" else 0
    height += (o["fontsize"]  + lineDistance) * len(lines) 
    height += int(0.5 * o["footerfontsize"]) + o["footerfontsize"] + border 
    
    # PIL stuff
    img  = Image.new("RGBA", (width, height), o["bgcolor"])
    draw = ImageDraw.Draw(img)
    
    startPos=lineDistance
    
    # heading:
    if o["heading"]!="":
        draw.text(((width-headingLength)/2, startPos),o["heading"],o["color"],font=fontHeading)
        startPos += o["headingfontsize"] + lineDistanceHeading 
        
    # main text:
    for i, line in enumerate(lines):
        draw.text(((width-lineWidths[i])/2, startPos),line,o["color"],font=font)
        startPos += o["fontsize"] + lineDistance
    
    # footer:
    startPos += int(0.5 * o["footerfontsize"])
    draw.text((width-footerLength-border, startPos),o["footer"],o["color"],font=fontFooter)
    
    # PIL stuff
    draw = ImageDraw.Draw(img)
    draw = ImageDraw.Draw(img)
    
    # save to file
    if filename.endswith("jpg"):
        img.save(filename, quality=o["jpgquality"])
    else:
        img.save(filename)

 
if __name__ == "__main__":
    
    putAllFontsImageIntoFolder(dirname=STATICDIR, **ALLFONTSIMAGEDEFAULTS)
    exit()
    

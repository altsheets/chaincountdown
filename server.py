#!/usr/bin/python
'''
@title:    chaincountdownserver.py
@summary:  Image generating http server

@author:   AltSheets
@version:  v10

@license   Giveback license v05 http://altsheets.ddns.net/give/

@requires  config.py, imaging.py,chaincountdown.py 
@see       chaincountdown.py for explanations & donation addresses

'''

import chaincountdown, imaging, helpers 

from config import PORT_NUMBER, INFOPAGE, STYLESHEET, SUGGESTION
from config import SERVERS
from config import FILENAMEPIC, IMAGETYPES
from config import FONTS, IMAGEDEFAULTS, FONTSIZEFOOTER_MIN
from config import BASEDIR, TEMPDIRNAME
from config import PAGES, STATICDIR, MIMETYPE

import urlparse, mimetools, sys, os
from StringIO import StringIO
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


class ParsingException(Exception): 
    "Some errors can be answered specifically."
    pass 

def concatArgs(e): 
    "join the exception args to one string"
    if type(e) == type(tuple()): several=e
    else: several=e.args
    return ", ". join(["%s"%arg for arg in several])
    
class myHandler(BaseHTTPRequestHandler):
    """This class handles any incoming request from the browser. Adapted from:
       https://github.com/tanzilli/playground/blob/master/python/httpserver/example2.py
    """
    
    # error codes: See BaseHTTPServer.py
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404
    NOT_ACCEPTABLE = 406
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    
    def parseUrl(self):
        "Analyzes the user request. Detects problems."

        o = urlparse.urlparse(self.path)
        # scheme is:  /pfn/123456.png?option1=value&option2=value
        
        # platform name (e.g. "nxt" or "nhz" or "burst")        
        pfn = o.path.split("/")[1].lower()
        if pfn =="hz": pfn="nhz"
        if pfn=="": raise Exception("no platform specified")
        if pfn not in SERVERS.keys():
            raise ParsingException(self.NOT_IMPLEMENTED, 
                                   "Unknown chain. Contact me if you want your coin implemented here.")
    
        # 123456.png
        filename = o.path.split("/")[2]
        filename, suffix = filename.split(".")
        suffix=suffix.lower()
        if suffix not in IMAGETYPES: raise ParsingException(self.BAD_REQUEST, "Wrong image type.")
        
        try: BT = int(filename)
        except Exception:
            raise ParsingException(self.NOT_ACCEPTABLE, 'Your block height target is not numeric. ')
        
        # make dict from user parameters, for the image (e.g. fontsize)
        query = urlparse.parse_qs(o.query)
        query = dict([(k,v[0]) for k,v in query.items()]) # list -> single argument 
        
        # if query.get("font", "") not in FONTS:
        # print imaging.findMatchingFont( query.get("font", "") , FONTS)
        if query.has_key("font") and imaging.findMatchingFont( query["font"], FONTS)==None :
            raise ParsingException(self.NOT_ACCEPTABLE, 'Font not supported. Contact me, or change to standard font ')
        
        return pfn, BT, suffix, query
    
    def suggest(self):
        "helping the user to understand what he should rather do"
        host=mimetools.Message(StringIO(self.headers))["host"]
        return (SUGGESTION % (host))
    
    def makeImage(self, pfn, filename, suffix, BT, query):
        "ask blockchain server, calculate text, make image - and save it to disk"
        
        try: 
            _, text = chaincountdown.doTheChaChaCha(BT, pfn)
        except Exception as e:
            self.send_error(self.INTERNAL_SERVER_ERROR, 
                            'Querying the blockchain server failed (%s)' % concatArgs(e))
            return False

        try:
            o = helpers.replacedInDict(IMAGEDEFAULTS, query)
            o["fontsizefooter"] = max (FONTSIZEFOOTER_MIN, int(o["fontsize"]) / 2)
            imaging.textToImage(filename, text=text, **o)
        except Exception as e:
            self.send_error(self.BAD_REQUEST, 
                            'Creating the image did not work (%s) ' % concatArgs(e.args) + self.suggest())
            return False
        
        return True

    def do_GET(self):
        "Handler for all GET requests:"
        
        mimetype=""
        
        if self.path == "/": self.path+=INFOPAGE
         
        if self.path[1:] in PAGES:  
            self.path=filetosend=os.path.join(STATICDIR, self.path[1:]) 
            mimetype=MIMETYPE[helpers.suffix(self.path)]
                    
        # create and return image
        if mimetype=="":
            
            try:
                pfn, BT, suffix, query = self.parseUrl()
                filetosend = TEMPDIRNAME+FILENAMEPIC+"."+suffix
            except ParsingException as e:
                self.send_error(e.args[0], "%s" % e.args[1])
                return 
            except Exception as e:
                msg = 'Something went wrong (%s).' % concatArgs(e)
                self.send_error(self.NOT_FOUND, msg+self.suggest())
                return
            
            success = self.makeImage(pfn, filetosend, suffix, BT, query)
            if not success: return # an http error code is already set in self.makeImage 
            
            # success:
            mimetype='image/%s' % suffix
            
                
        # serve the file:
        try:
            self.send_response(self.OK)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            f = open(filetosend, "rb")
            self.wfile.write(f.read())
            f.close()
            return
        except IOError as e:
            self.send_error(self.NOT_FOUND,'File Not Found: %s' % self.path)

def server():
    "A web server which returns generated images, or an index page."
    try:
        #Create a web server and define the handler to manage the incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print >> sys.stderr,  'Started httpserver on port: ' , PORT_NUMBER
        
        #Wait forever for incoming http requests
        server.serve_forever()
    
    except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
    
       
if __name__ == "__main__":
    # testTextToPNG()
    server()
    
    
    
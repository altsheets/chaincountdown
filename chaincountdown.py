#!/usr/bin/python
'''
@title:    chaincountdown.py 

@summary:  HttpServer which returns time estimation to targetblock of nxt/hz. 
           Image rendered at request. Choosable heading, fontsizes & colors.

@version:  v11 "Conceptual Thunderstorm" 
                at after 2015/08/10 16:50 UTC ~ nxt-block 494158 = hz-block 419023
@since:                  2015/08/05 03:00 UTC ~ 44 hours of hard & enjoyable work

@manual:   see index.html page at http://....:8888/    
@requires: NXT / HZ / BURST / ... server for: getBlockchainStatus & getBlock

@author:   AltSheets
@license:  Giveback license v05  - http://altsheets.ddns.net/give/

@reward:       Bitcoin address exclusive to this epic.. 
               [BTC] 13whfNFT2dse7eiuNXVkuJivjxqSXHrW4j
                        Thanks a lot! Much appreciated!
                        
@donate:    or other currencies:
               NXT-CMKU-ZQYK-V6CD-9UHF4 or 
               NHZ-Q675-SGBG-LQ43-D38L6 or
               BURST-ESVR-L2WJ-NT3Y-BWM6V   Thx
@invest:    or invest into my dividends paying assets
               AAssetNXT (NXT 13634799205909171438)
               AAssetHZ  (HZ 8101260088962758269)
@freetrial: or try and buy this auto-updated portfolio overview
               Altfolio http://altfolio.ddns.net - free trial!

@related:   chaincountdown.py was created for the nxthacks2015
                 where I submitted my amazing "AssetGraphs.py"
                         http://altsheets.ddns.net/assetgraphs
'''

from config import TIMEOUT
from config import SERVER, BLOCKSPERMINUTE, GENESIS

import server

import urllib2, urllib, json, time


def queryApi(data, pfn):
    """urlencode data parameters, urlopen, result to json
       returns (True, json) or (False, error message)  
    """
    url = SERVER[pfn] + "?%s" % urllib.urlencode(data)
    
    try:
        f=urllib2.urlopen(url, timeout=TIMEOUT)
        answer = f.read()
        f.close()
        apiResult = json.loads(answer)
    except Exception as e:
        return False, e
    
    if apiResult.has_key("errorDescription"):
        return False, apiResult
    else:
        return True, apiResult

def getBlockchainStatus(pfn):
    "api getBlockchainStatus"
    data = {"requestType" : "getBlockchainStatus"}
    return queryApi(data, pfn=pfn)

def getBlock(block, pfn):
    "api getBlock(block)"
    data = {"requestType" : "getBlock", "block": block}
    return queryApi(data, pfn=pfn)
    
def coinTimeToHumanTime(coinTime, pfn):
    "returns date and time when given coin timestamp and platformname" 
    epoch=GENESIS[pfn] + coinTime
    humanReadable=time.strftime("%d %b %Y %H:%M:%S UTC", time.gmtime(int(epoch)))
    return humanReadable  

def ifDictThenFormatting(err):
    "if the error is in dict format, show one item per line."
    res=err.copy()
    if type(res)==type({}):
        res = "\n".join(["%s:%s"%(k,v) for k,v in res.items()])
    return res
                     
def abortTextIfNecessary(success, apiResult, pfn):
    "Check the results. If not good, return reasons as text."
    if not success: 
        string = "%s error that should not happen,\nbetter contact your higher power:\n%s"
        return success, string % (pfn, ifDictThenFormatting(apiResult))
     
    # TODO: Is the server still syncing?
    if apiResult["lastBlockchainFeederHeight"] - apiResult["numberOfBlocks"] > -1:
        showText =  "Nope - please wait:\nBlockchain still syncing,\n"
        showText += "Current block = %d" % apiResult['numberOfBlocks']
         
        succ, block=getBlock(apiResult["lastBlock"], pfn)
        if succ:
            blockDateTime = coinTimeToHumanTime ( block["timestamp"], pfn ) 
            showText += "\n(%s)." % blockDateTime
        return False, showText  
    
    return True, apiResult

def calculateCountdown(apiResult, blockHeightTarget, pfn):
    "generate the answers, returns success & lots of numbers"
    heightNow = apiResult["numberOfBlocks"]
    blocksLeft = blockHeightTarget - heightNow
    if blocksLeft < 0: 
        return False, heightNow, blocksLeft, 0, ""
    
    minutesLeft= blocksLeft / BLOCKSPERMINUTE[pfn]
    coinTimeThen = apiResult["time"] + 60 * minutesLeft
    datetimeThen = coinTimeToHumanTime(coinTimeThen, pfn)
    
    return True, heightNow, blocksLeft, minutesLeft, datetimeThen

def understandableDuration(Minutes):
    "from minutes, generate hours, or weeks, or ... - depending on what makes sense"
    
    limits = ((1,           "minutes",  0),
              (60,          "hours",    2),
              (60*24,       "days",     1),
              (60*24*7,     "weeks",    1),
              (60*24*30,    "months",   1),
              (60*24*365,   "years",    1))
        
    divisor, name, digits = [(T, N, D)
                             for T, N, D in limits
                             if Minutes > 2*T] [-1] # take highest

    duration = float(Minutes)/divisor
    duration = ("%." + "%d"%digits + "f") % duration
    
    return "~%s %s" % (duration, name)


def pprintCountdown(inTheFuture, BN, BL, Minutes, DT):
    "Generates nice text from the above numbers"
    if not inTheFuture:
        showText = "Sorry: Already at block %d, \nyou are %d blocks too late." % (BN, -BL)  
        return False, showText
    
    showText =  "%d blocks left to target.\nFrom current block %d\n" % (BL, BN)
    duration = understandableDuration(Minutes) 
    showText += "%s. My best guess:\n%s" % (duration, DT)
    
    return True, showText


def doTheChaChaCha(blockHeightTarget, pfn):
    """this is where the magic happens:
       get chain data, check results, calculate, and make a nice string from it."""
    
    success, apiResult = getBlockchainStatus(pfn)
    
    success, showText = abortTextIfNecessary (success, apiResult, pfn)
    if not success: 
        return success, showText
#        
    return pprintCountdown ( *calculateCountdown(apiResult, blockHeightTarget, pfn) )
    
def test_doTheChaChaCha():
    "tests to check everything, incl the minutes conversion."
    for BT in (-1, 0, 490490, 495997, 500490, 510490, 600490, 900490, 1900490, 41900490):
        success, showText = doTheChaChaCha(BT, "nxt")
        print success
        print showText
        print 


if __name__ == "__main__":
    # test_doTheChaChaCha()
    server.server()
    
    
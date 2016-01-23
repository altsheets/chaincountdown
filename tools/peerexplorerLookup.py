#!/usr/bin/python
'''
@title:    peerexplorerLookup.py

@summary:  Queries peerexplorer for nxt nodes with open API, 
           then looks up the domainnames for all results.
           
           Final table is:
           * sorted by domain, in cool ordering: from TLD to the front
           * then IP addresses, in increasing order

@related:  Made for chaincountdown.py when jnxt.org was down.
           https://github.com/altsheets/chaincountdown            

@version:  v0.14
@since:    2016/01/23

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
               
@science:   or support this great new project - by trying & buying
               a totally new innovative GUI for blockchain data:
               
               AssetGraphs-v2
               http://altsheets.ddns.net/assetgraphs/v2/products/
'''

import urllib2, urlparse, json, socket, threading, timeit


def queryPeerexplorer(server="http://www.peerexplorer.com", command="/api_openapi"):
    """get all IP addresses"""
    
    url=urlparse.urljoin(server, command)
    # print url
    try:
        f=urllib2.urlopen(url)
        answer = f.read()
        f.close()
        apiResult = json.loads(answer)
    except Exception as e:
        return False, e
    
    if apiResult.has_key("errorDescription"):
        return False, apiResult
    else:
        return True, apiResult
      
def lookupIPs_blocking(IPs, breakEarly=False):
  """
  Given a list of IPs ... this returns domain names.
  Slow. Too slow. See below.
  """
  
  IPdomains=[]
  if breakEarly: maxNum=5
  for IP in IPs:
    try:
      domain=socket.gethostbyaddr(IP)[0]
    except:
      domain=""
    print "%15s: %s" % (IP, domain)
    IPdomains.append((domain, IP))
    if breakEarly: 
      maxNum-=1
      if maxNum<=0: break
    
  return IPdomains


def lookupIPs(IPs, breakEarly=False):
  """
  Given a list of IPs ... this returns domain names.
  Threaded version, very fast.
  """
  
  started=timeit.default_timer()
  
  def IPthread(IP, IPdomains, printLock):
    "gethostbyaddr, then print (with printLock = in orderly fashion)"
    try:
      domain=socket.gethostbyaddr(IP)[0]
    except:
      domain=""
    printLock.acquire()
    print "(%.4fs) %16s: %s" % (timeit.default_timer()-started, IP, domain)
    printLock.release()
    IPdomains.append((domain, IP))

  IPdomains=[]
  threads, printLock=[], threading.Lock()
  for IP in IPs:
    t=threading.Thread(target=IPthread, args=(IP, IPdomains, printLock))
    threads.append(t)
  for t in threads: t.start()
  for t in threads: t.join()
    
  return IPdomains

def sortBackToFront(myList):
  "Sorts domain names in a cool way: backwards from TLD to the front."
  myList2=[]
  for elements in sorted( [x.strip().split('.')[::-1] for x in myList] ):
    myList2.append(".".join([elem for elem in reversed(elements)]))
  return myList2
     
def sortIPaddresses(ips):
  "Sorts IP address in increasing order."
  for i in range(len(ips)):
    ips[i] = "%3s.%3s.%3s.%3s" % tuple(ips[i].split("."))
  ips.sort()
  for i in range(len(ips)):
    ips[i] = ips[i].replace(" ", "")

def makeNXTnodesTable():
  """Put everything together: Query peerexplorer, query DNS, sort, print"""
  
  command="/api_openapi"
  IPs = queryPeerexplorer(command=command)
  
  if not IPs[0]:
    print "peerexplorer didn't want to play with me: ", IPs[1]
    return False
  
  IPs=IPs[1]["peers"]
  print "Got %d node IPs from Peerexplorer, for command %s" % (len(IPs), command)
  print "Now looking up domain names, patience please ..."
  NXTnodes=lookupIPs(IPs)
  
  domains=sortBackToFront(zip(*NXTnodes)[0])
  domains = filter(lambda x:x!="", domains)
  print "Ready. For %d of the %d I got domain names." % (len(domains), len(NXTnodes))
  
  formattingString = "%15s: %"+"%d"%(max([len(d) for d in domains])+2)+"s"
  print "\nNow everything again, sorted. Domain names first, then IP-address-only:"
  domainsDict=dict(NXTnodes)
  for d in domains:
    print formattingString % (domainsDict[d], d)
    
  noDomains=[IP for domain, IP in NXTnodes if domain == ""]
  sortIPaddresses(noDomains)
  for IP in noDomains:
    print "%15s" % IP
  
  return True
      

if __name__=="__main__":
  makeNXTnodesTable()
  
  
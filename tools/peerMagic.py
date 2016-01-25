#!/usr/bin/python
'''
@title:    peerexpMagic.py

@summary:  NXT: Queries peerexplorer for nxt nodes with open API.
           HZ: Queries localhost for 'getPeers', then starts crawling them all!
           
           BOTH: Looks up the domainnames for all results,
                 and does fancy sorting:
           
           Final table is:
           * sorted by domain, in cool ordering: from TLD to the front
           * then IP addresses, in increasing order

@related:  Made for chaincountdown.py when jnxt.org was down.
           https://github.com/altsheets/chaincountdown            

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

VERSION =      "v0.18"

# wow, I am becoming more and more pythonic (-: 
import urllib, urllib2, urlparse, json, socket, threading, timeit, Queue, time, collections, pickle, datetime, os

try: import requests
except: print "pip install requests"

TIMEOUT=3

# for HZ crawler
NUM_WORKERS=150  # do not put too high. For unknown reasons, it then doesn't visit the whole network. Strange bug.
PRINT_EVERY=100 

HZ_PEER_PORT=7774
HZ_API_PORT=7776
HZ_SUFFIX="nhz"

HZ_START_NODE="woll-e.net" # api.nhzcrypto.org

# for 7774 peerserver:
HEADERS = {'content-type': 'application/x-www-form-urlencoded'} 
DATA = {"protocol":1, "application":"peerMagic", "version":VERSION}


def queryAPI(server="http://www.peerexplorer.com", command="/api_openapi", timeout=TIMEOUT, data=None):
    """
    Send command to server, examine the result. 
    Returns (bool success, json answer)"""
    
    url=urlparse.urljoin(server, command) if command!="" else server
    try:
        f=urllib2.urlopen(url, timeout=timeout, data=data)  # data=None --> GET, otherwise POST
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


def lookupIPs(IPs, breakEarly=False, printSteps=True):
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
    IPdomains.append((domain, IP))
    if printLock!=None:
      printLock.acquire()
      print "(%.4fs) %16s: %s" % (timeit.default_timer()-started, IP, domain)
      printLock.release()

  IPdomains, threads = [], []
  printLock = threading.Lock() if printSteps else None 
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
    try:
      ips[i] = "%3s.%3s.%3s.%3s" % tuple(ips[i].split("."))
    except:
      print "probably not an ip address:", ips[i] 
  ips.sort()
  for i in range(len(ips)):
    ips[i] = ips[i].replace(" ", "")


def nodesTableWithDomainNames(IPs, printSteps=True):
  """Put everything together: Query DNS, sort, print"""
  
  print "Looking up domain names, patience please ..."
  NXTnodes=lookupIPs(IPs, printSteps=printSteps)
  
  domains=sortBackToFront(zip(*NXTnodes)[0])
  domains = filter(lambda x:x!="", domains)
  print "Ready. For %d of the %d I got domain names." % (len(domains), len(NXTnodes))
  
  formattingString = "%15s: %"+"%d"%(max([len(d) for d in domains])+2)+"s"
  print "\nEverything again, now sorted. Domain names first, then IP-address-only:"
  domainsDict=dict(NXTnodes)
  for d in domains:
    print formattingString % (domainsDict[d], d)
    
  noDomains=[IP for domain, IP in NXTnodes if domain == ""]
  sortIPaddresses(noDomains)
  for IP in noDomains:
    print "%15s" % IP
  

def nodesTableWithDomainNames_NXT():
  """Query peerexplorer, then IP-->DNS table"""
  
  command="/api_openapi"
  IPs = queryAPI(command=command)
  
  if not IPs[0]:
    print "peerexplorer didn't want to play with me: ", IPs[1]
    return False
  
  IPs=IPs[1]["peers"]
  print "Got %d node IPs from Peerexplorer, for command %s" % (len(IPs), command)
  
  nodesTableWithDomainNames(IPs)



#####################################################################
#                           HZ crawler
#####################################################################


def requestPOST(url, requestType="getInfo", timeout=TIMEOUT, headers=HEADERS):
  """POST request to peer node, incl. correct headers.
  
  MaWo's script was the example, how to do it with 'curl':
  https://bitcointalk.org/index.php?topic=823785.msg13656332#msg13656332
  
  Check out my testing script  'test7774.py' where I found the headers trick.
  """
  
  data=DATA
  data["requestType"] = requestType
  data=json.dumps(data)
  try:
    r=requests.post(url, data=data, headers=headers, timeout=timeout)
  except Exception as e:
    return False, "(%s) %s" % (type(e), e)
  
  if r.status_code == requests.codes.ok:
    return True, r.json()
  else:
    return False, r.text
  

def makeUrl_perhapsAddPort(address):
  """
  Prepend http://
  If the address already has a :port then just return it. 
  Otherwise :7776
  """
  if ":" not in address:
    address+=":%s"%HZ_PEER_PORT
  address="http://"+address
  return address


def getInfo(node):
  """ask peernode for its infos (e.g. hallmark, version, etc.)"""
  success, info = requestPOST(url=makeUrl_perhapsAddPort(node), requestType="getInfo")
  return success, info
  

def getPeers(node):
  """ask peernode for its peers"""
  success, peers = requestPOST(url=makeUrl_perhapsAddPort(node), requestType="getPeers")
  return success, peers

    
def getInfo_then_GetPeers(node):
  """The protocol seems to insist to first ask for getInfo."""
  
  success, info = requestPOST(url=makeUrl_perhapsAddPort(node), requestType="getInfo")
  if not success: return success, info
  time.sleep(0.2) # to avoid "Peer request received before 'getInfo' request"
  
  success, peers = requestPOST(url=makeUrl_perhapsAddPort(node), requestType="getPeers")
  return success, peers  
   

def test7774(thenExit=False):
  """test post, getPeers"""
  print requestPOST( url="http://%s:%s/%s"%(node, HZ_PEER_PORT, HZ_SUFFIX) )
  success, peers = getPeers(HZ_START_NODE)
  if success:
    print "\n".join([p for p in peers["peers"]])
  if thenExit: exit()
  
def peerServerON(node):
  """asks 'getInfo' and checks results for key 'version'
  """
  success, info = requestPOST(url=makeUrl_perhapsAddPort(node))
  return success and info.has_key('version')
    
def test_CheckPeerServer():
  """test the above"""
  for IP in ("1.2.3.4", "173.232.15.176", HZ_START_NODE, "localhost"):
    print IP, peerServerON(IP)


def printAnswers(IPs):
  """to study the peer node answers"""
  for IP in IPs:
    nodePeerServer="http://%s:%s" % (IP, HZ_PEER_PORT)
    print queryAPI(server=nodePeerServer, command="", data="", timeout=3)
    

def checkOpenAPI_worker(apQueue, apDone, apON, openAPI, apInfo, network, printLock, thresholds, started):
  """Multi-threaded. Works through a queue: 
     If 'getPeers' is successful, then append AP (address+port) to apON list. 
     also add yet unchecked peers to the queue.
     if :API_PORT getTime successful, then append IP to openAPI.
  """
  
  while True:
    
    AP=apQueue.get() # dequeue one (address+port)
    if AP in apDone: 
      apQueue.task_done() # been here before, in another thread
      
    else:
      apDone.append(AP)

      # question 1: open API server?
      IP=AP.split(":")[0]
      apiNodeAnswers, _ =queryAPI(server="http://%s:%s" % (IP, HZ_API_PORT),
                                  command="/nhz?requestType=getTime")
      if apiNodeAnswers: openAPI.append(IP) # == this IP has an open API
        
      # question 2: is this a peer node server?
      peerNodeAnswers, infos = getInfo(AP)
      if peerNodeAnswers: 
        try:
          apInfo[AP]=[infos['platform'], infos['version']]
        except Exception as e:
          print "(%s) %s" % (type(e), e), infos 
        apON.append(AP)

        # only if it answers, try to get peers:        
        time.sleep(0.2)
        peerNodeGotPeers, hisPeers = getPeers(AP)
        
        if peerNodeGotPeers:
          newCount=0   
          try:
            hisPeers=hisPeers["peers"]
          except:
            print "STRANGE, this should not happen:", hisPeers
          else:
            for p in hisPeers:
              network[IP]=hisPeers
              if p not in apDone:
                apQueue.put(p)     # enqueue the new peers
                newCount+=1

      # from here on, it's all about pretty printing:
      checked, mt = len(apDone), max(thresholds)

      if peerNodeAnswers or apiNodeAnswers or checked>mt:
        peerInfo=""
        if checked > mt: thresholds.append( mt + PRINT_EVERY)
          
        if peerNodeAnswers and peerNodeGotPeers:
          peerInfo = "peers=%3d of which unchecked=%3d" % (len(hisPeers), newCount)
        
        nN, qs, oa = len(apON), apQueue.qsize(), len(openAPI)
        timeSpent = timeit.default_timer()-started

        infoline=("(%6.3fs) nodes=%3d openAPI=%3d checked=%4d queue=%4d |"
                  "%16s: node=%5s openAPI=%5s | %s") 
        infoline = infoline % (timeSpent, nN, oa, checked,        qs,
                   IP, peerNodeAnswers, apiNodeAnswers, peerInfo)        
        
        printLock.acquire()
        print infoline
        printLock.release()
        
      apQueue.task_done()


def crawlHZnodes(node=HZ_START_NODE):
  """
  Checks hundreds of IPs for open API.
  starting point is localhost --> getPeers
  """
  
  url="http://%s:%s" % (HZ_START_NODE, HZ_API_PORT)
  
  success, peers=queryAPI(server=url, command="/nhz?requestType=getPeers")
  if not success:
    print "%s didn't want to play with me: %s" % (node, peers); return False
  
  initialPeers=peers["peers"]
  print ("Got %d peers from %s, now checking which ones have open API, "
         "and enqueue'ing their peers:" % (len(initialPeers), node))
  print ("Patience please, this can take minutes. Printing each openAPI IP, "
         "plus every approx. %d checked IPs:" % PRINT_EVERY)

  peersToCheck,printLock=Queue.Queue(), threading.Lock()  
  started=timeit.default_timer()
  apON, openAPI, apDone, apInfo, network=[], [], [], {}, {}
  thresholds=[PRINT_EVERY] # using list because it is thread-safe

  for i in range(NUM_WORKERS):
    args=(peersToCheck, apDone, apON, openAPI, apInfo, network, printLock, thresholds, started)
    t=threading.Thread(target=checkOpenAPI_worker, args=args)
    t.daemon=True
    t.start()

  for item in initialPeers:
    peersToCheck.put(item)
    
  peersToCheck.join() # waits until the queue is finished
 
  duration=timeit.default_timer()-started
  n, qs, oa = len(apON), peersToCheck.qsize(), len(openAPI)
  checked = len(apDone)
  
  print "(%6.3fs) nodes=%3d openAPI=%3d checked=%4d queue=%4d " % (duration, n, oa, checked, qs)
  
  print "\nReady. Found %d nodes, and %d with open API." % (n, oa)
  
  return apON, openAPI, apInfo, network
    

def makeIP(ap):
  """
  If already IP, then just return it. 
  Otherwise DNS lookup, to get IP.
  ap=address+port or IP
  """
  ap=ap.split(":")
  
  if len(ap)==1: addr,p=ap[0],""
  else:          addr,p=ap
  
  try:
    socket.inet_aton(addr)
    ip=addr
  except socket.error:
    try:    
      ip = socket.gethostbyname(addr)
    except Exception as e:
      print "gethostbyname: (%s) %s" % (type(e), e) 
      ip=addr # fallback back to input

  # attach the port again, if it had one
  if p!="": ip+=":"+p
  return ip

def test_makeIP():
  "test cases for the above"
  for ap in ["www.google.de", "www.google.de:80", "23.245.7.15", "23.245.7.15:99"]:
    print "%20s = %20s" % (ap, makeIP(ap))
    
def makeAllIP(apList):
  "DNS lookup of a whole list of APs"
  return [makeIP(ap) for ap in apList]


def infoStatistics(apInfo):
  """Overview of 'versions' and 'platforms'"""
  
  # print apInfo.values()
  pf, ver = zip(*(apInfo.values()))
  
  print "Names:", 
  names=collections.Counter(pf).items()
  names.sort(key=lambda x:x[1], reverse=True)
  print ", ".join(["%s (%s)"%(k, v) for k,v in names])

  print "Versions:"
  versions = collections.Counter(ver).items()
  versions.sort(key=lambda x:x[1], reverse=True)
  print "\n".join(["%3d  %s"%(v,k) for k,v in versions])
  print

  
def timestampForFilename():
    "coarse to fine grained timestamp"
    return datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def nodesTableWithDomainNames_HZ():
  """
  Query localhost for peers, then crawl, then IP-->DNS table.
  
  Network and node-information is pickled to file.
  Filename is returned.
  """
  
  result = crawlHZnodes() # crawler
  
  if not result:
    print "You probably have no HZ node running on localhost."
    print "Start your HZ node, or change HZ_STARTING_NODE_URL to a node with openAPI."
    return False
    
  nodeON_APs, openAPI_IPs, apInfo, network = result
  
  try:
    fn="HZ_%s.pickle" % timestampForFilename()
    with open(fn, 'w') as pkl_file:
      pickle.dump((network, openAPI_IPs, apInfo), pkl_file)
    print "Network written to: %s\n" %fn
  except:
    pass 

  infoStatistics(apInfo)
  
  print "Convert all into IP addresses."
  openAPI_IPs =makeAllIP(openAPI_IPs)
  nodeON_APs  =makeAllIP( nodeON_APs)
  
  print "Drop port numbers."
  nodeON_IPs = [AP.split(":")[0] for AP in nodeON_APs] 
  
  for purpose, ipList in (("peerservers", nodeON_IPs),("apiservers", openAPI_IPs)):
    sortIPaddresses(ipList)
    print "These %d IPs are %s:" % (len(ipList), purpose)
    print ipList
  
  print "These peers are using a non-standard port:"
  nodeON_diffPort = list ( set(nodeON_APs) - set(nodeON_IPs))
  print nodeON_diffPort 
  
  nonPeerButApiNodes = list ( set(openAPI_IPs) - set(nodeON_IPs) )
  print "open API but not peer nodes ('d be a bit STRANGE actually): "
  print nonPeerButApiNodes

  nonOpenApiNodes = list ( set(nodeON_IPs) - set(openAPI_IPs) )
  print "\nNodes but not open API: ", len(nonOpenApiNodes)
  nodesTableWithDomainNames(nonOpenApiNodes, printSteps=False)
  print "These are all peer IPs with non-open API!"
  
  print "\nOpen API:", len(openAPI_IPs)
  nodesTableWithDomainNames(openAPI_IPs, printSteps=False)
  print "These are all IPs with open API!"
  
  return fn


def makeIPdropPort(ap):
  """returns IP of (addr+port)"""
  ap=makeIP(ap)
  ip=ap.split(":")[0] # DNS-->IP, and drop port
  return ip 

  


def saveNetworkFiles(fn="HZ_20160125-105105.pickle"):
  """
  Long code, sorry. But not spaghetti!
  
  It is simply ... 
  sequentially transforming everything ... 
  into network files - to be read with Pajek.
  """ 
  print 
  
  try:
    with open(fn, 'r') as pkl_file:
      network, openAPI_IPs, apInfo = pickle.load(pkl_file)
    print "Network loaded from: %s" %fn
  except:
    print "Load failed. Exit."
    return
  
  print dict([(name, len(eval(name))) for name in ("network", "openAPI_IPs", "apInfo")])

  # transform all (addr+port) to IP address, merge duplicates on the way  
  ipNetwork={}
  for n, peers in network.items():
    nodeIP=makeIPdropPort(n)
    peerIPs=map(makeIPdropPort, peers)
    peerIPs=list(set(peerIPs)) # unique only
    if len(peerIPs)!=len(peers): print "Neighbours of %s just got less when DNS lookup" % n
    
    if ipNetwork.has_key(nodeIP):
      print "%s was already added, probably DNS as well as IP entry in list. MERGED!" % nodeIP
      #print "before:", ipNetwork[nodeIP]
      #print "   new:", peerIPs
      ipNetwork[nodeIP]=list(set (ipNetwork[nodeIP] + peerIPs))
      #print "merged:", ipNetwork[nodeIP] 
       
    ipNetwork[nodeIP]=peerIPs
    
  print "ipNetwork: ", len(ipNetwork)

  print "sort IP addresses increasing:"
  IPsSorted=ipNetwork.keys()
  sortIPaddresses(IPsSorted)
  print "IPsSorted: ",  len(IPsSorted)  

  pajekFilename="%s_network-%s" % (os.path.splitext(fn)[0], timestampForFilename())
  
    
  with open(pajekFilename+".net", "w") as f:
    f.write("*Vertices %s\n" % len(ipNetwork))
    
    IP2index, index2IP={}, {}
    for i, n in enumerate(IPsSorted):
      f.write('%d "%s"\n'% (i+1, n))
      IP2index[n] = i+1
      index2IP[i+1] = n
      
    f.write("*Edges\n")  
    for n, peers in ipNetwork.items():
      dropped=0
      for p in peers:
        if p in IP2index.keys(): # only talk about nodes which are answering, drop all others!
          f.write("%d %d 1\n" % (IP2index[n], IP2index[p]))
        else:
          dropped+=1
      #if dropped: print "dropped %d nodes, kept %d nodes" % (dropped, len(peers)-dropped) 
      
      
  print "Network written to '%s.net'\n" % pajekFilename
  print dict([(name, len(eval(name))) for name in ("IP2index", "index2IP")])
  
  ipInfo={}
  for ap, info in apInfo.items():
    ip=makeIPdropPort(ap)
    if ipInfo.has_key(ip):
      print "collision, please check that equal:", 
      print ipInfo[ip], info
    ipInfo[ip]=info
    
  print dict([(name, len(eval(name))) for name in ("apInfo", "ipInfo")])
  
  print "Sorting and saving version numbers...\n"
  versions=zip(*(ipInfo.values()))[1]
  # print versions
  versions=list(set(versions)) # make unique
  versions.sort()
  
  # print versions
  versionDict=dict([(v,i) for i, v in enumerate(versions)])
  # print versionDict 
  
  versionDictKeys=sorted(versionDict.keys())
  with open(pajekFilename+"_versions_names.txt", "w") as f:
    f.write("\n".join(["%2d %s"%(versionDict[k],k) for k in versionDictKeys])+"\n")
  # todo: Could do statistics, too.
  print "Versions names written to '%s_versions_names.txt'" % pajekFilename
    
  with open(pajekFilename+"_versions.clu", "w") as f:
    f.write("*Vertices %s\n" % len(IPsSorted))
    for IP in IPsSorted:
      f.write("%s\n" % versionDict[ ipInfo[IP][1] ] )
    
  print "Cluster of versions written to '%s.clu'" % pajekFilename
  
  
def countInFile(fn="HZ_20160125-105105_network-20160125-112807_versions.clu"):
  "Just to check which dataset I had actually used... *g*"
  with open(fn,"r") as f:
    lines=f.readlines()
  lines=lines[1:]
  print collections.Counter(lines)

if __name__=="__main__":
  # test7774(thenExit=True)
  # test_CheckPeerServer(); exit()
  # test_makeIP(); exit()
  
  print ("-" * 50 + "\n") * 2 + "\nNXT:\n\n" + ("-" * 50 + "\n") * 2
  nodesTableWithDomainNames_NXT()
  
  print ("-" * 50 + "\n") * 2 + "\nHZ :\n\n" + ("-" * 50 + "\n") * 2
  fn=nodesTableWithDomainNames_HZ()
    
  saveNetworkFiles(fn)
  #
  # countInFile()
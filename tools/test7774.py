
"""
Tying to find out how to contact the peerServer port 7774 on HZ

The example from MaWo's script https://bitcointalk.org/index.php?topic=823785.msg13656332#msg13656332 is: 
curl -4 -m5 --data '{"platform":"TEST","protocol":1,"application":"TEST Bot","requestType":"getInfo","version":"v0.1"}' "http://woll-e.net:7774/nhz"


At first, I just could not get it working, however I tried. Always the same answer:

http://woll-e.net:7774/nhz
test 1:
{"cause":"Unexpected character (r) at position 0.","error":"Your peer is blacklisted"}
test 2:
{"cause":"Unexpected character (r) at position 0.","error":"Your peer is blacklisted"}


Then I had the idea to send both requests (curl, python.requests) to requestb.in, to compare them.
And that helped! 

The 'header' has to be set to 'application/x-www-form-urlencoded', 
for the 7774 peerserver to accept the data. *sigh*, I made it ... 

"""
 
import urllib2, urllib, urlparse

try:  import requests
except:  print "pip install requests"

PORT=7774

NODE="eu6.woll-e.net"
# NODE="woll-e.net"

URL="http://%s:%s/nhz" % (NODE, PORT)


def test1():
  print "test 1:"
  data='{"platform":"TEST","protocol":1,"application":"TEST Bot","requestType":"getInfo","version":"v0.1"}'
  s=urllib2.urlopen(url=URL, data=data)
  answer=s.read()
  s.close()
  print answer
  
def test2():
  print "test 2:"
  try:
    import requests
  except:
    print "pip install requests"
    return False
  
  data={"platform":"TEST","protocol":1,"application":"TEST Bot","requestType":"getInfo","version":"v0.1"}
  r=requests.post(URL, data=data)
  print r.text
  
import json
  
def test3():
  """
  Trying to find out what is wrong 
  by comparing curl with python.requests.post
  in requestb.in
  """
  
  
  print """
  test against this manual curl:
  curl -d '{"protocol":1,"requestType":"getInfo"}' "http://requestb.in/11c8di01"  
  """
  
  url="http://requestb.in/11c8di01" # http://requestb.in/11c8di01?inspect
  
  data={"protocol":1,"requestType":"getInfo"}
  data=json.dumps(data)

  # THIS WAS THE THING TO DO *sigh*:  
  headers = {'content-type': 'application/x-www-form-urlencoded'}
  
  r=requests.post(url, data=data, headers=headers)
  print r.status_code, r.text
  print "now lookup %s_inspect to see the results.\n\n" % url
  
def test4():
  nodes=[u'5.9.149.197', u'5.196.143.14', u'23.95.44.142', u'23.245.7.15', u'31.24.29.221', u'37.120.160.148', u'37.120.173.114', u'40.115.9.5', u'40.115.9.55', u'45.55.81.226', u'45.55.157.54', u'52.24.16.77', u'52.24.85.12', u'52.24.187.95', u'52.26.95.4']
  
  data={"protocol":1,"requestType":"getInfo"}
  data=json.dumps(data)
  headers = {'content-type': 'application/x-www-form-urlencoded'}
  
  for n in nodes:
    url="http://%s:%s/nhz" % (n, PORT)
    print "%15s" % n,
    try:
      r=requests.post(url, data=data, headers=headers, timeout=1)
    except:
      print
      continue
    
    print r.status_code, 
    j = r.json()
    for k in ("version", "announcedAddress", "platform"):
      print "%15s" % j.get(k, ""),
    print
    

if __name__=="__main__":
  print URL
  test1()
  test2()
  test3()
  test4()
  
  
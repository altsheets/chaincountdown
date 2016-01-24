
"""
attempt to contact the peerServer port 7774 on HZ

curl -4 -m5 --data '{"platform":"TEST","protocol":1,"application":"TEST Bot","requestType":"getInfo","version":"v0.1"}' "http://woll-e.net:7774/nhz"

is the example.

But I just cannot get it working, however I try. Always the same answer:

http://woll-e.net:7774/nhz
test 1:
{"cause":"Unexpected character (r) at position 0.","error":"Your peer is blacklisted"}
test 2:
{"cause":"Unexpected character (r) at position 0.","error":"Your peer is blacklisted"}

Please help. Thanks.

"""
 
import urllib2

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
  
  
if __name__=="__main__":
  print URL
  test1()
  test2()
  
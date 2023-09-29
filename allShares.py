import urllib2
import os

request = urllib2.Request('http://quote.eastmoney.com/stocklist.html')
response = urllib2.urlopen(request)
try:
    content = response.read()
except Exception as e:
    print "get all shares fail"
    print e
    exit()
f = open('/Users/alchemystar/shares/data/stocklisthtml.txt', 'w')
shares = open('/Users/alchemystar/shares/data/metadata/shares.txt', 'w')
content = content.decode("gbk").encode("utf-8")
f.write(content)
cmd = "grep 'a target=\"_blank\" href=' /Users/alchemystar/shares/data/stocklisthtml.txt |\
 awk -F 'html\">' '{print $2}' | awk -F '</a>' '{print $1}' "
output = os.popen(cmd).read()
output = output.split("\n")
print len(output)
shares.write("name,code")
for item in output:
    if item.strip() != '':
        item = item.split("(")
        row = (item[0] + "," + item[1].split(")")[0]+"\n").decode("utf-8").encode("gbk")
        shares.write(row)

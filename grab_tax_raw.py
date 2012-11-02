import urllib2
from BeautifulSoup import BeautifulSoup

# Our url
address ='https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20121&m=0160001'

# Read in the response to a HTTP request
response = urllib2.urlopen(address).read()

# BeautifulSoup is a very nice library for parsing HTML and walking
# through an HTML document hierarchy
soup = BeautifulSoup(response)

## We want to grab all the td elements like the one below
##
## <TD CLASS="data" ALIGN="right" VALIGN="top" NOWRAP>
## <CENTER><B>ST</B></CENTER>b
## 18,887,148.64<BR>
## 16,185,354.22<BR>
## 62,117,172.52<BR>
## 17,352,693.36<BR>
## 14,166,524.92<BR>
## 7,891,375.77<BR>
## 32,494,883.62<BR>
## 29,752,400.16<BR>
## 20,989,444.21<BR>
## 4,220,617.81<BR>
## 224,057,615.23<BR><BR></TD>
taxes = soup.fetch('td', {'align':'right', 'valign':'top'})

for tax in taxes :
  print tax
  print



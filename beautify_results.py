import urllib2
from BeautifulSoup import BeautifulSoup

# Our url
address ='https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20121&m=0160001'

# Read in the response to a HTTP request
response = urllib2.urlopen(address).read()

soup = BeautifulSoup(response)

print soup.prettify()

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
## <CENTER><B>ST</B></CENTER>
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

tax_list = []
for tax in taxes :
  # The element corresponding to the name of the tax is the second
  # child of the TD element (Python indexes start with 0) It's not the
  # first element because BeautifulSoup considers newlines, '\n', and
  # there is a newline before <CENTER>
  #
  # <CENTER><B>ST</B></CENTER>
  #
  # in BeautifulSoup the .text method returns all the text enclosed by
  # start and closing tags
  tax_name = tax.contents[1].text

  # We turn the BeautifulSoup element into a simple string that looks
  # like
  # <td class="data" align="right" valign="top" nowrap="NOWRAP">
  # <center><b>RTA</b></center>
  # <br />
  # <br />
  # <br />
  # <br />
  # <br />
  # <br />
  # <br />
  # 1,587.98<br />
  # 895.65<br />
  # 118.50<br />
  # 4,151.20<br /><br /></td>
  tax_rows = str(tax)

  # remove the non-informative strings from the tax_rows string
  tax_rows = tax_rows.replace('<br />', '')
  tax_rows = tax_rows.replace('</td>', '')
  tax_rows = tax_rows.replace(',', '')

  #print tax_rows

  # split the string into a list at the newlines
  tax_rows = tax_rows.split('\n')

  # the first two elements correspond to the first td tag
  # and the tax name element which we already got
  amounts = tax_rows[2:]

  tax_list.append((tax_name, amounts))

print tax_list



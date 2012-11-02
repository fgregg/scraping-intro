import urllib2
from BeautifulSoup import BeautifulSoup

# Our url
address ='https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20121&m=0160001'

# Read in the response to a HTTP request
response = urllib2.urlopen(address).read()

# BeautifulSoup is a very nice library for parsing HTML and walking
# through an HTML document hierarchy
soup = BeautifulSoup(response)

tables = soup.fetch('table', {'cellspacing':'3'})
# the first table is the form

tax_info = []
for table in tables[1:] :
    taxes = table.fetch('td', {'align':'right', 'valign':'top'})
    tax_list = []
    for tax in taxes :
        tax_name = tax.contents[1].text

        tax_rows = str(tax)
        tax_rows = tax_rows.replace('<br />', '')
        tax_rows = tax_rows.replace('</td>', '')
        tax_rows = tax_rows.replace(',', '')
        tax_rows = tax_rows.split('\n')

        amounts = tax_rows[2:]

        tax_list.append((tax_name, amounts))


    heading = table.fetch('table', {'width':'600'})[0]

    headers = []
    for header in heading.fetch('td') :
        header_text = header.text
        if 'Number of Taxpayers' in header_text :
            num_tax_payers = header_text.split(':')
            num_tax_payers = num_tax_payers[1]
            num_tax_payers = num_tax_payers.strip()
            num_tax_payers = num_tax_payers.replace(',','')

            headers.append(num_tax_payers)
        else:
            headers.append(header_text)


    tax_info.append((headers, tax_list))


for county in tax_info :
  print county[0]
  for tax in county[1] :
    print '\t', tax
  

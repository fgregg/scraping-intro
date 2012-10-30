import csv
import urllib2
from BeautifulSoup import BeautifulSoup

column_names = ['municipality',
                'county',
                'number_taxpayers',
                'tax_type',
                'year',
                'quarter',
                'general_merchandise',
                'food',
                'drinking_and_eating_places',
                'apparel',
                'furniture_and_hh_and_radio',
                'lumber_bldg_hardware',
                'automotive_and_filling_stations',
                'drugs_and_misc_retail',
                'agriculture_and_all_others',
                'manufacturers',
                'total']

with open('taxes.csv', 'w') as csvfile:
  csvwriter = csv.writer(csvfile)
  csvwriter.writerow(column_names)





for year in range(1999,2013) :
  for quarter in range(1,5) :
    url = 'https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=%s%s&m=0160001' % (year, quarter)

    response = urllib2.urlopen(url)

    soup = BeautifulSoup(response.read())

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

    print url
    print tax_info



    with open('taxes.csv', 'a') as csvfile:
        csvwriter = csv.writer(csvfile)

        for tax_body in tax_info :
            muni, county, num_taxpayers = tax_body[0]
            for taxes in tax_body[1] :
                tax_row = [muni, county, num_taxpayers, taxes[0], year, quarter]
                tax_row.extend(taxes[1])
                print tax_row
                csvwriter.writerow(tax_row)

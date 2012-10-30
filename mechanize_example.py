import mechanize
from BeautifulSoup import BeautifulSoup

br = mechanize.Browser()
br.set_handle_robots(False)

br.open('https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific')

br.select_form('Query1')
br.form['p'] = ['20121']
br.form['m'] = ['0160001']
br.submit()

soup = BeautifulSoup(br.response().read())

print soup.prettify()






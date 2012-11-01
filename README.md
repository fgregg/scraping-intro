A High Level Introduction to Scraping
====

# What's the question?

Say we are interested in consumer spending. We'd like to know how total level of spending changes over time as well as how 
people shift what they spend their money on. Maybe we are interested because it its an indicator of future changes or maybe 
its connects to some theory we would like to test.

For some questions the right place to go is the [Consumer Expenditure Survey](http://en.wikipedia.org/wiki/Consumer_Expenditure_Survey). 
But maybe you only really cared about what's going on in Chicago, at an aggregate level. That survey can't really help you.

Illinois reports quarterly sales tax revenue by municipality or county and breaks out revenue by industrial 
classifications groupings. We don't have to make too many terrible assumptions to treat sales tax revenue as an indicator 
of consumer spending. Unfortunately, these data are not nicely packaged and ready for download. They are only available 
online through a Department of Revenue website: https://www.revenue.state.il.us/app/kob/index.jsp 

So now, we have to ask ourselves, 'Is this the data I need?' Having a clear idea what question you are trying to 
answer will not only make it much more likely that your effort will be worth it, but will usually  
simplify the task. 

# Is scraping the best way to get the data?

Let's assume that we decide that we want this data. How should we go about getting it?

The best, fastest, and easiest thing to do is often to just ask for it. Poke around the Department of Revenue site and 
you can find contact information for someone who can probably send you the data.

# Am I allowed to scrape the data?

If we don't go down that route then we ask, 'Am I allowed to scrape this data?'

Many websites have terms of services that describe what they want you to do and not do. For example Google's, 
says "Don’t misuse our Services. For example, don’t interfere with our Services or try to access them using a 
method other than the interface and the instructions that we provide."  This means, among other things, don't program 
your own scraper for google.com.

Whether or not you have ever read them, much less explicitly agreed to these terms, a properly written terms of 
service is an enforcable contract, and if you violate those terms you could be sued. It's up to you to find out 
whether scraping a site is prohibited.

On the state's site, I could not find any prohibition against scraping the site in the 
[Legal Notices](http://tax.illinois.gov/AboutIdor/LegalNotices.htm) page or anywhere else. 

# Let's do this!
Let's go to the tantalizingly named [Standard Industrial Classification (SIC) Code Reporting](https://www.revenue.state.il.us/app/kob/index.jsp), and click on
the link to 'Specific Muncipalities and Counties.' We get a page that has a form where we can select a reporting period, a
municipal or county government, and a tax type. Let's keep the default for the reporting period and select 'Chicago' from
the drowp down list 'Municipal or County Government Name'. Then click 'Start Search.'

If all goes well, we get a page that shows us Chicago's tax information for the most recent reporting period.

Our task is to write a computer program that 
1. Requests Chicago's tax information for every reporting period
2. Extracts the relevant data from the results of those requests

So, we need to understand how make requests and how responses tends to be organized on the web.

## What's the request?
Let's hit the back button, and let's look at the address. 

    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific
    
then, let's go forward and look at the address for our search results

    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20122&m=0160001&c=000&t=00&x=95&y=12

The first part is the same, but there's a bunch more stuff in the search result address. That stuff, 
starting with the '?,' is a request

    r=Specific&p=20122&m=0160001&c=000&t=00&x=95&y=12

We are saying to some program on their end, 'please give me the resource that corresponds 
to a request with the following parameters.'

    r : Specific
    p : 20122
    m : 0160001
    c : 000
    t : 00
    x : 95 
    y : 12

Let's try changing some of these parameters. First let's see if we need all of them.

    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20122&m=0160001&c=000&t=00&x=95&y=12
    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20122&m=0160001&c=000&t=00&x=95
    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20122&m=0160001&c=000&t=00
    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20122&m=0160001&c=000
    https://www.revenue.state.il.us/app/kob/KOBReport?r=Specific&p=20122&m=0160001
    https://www.revenue.state.il.us/app/kob/KOBReport?p=20122&m=0160001

All these requests return the same results. So, it looks like that the only parameters we have to worry about are
'p' and 'm.' 

At this point, some of you maybe guessing that 'p' is the period value, where the first four digits of the
value are the year and the last digit is the reporting period. Let's try out that theory.

    https://www.revenue.state.il.us/app/kob/KOBReport?p=20121&m=0160001
    https://www.revenue.state.il.us/app/kob/KOBReport?p=20111&m=0160001
    
The first request does give us the tax information for the first quarter of 2012 and the second gives us the information
for the first quarter of 2011. So, it looks like we know how to request different years and quarters.

Looks like 'm' might be the municipal identifier, and if we try to change it we don't get information about Chicago.

    https://www.revenue.state.il.us/app/kob/KOBReport?p=20122&m=0160002
  
However, it's not clear whether there is any logic to having Chicago be '0160001.'

So now, we actually know enough that we can request the tax information for arbitrary reporting periods without 
having to use the form. However, we still don't know the range of reporting periods or how to ask for tax information
for other places. We'll return to these issue after we talk a little bit about HTML and extracting information from
web pages.

## Parsing Results





There are two main ways that we make requests from websites and we are seeing one of them




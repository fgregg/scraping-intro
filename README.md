An Introduction to Scraping
====

# What's the question?

Say we are interested in consumer spending in Chicago. We'd like to know how total level of spending changes over time 
as well as how Chicagoans shift what they spend their money on. Maybe we are interested because it its an indicator 
of future changes or maybe its connects to some theory we would like to test. Unfortunately, a typical source, like 
the national [Consumer Expenditure Survey](http://en.wikipedia.org/wiki/Consumer_Expenditure_Survey), can't really tell 
us that much about Chicago consumers.

Fortunately, Illinois's Department of Revenue publishes quarterly sales tax revenue by municipality or county and 
breaks out revenue by industrial classifications groupings. Unfortunately, these data are not nicely packaged and 
ready for download. They are only available online through a Department of Revenue 
website: https://www.revenue.state.il.us/app/kob/index.jsp 

We can scrape that website, but before we start we need to make sure that it's worth it. Is it a reasonable to
assume that tax revenue is an indicator of consumer spending? Is the data too aggregated? If we had all the data,
is the question worth answering? What is the minimum amount of data that I need to see if it's worth scraping
more?

If you have, a clear idea what question the scraping will answer, it is more likely that the scraping will be worthwhile, 
and it will also often simplify the task. 

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
Let's go to the tantalizingly named [Standard Industrial Classification (SIC) Code Reporting](https://www.revenue.state.il.us/app/kob/index.jsp), 
and click on the link to 'Specific Muncipalities and Counties.' We get a page that has a form where we can select a 
reporting period, a municipal or county government, and a tax type. Let's keep the default for the reporting period and 
select 'Chicago' from the drop down list 'Municipal or County Government Name'. Then click 'Start Search.'

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

We are saying to some program on their end, 'Give me the resource that corresponds 
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
When we make a valid request to a website, it responds with an blob of text that is an HTML document. HTML is a 
mixture of text and a directions of how to layout that text. Your browser interprets those directions and makes 
pretty and complicated things for you, but it all starts with the HTML that the website sent you. 
Let's look at some of HTML right now.

On a [results page](https://www.revenue.state.il.us/app/kob/KOBReport?p=20122&m=0160001). If you have a two button 
mouse click on the page with your left button. If you have a Mac, CMD-Click. You should see a menu that has an option called
'View Source.' Select it. See... it's just a bunch of text.

### Basics of HTML
Some pieces of text are enclosed in angle brackets: <>. These are called tags and are directions on how to layout the site. 
Most tags come in pairs, which are called start and end tags. For example the paragraph tag is `<p>`, and the way 
that you say that bunch of sentences are a paragraph are to put them between opening and closing paragraph tags:

```html
<p>This is a pretty short paragraph</p>
```
    
Some tags have additional options, like the link tag `<a>` if this tag has an `href` option (standing for hypertext 
reference), then the enclosed text will be a clickable link to the value of the `href` option. 

```html
<a href="http://google.com">This text will be shown clickable as a link to http://google.com</a>
```
One important consequence of tags coming in start and end pairs is that an HTML document can be modeled as a hierarchy. 
Everything between a start and close tag can be seen as *child* of that tag. For example the short HTML document

```html
<html>
    <head>
        <title>
            Example of Hierarchy
        </title>
    </head>
    <body>
        <p>
            A short paragraph with a <a href='http://google.com'>link</a>.
        </p>
        <p>
            Another short paragraph
        </p>
    </body>
</html>
```

can be seen as having this hierachy
```
html    
  - head (child of html)
    - title (child of head, grandchild of head)  
  - body (child of html)
    - p (chid of body, grandchild of html)
      - a (child of p, grandchild of body, great-grandchild of html)
    - p (chid of body, grandchild of html)
```

This hierarchy is very useful because it means that we can refer unambiguously to every element of an HTML document. 
If we want identify the last paragraph, we can refer to it as the second child of the second child of the html tag.

## Back to the Source
Alright let's return to the source of our results page and see what we can learn. First let's find the `<form>` tag. Notice
that is has a name attribute 'Query1'. Next notice that there is a `<select>` tag which has the name 'p'. It has lots of 
`<option>` children for the different reporting periods. It we hadn't guessed it, viewing the source would have
let us know that the 'p' parameter corresponded to the reporting period.

```html
<FORM METHOD="get" NAME="Query1" ACTION="KOBReport">
<INPUT TYPE="HIDDEN" NAME="r" VALUE="Specific">
<TABLE BORDER=0 CELLPADDING=0 CELLSPACING=3>
<TR>
<TD COLSPAN=2 NOWRAP>
Report Period:
<SELECT NAME="p">
<OPTION SELECTED VALUE="20122">2012 2nd quarter - Sales made during April, May, and June 2012</OPTION>
<OPTION VALUE="20121">2012 1st quarter - Sales made during January, February, and March 2012</OPTION>
<OPTION VALUE="20110">2011 Calendar Year - Sales made during January 2011 through December 2011</OPTION>
...
<OPTION VALUE="19994">1999 4th quarter - Sales made during October, November, and December 1999</OPTION>
<OPTION VALUE="19993">1999 3rd quarter - Sales made during July, August, and September 1999</OPTION>
<OPTION VALUE="19980">1998 Calendar Year - Sales made during January 1998 through December 1998</OPTION>
<OPTION VALUE="19970">1997 Calendar Year - Sales made during January 1997 through December 1997</OPTION>
<OPTION VALUE="19960">1996 Calendar Year - Sales made during January 1996 through December 1996</OPTION>
<OPTION VALUE="19950">1995 Calendar Year - Sales made during January 1995 through December 1995</OPTION>
<OPTION VALUE="19940">1994 Calendar Year - Sales made during January 1994 through December 1994</OPTION>
</SELECT>
```

We can learn a few more things from the source. First, for the quarterly reports, the value of 'p' is the year and 
quarter as we suspected. However we also see that sometimes the last digit is 0, and that corresonds to a yearly 
reporting period. We also see that the first reporting period is for the 1994 year, and that quarterly reporting 
seemed to start in the third quarter of 1999.

Moving to the next `<select>` tag 'm', we see the municipal code for Illinois cities in the value options of the `<option>`
children. We don't see a lot of rhyme or reason, but we now know where to look for other muncipality codes.

```html
<SELECT NAME="m">
<OPTION VALUE="0000000">[SELECT]</OPTION>
<OPTION VALUE="0480002">Abingdon</OPTION>
<OPTION VALUE="0015000">Adams County Government</OPTION>
...
<OPTION VALUE="0280020">Zeigler</OPTION>
<OPTION VALUE="0490030">Zion</OPTION>
</SELECT>
```

Let's move on to the data.

### Extracting the data

What we would like to do is find some distinguishing pattern that lets us just grab the data we want.

Let's start by noticing that the revenue data are enclosed in `<td>` tags and that these tags have some arguments.

```html
<TD CLASS="data" ALIGN="right" VALIGN="top" NOWRAP>
<CENTER><B>ST</B></CENTER>b
18,887,148.64<BR>
16,185,354.22<BR>
62,117,172.52<BR>
17,352,693.36<BR>
14,166,524.92<BR>
7,891,375.77<BR>
32,494,883.62<BR>
29,752,400.16<BR>
20,989,444.21<BR>
4,220,617.81<BR>
224,057,615.23<BR><BR></TD>
```

Our first script will grab all the parts of page that have that pattern.

    python grab_tax_raw.py

Well that worked. Let's extend this a little bit py processing the text inside the `<td>` tags and get the an array of 
the revenues. For this we are going to do some simple string processing.

    python grab_tax_list.py

We are close, but notice that the same tax name appears more than once. The results reports the the Chicago taxes that are 
collected from retailers located in Cook County separately from the retailers located in DuPage count (it's just few by O'Hare).
Going back to the source we can see that these two sets of results are in sibling tables. The opening tags have the form

```html
<TABLE WIDTH="600" BORDER=0 CELLPADDING=0 CELLSPACING=0>
```

This is a little hard to see because of the formatting of the source. Fortunately, BeautifulSoup can pretty the 
source up for us, so the hierarchy is easier to see.

    python beautify_results.py

We'll want to grab the county info, and the number of taxpayers while we are at it.

    python complete_page.py


So we have all the results from one page. Now let's grab all the pages, and write the results into a comma delimited file
we'll call `taxes.csv`.

    python direct_example.py

## Payoff
Once we have the `taxes.csv`, the scraping is done and we move on to do whatever we wanted to do with the data in
the first place. Let's make some simple graphs. 

![Sales](https://github.com/fgregg/scraping-intro/raw/master/sales.png)
![Sales](https://github.com/fgregg/scraping-intro/raw/master/retailers.png)

# More topics and resources

* [Post Requests](http://en.wikipedia.org/wiki/POST_%28HTTP%29): We discussed one of the major ways of making requests to websites -- encoding the request in the addres. We 
can also make requests in what are called the message bodies. Many, more complicated websites use this other POST method. It
can be pretty tricky to figure out exactly what the right POST request is. Tools like [Firebug](http://getfirebug.com/) 
or [Chrome Developer Tools](https://developers.google.com/chrome-developer-tools/) are invaluable in tracing what
requests get what results.
* [ScraperWiki](https://scraperwiki.com/) is a repository of scraping programs. You can find many useful patterns and inspiration here.
* [Open Gov Hack Night](http://opengovhacknight.eventbrite.com/): Every Tuesday at 1871 in the Merchandise Mart, Chicago developers working with open data get together to work on projects
  and learn from each other. Many folks have written many scrapers, and you can get some good help here.




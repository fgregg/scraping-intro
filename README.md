A High Level Introduction to Scraping
====

# What's the question?

Say we are interested in consumer spending. We'd like to know how total level of spending changes over time as well as how 
people shift what they spend their money on. Maybe we are interested because it its an indicator of future changes or maybe 
its connects to some theory we would like to test.

For some questions the right place to go is the (Consumer Expenditure Survey)[http://en.wikipedia.org/wiki/Consumer_Expenditure_Survey]. 
But maybe you really cared about what's going on in Chicago, at an aggregate level. That survey can't really help you.

Illinois reports quarterly sales tax revenue by municipality or county and breaks out revenue by industrial 
classifications groupings. We don't have to make too many terrible assumptions to treat sales tax revenue as an indicator 
of consumer spending. Unfortunately, these data are not nicely packaged and ready for download. They are only available online through a Department of Revenue website: https://www.revenue.state.il.us/app/kob/index.jsp 

So now, we have to ask ourselves, 'Is this the data I need?' Having a clear idea what question you are trying to answer will not only make it much more likely that your effort will be worth it, but will usually dramatically simplify the task. 

# Is scraping the best way to get the data?

Let's assume that we decide that we want this data. How should we go about getting it?

The best, fastest, and easiest thing to do is often to just ask for it. Poke around the Department of Revenue site and 
you can find contact information for someone who can probably send you the data.

# Am I allowed to scrape the data?

If we don't go down that route then we ask, 'Am I allowed to scrape this data?'

Many websites have terms of services that you describe what they want you to do and not do. For example Google's, says "Don’t misuse our Services. For example, don’t interfere with our Services or try to access them using a method other than the interface and the instructions that we provide."  This means, among other things, don't program your own scraper for google.com.

Whether or not you have ever read them, much less explicitly agreed to these terms, a properly written terms of service is an enforcable contract, and if you violate those terms you could be sued. It's up to you to find out whether scraping a site is prohibited.

On the state's site, I could not find any prohibition against scraping the site in the (Legal Notices)[http://tax.illinois.gov/AboutIdor/LegalNotices.htm] page or anywhere else. 

# Let's do this!





taxes <- read.csv("taxes.csv", header=TRUE)

chicago_tax <- taxes[taxes$tax_type == "HMR",]

chicago_total <- aggregate(chicago_tax$total,
                           by=list(paste(chicago_tax$year,
                             chicago_tax$quarter)),
                           FUN=sum,
                           na.rm=TRUE)

chicago_payers <- aggregate(chicago_tax$number_taxpayers,
                            by=list(paste(chicago_tax$year,
                              chicago_tax$quarter)),
                            FUN=sum,
                            na.rm=TRUE)

chicago_total <- ts(chicago_total$x, c(1999,3), c(2012,2), 4)
chicago_payers <- ts(chicago_payers$x, c(1999,3), c(2012,2), 4)

tax_rate = c(rep(.01, 24), rep(.0125, 28))

plot((chicago_total/tax_rate)/1000000000, ylab="Dollars, billions", main="Taxable Sales")

plot(chicago_payers)


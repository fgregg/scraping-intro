taxes <- read.csv("taxes.csv", header=TRUE)

chicago_rate = c(rep(.01, 24), rep(.0125, 28))

chicago_tax <- taxes[taxes$tax_type == "HMR",]

chicago_total <- aggregate(chicago_tax$total,
                           by=list(paste(chicago_tax$year,
                             chicago_tax$quarter)),
                           FUN=sum)

chicago_total <- ts(chicago_total$x, c(1999,3), c(2012,2), 4)
chicago_total <- chicago_total/chicago_rate


plot(chicago_total/1000000000, ylab="Dollars, billions", main="Taxable Sales in Chicago")

chicago_payers <- aggregate(chicago_tax$number_taxpayers,
                            by=list(paste(chicago_tax$year,
                              chicago_tax$quarter)),
                            FUN=sum)

chicago_payers <- ts(chicago_payers$x, c(1999,3), c(2012,2), 4)

plot(chicago_payers, main="Retailers in Chicago")

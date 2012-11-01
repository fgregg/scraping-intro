taxes <- read.csv("taxes.csv", header=TRUE)

chicago_tax <- taxes[taxes$tax_type == "CHMR",]

chicago_total <- ts(chicago_tax$total, c(1999,3), c(2012,2), 4)
chicago_payers <- ts(chicago_tax$number_taxpayers, c(1999,3), c(2012,2), )

plot(chicago_total/1000000, ylab="Dollars, millions", main="Chicago Home Rule Revenue by Quarter")


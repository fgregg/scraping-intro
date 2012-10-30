taxes <- read.csv("taxes.csv", header=TRUE)

chicago_tax <- taxes[taxes$tax_type == "CHMR",]
chicago_tax <- ts(chicago_tax$total, c(1999,3), c(2012,2), 4)

plot(chicago_tax)

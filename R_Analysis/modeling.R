library(DBI)
library(RSQLite)
library("maps")

source('utility.R')

database <- "database/altran.db"

con <- dbConnect(RSQLite::SQLite(), "database/altran.db")

chunk <- get_chunk(con, up)

x <- chunk$speed
y <- chunk$signal_inst

lm1 <- lm(y~x)
print(lm1)
summary(lm1)

plot(x,y, pch=19, xlab="Speed", ylab="Signal Strength")
title("Modeling of signal strength as a function of speed", line=1)
abline(lm1, col="red")


#lac and lgn
x <- chunk$lac
y <- chunk$lng

lm1 <- lm(y~x)
print(lm1)
summary(lm1)

plot(x,y, pch=19, xlab="LAC", ylab="Longitude")
title("Modeling of longitude as a function of LAC", line=1)
abline(lm1, col="red")

resid <- residuals(lm1)
y_hat <- fitted.values(lm1)

plot(y_hat,resid, pch=19, xlab="Fitted values", ylab="Residuals")
title("Residual of our model as a function of fitted values", line=1)
abline(h=0, col="red")

hist(resid)

qqnorm(resid, line=1, pch=19)
abline(a=2, b=42, col="red")

#lac and lat
x <- chunk$lac
y <- chunk$lat

lm1 <- lm(y~x)
print(lm1)
summary(lm1)

plot(x,y, pch=19, xlab="LAC", ylab="Latitude")
title("Modeling of latitude as a function of LAC", line=1)
abline(lm1, col="red")

resid <- residuals(lm1)
y_hat <- fitted.values(lm1)

plot(y_hat,resid, pch=19, xlab="Fitted values", ylab="Residuals")
title("Residual of our model as a function of fitted values", line=1)
abline(h=0, col="red")

hist(resid)

qqnorm(resid, line=1, pch=19)
abline(a=-20, b=15, col="red")


##
#lac and lgn+lat
x <- chunk$lac
y2 <- chunk$lat
y <- chunk$lng

lm2 <- lm(y2+y~x)
print(lm2)
summary(lm2)

plot(x,y+y2, pch=19, xlab="LAC", ylab="Longitude + Latitude")
title("Modeling of longitude as a function of LAC", line=1)

abline(lm2, col="red")

resid2 <- residuals(lm2)
y_hat2 <- fitted.values(lm2)


plot(y_hat2, resid2)
abline(h=0, col="red")

hist(resid2)
qqnorm(resid2)
abline(a=2, b=42, col="red")



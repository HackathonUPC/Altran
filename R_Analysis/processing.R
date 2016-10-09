library(DBI)
library(RSQLite)
library("maps")

source('utility.R')

database <- "database/altran.db"

con <- dbConnect(RSQLite::SQLite(), "database/altran.db")

up <- 50000

month <- 6
year <- 2016

chunk <- get_chunk(con, up, month_range = c(month,month), year=year)

############
# Visu_lac # 
{
  visu_lac(chunk, remap=TRUE, lac.num=1)
  
  for (i in 2:length(lcolors))
  {
    visu_lac(chunk, remap=FALSE, lac.num=i)
  }
  
  # for (i in length(lcolors):(length(lcolors)+1+length(lcolors)))
  # {
  #   visu_lac(chunk, remap=FALSE, lac.num=i, offset=1)
  # }
}
# Visu_lac # 
############


#################
# Visu_f.carier # 
{
  visu_f.carrier(chunk, "movistar", col=2)
  write.legend(2, "Vodafone")
  
  visu_f.carrier(chunk, "orange", col=4, remap=FALSE)
  write.legend(4, "Orange", number=2)
  
  visu_f.carrier(chunk, "vodafone", col=1, remap=FALSE)
  write.legend(1, "Vodafone", number=3)
}
# Visu_f.carier #
#################
up = 100000
year = 2016

for(year in 2015:2016)
{
for(month in 1:12)
{
  con <- dbConnect(RSQLite::SQLite(), "database/altran.db")
  chunk <- get_chunk(con, month_range = c(month,month), year=year)
  

#################
# Visu_f.carrier.sigstr # 
{
  folder <- "plots/carrier_coverage/evolution/"
  fname <- paste("carrier_coverage_", year, "_",month,".png",sep="")
  png(filename=paste(folder,fname, sep=""))
  
  #ploting
  visu_f.carrier.sigstr(chunk, "movistar", col=2)
  write.legend(2, "Movistar")
  
  visu_f.carrier.sigstr(chunk, "orange", col=4, remap=FALSE)
  write.legend(4, "Orange", number=2)
  
  visu_f.carrier.sigstr(chunk, "vodafone", col=1, remap=FALSE)
  write.legend(1, "Vodafone", number=3)
  
  ptitle <- "Coverage of main providers with size proportional to signal"
  ptitle2 <- paste("strength (", months[month], " ", year ,")",sep="")
  text(-4.8, 36.4, ptitle, pos=4)
  text(-4.8, 36.1, ptitle2, pos=4)
  
  dev.off()
  
}
# Visu_f.carier.sigstr #
#################
}#endformonth
}#endforyear
#00:45 start
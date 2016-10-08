library(DBI)
library(RSQLite)
library("maps")

source('utility.R')

database <- "database/altran.db"

con <- dbConnect(RSQLite::SQLite(), "database/altran.db")

up <- 5000

chunk <- get_chunk(con, up)

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

#################
# Visu_f.carrier.sigstr # 
{
  visu_f.carrier.sigstr(chunk, "movistar", col=2)
  write.legend(2, "Movistar")
  
  visu_f.carrier.sigstr(chunk, "orange", col=4, remap=FALSE)
  write.legend(4, "Orange", number=2)
  
  visu_f.carrier.sigstr(chunk, "vodafone", col=1, remap=FALSE)
  write.legend(1, "Vodafone", number=3)
}
# Visu_f.carier.sigstr #
#################
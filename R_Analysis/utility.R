lcolors = c("red", "blue", "green", "orange", "yellow", "purple", "salmon")
region = c("Spain", "Portugal")

#con: connexion of database
#up: if we want to take just 'up' first values. -1 for everything
get_chunk <- function(con, up=-1, month_range=c())
{
  extra_req <- ""
  
  if(length(month_range) == 2)
  {
    extra_req = paste("AND month >=", month_range[1], "AND month <= ", month_range[2])
  }
  req <- paste("SELECT lac, month, lat, lng, signal_inst, fullCarrier, speed  FROM altran WHERE lac > 0",extra_req,"ORDER BY lac;")
  
  res <- dbSendQuery(con, req)
  
  (chunk <- dbFetch(res,n=up))
}

#####################
#####################
#Objective : popular area - group by lac


visu_lac <-function(chunk, lac.num, remap=TRUE, offset=0)
{
  #filtered chunk
  f.chunk <- chunk[chunk$lac == lac.num,]
  
  lng.points <- f.chunk$lng
  lat.points <- f.chunk$lat
  
  if (remap)
  {
    map("world", region, fill=TRUE, col="white", bg="lightblue", mar=c(0,0,0,0))
    text(2.1833+0.1,41.3833, "Barcelona", pos=4)
  }
  points(lng.points,lat.points, col=lcolors[1 + ((lac.num-1) %% length(lcolors))], pch=16+offset, lw=2)
  points(2.1833, 41.3833, col="black", pch=16)  #Barcelona
}

# group by carrier
#Visualisation fullCarrier
visu_f.carrier <- function(chunk, carrier, remap=TRUE, offset=0, col)
{
  f.chunk <- chunk[chunk$fullCarrier == carrier,]
  f.chunk <- f.chunk[!is.na(f.chunk$lat),]
  
  lng.points <- f.chunk$lng
  lat.points <- f.chunk$lat
  
  if (remap)
  {
    map("world", region, fill=TRUE, col="white", bg="lightblue", mar=c(0,0,0,0))
    text(2.1833+0.1,41.3833, "Barcelona", pos=4)
  }
  points(lng.points,lat.points, col=lcolors[1 + ((col-1) %% length(lcolors))], pch=16+offset)
  points(2.1833, 41.3833, col="black", pch=16)  #Barcelona
}

# group by carrier
#Visualisation fullCarrier with dot size proportional to signal strength

scale.factor <- 2

visu_f.carrier.sigstr <- function(chunk, carrier, remap=TRUE, offset=0, col)
{
  f.chunk <- chunk[chunk$fullCarrier == carrier,]
  f.chunk <- f.chunk[!is.na(f.chunk$lat),]
  
  lng.points <- f.chunk$lng
  lat.points <- f.chunk$lat
  
  sigstr.points <- f.chunk$signal_inst
  fact <- max(sigstr.points)/scale.factor  #some scaling
  
  sigstr.points <- sigstr.points/fact
  
  if (remap)
  {
    map("world", c("Spain", "Portugal"), fill=TRUE, col="white", bg="lightblue", mar=c(0,0,0,0))
    text(2.1833+0.1,41.3833, "Barcelona", pos=4)
  }
  
  points(lng.points,lat.points, col="black", pch=16+offset, cex=0.7+sigstr.points)
  points(lng.points,lat.points, col=lcolors[1 + ((col-1) %% length(lcolors))], pch=16+offset, cex=sigstr.points)
  points(2.1833, 41.3833, col="black", pch=16)  #Barcelona
  
  print(paste(length(lng.points), " points plotted"))
  print(lng.points[1])
}

write.legend <- function(color, label, number=1)
{
  startX <- 2
  startY <- 39
  height <- 0.4

  y <- startY-height*(number-1)
  points(startX, y, col=lcolors[color], pch = 16)
  text(startX+0.2, y, label, pos=4)
}

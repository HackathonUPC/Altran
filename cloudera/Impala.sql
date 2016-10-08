create table krishna.altran(ts int, dt string, lat string,
					lng string, signal_inst int, signal_min int,
					signal_max int, signal_avg int, carrier string,
					fullCarrier string, status string, net int,
					net_type string, lac int, cid int, psc int, speed string,
					satellites int, precision1 string, provider string,
					activity string, incident string, downloadSpeed int, uploadSpeed int )
  row format delimited
  fields terminated by ',';

LOAD DATA INPATH '/user/cloudera/output.csv' overwrite INTO TABLE krishna.altran PARTITION (partcol1=ts);

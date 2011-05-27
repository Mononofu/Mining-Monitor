import time
import datetime
from optparse import OptionParser
import sqlite3
import config

parser = OptionParser()
parser.add_option("-t", "--timeframe", type="int", dest="timeframe",
                  default=4, help="timefram in hours to graph")
parser.add_option("-r", "--resolution", type="int", dest="resolution",
                  default=20, help="one stat point every x seconds")

(options, args) = parser.parse_args()

conn = sqlite3.connect(config.db_file)
c = conn.cursor()

timest = []
load = []
temp = []
fanspeed = []
fanrpm = []
hashrate = []
efficiency = []

c.execute("select * from stats where time > %f order by time"
          % (time.time() - options.timeframe*3600))
for row in c:
    timest.append(datetime.datetime.fromtimestamp(row[0]))
    load.append(row[1])
    temp.append(row[2])
    fanspeed.append(row[3])
    fanrpm.append(row[4])
    hashrate.append(row[5])
    efficiency.append(row[6])

c.close()
conn.close()

# print the data points in csv format
for i in range(len(timest)):
    if i % (options.resolution / 10) == 0:
        print "%s;%d;%d;%d;%f" % (timest[i].strftime("%H:%M"),
                                  load[i],
                                  temp[i],
                                  fanspeed[i],
                                  hashrate[i])

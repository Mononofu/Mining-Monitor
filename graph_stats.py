import sqlite3
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib
import datetime
import matplotlib.dates as mdates
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-t", "--timeframe", type="int", dest="timeframe",
                  default=4, help="timefram in hours to graph")

(options, args) = parser.parse_args()

conn = sqlite3.connect("stats.sqlite")
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

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(timest, temp, '-',
        timest, fanspeed, '-',
        timest, load, '--',
        timest, efficiency, '--')

hours    = mdates.HourLocator()   # every year
minutes  = mdates.MinuteLocator()  # every month
hoursFmt = mdates.DateFormatter('%H:%M')

ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)
ax.xaxis.set_minor_locator(minutes)


datemin = timest[0]
datemax = timest[-1]
ax.set_xlim(datemin, datemax)
ax.set_ylim(0, 100)

ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

plt.legend(('Temperature C', 'Fan %', 'Load %', 'Efficiency %'),
           'lower center', shadow=True, fancybox=True)

leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
llines = leg.get_lines()  # all the lines.Line2D instance in the legend
frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

frame.set_facecolor('0.80')      # set the frame face color to light gray
plt.setp(ltext, fontsize='small')    # the legend text fontsize
plt.setp(llines, linewidth=1.5)      # the legend linewidth

plt.savefig('temperature%02d.png' % options.timeframe, dpi=150)



ax.cla()
ax.plot(timest, hashrate)
ax.set_ylim(0, 450)

ax.xaxis.set_major_locator(hours)
ax.xaxis.set_major_formatter(hoursFmt)
ax.xaxis.set_minor_locator(minutes)

datemin = timest[0]
datemax = timest[-1]
ax.set_xlim(datemin, datemax)

ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()


plt.legend(('Hashrate in MHash/s',),
           'lower center', shadow=True, fancybox=True)
leg = plt.gca().get_legend()
ltext  = leg.get_texts()  # all the text.Text instance in the legend
llines = leg.get_lines()  # all the lines.Line2D instance in the legend
frame  = leg.get_frame()  # the patch.Rectangle instance surrounding the legend

frame.set_facecolor('0.80')      # set the frame face color to light gray
plt.setp(ltext, fontsize='small')    # the legend text fontsize
plt.setp(llines, linewidth=1.5)      # the legend linewidth

plt.savefig('hashrate%02d.png' % options.timeframe, dpi=150)

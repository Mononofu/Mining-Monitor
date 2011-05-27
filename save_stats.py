import sqlite3
import ADL
import time

ADL.SetupADL(0)

update_frequency = 6    # updates per minute

for i in range(update_frequency):
    conn = sqlite3.connect("/home/mononofu/pyADL/stats.sqlite")
    c = conn.cursor()

    c.execute("create table if not exists stats (time REAL, load INTEGER, temp REAL, fanspeed INTEGER, fanrpm INTEGER, hashrate REAL, efficiency REAL)")

    try:
        hashrate, efficiency = open("/home/mononofu/phoenix-1.48/miner.log").readline().split(':')
    except ValueError:
        hashrate, efficiency = (0, 0)
    hashrate = int(hashrate)
    efficiency = float(efficiency)
    c.execute("insert into stats values (?, ?, ?, ?, ?, ?, ?)",
              ( time.time(),
                ADL.getGPULoad(),
                ADL.getTemp(),
                ADL.getFanSpeed(),
                ADL.getFanRPM(),
                hashrate / 1000.,
                efficiency * 100
                )
              )

    conn.commit()
    c.close()
    conn.close()
    time.sleep(60/update_frequency)

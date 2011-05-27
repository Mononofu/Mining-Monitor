import sqlite3
import ADL
import time
import config

ADL.SetupADL(config.device_number)

config.

for i in range(config.update_frequency):
    conn = sqlite3.connect(config.db_file)
    c = conn.cursor()

    c.execute("create table if not exists stats (time REAL, load INTEGER, "
              "temp REAL, fanspeed INTEGER, fanrpm INTEGER, hashrate REAL, "
              "efficiency REAL)")

    try:
        hashrate, efficiency = open(config.miner_log).readline().split(':')
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
    time.sleep(60/config.update_frequency)

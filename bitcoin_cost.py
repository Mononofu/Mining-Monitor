import json
import time
import os
import urllib2
import locale

# 1 kWh = 15 cent
# 1 kWh = 3.6 * 10^6 J
# => 4.17 cent / MJ
# => 0.24 MJ / cent

class BitcoinCalculator:
    def __init__(self):
        self.mhash_per_s = 420
        self.gpu_power = 220                         # Watt
        self.system_power = 100                      # Watt
        self.hardware_cost = 320                     # euro
        
        self.kwh_price = 0.15                        # euro
        self.cache_lifetime = 1800                   # seconds
        self.cache_file = 'bitcoin_cache.txt'
        
        self.coins_per_block = 50                    # won't change before 2012
        locale.setlocale(locale.LC_ALL, 'en_US.utf8')

################################################################################
############################## do not edit below ###############################
################################################################################

        
    def update_rates(self):
        self.difficulty = float(urllib2.urlopen("http://blockexplorer.com/q/getdifficulty").read())
        rate = urllib2.urlopen("https://mtgox.com/code/data/ticker.php").read()
        self.usd_per_bitcoin = float(json.loads(rate)["ticker"]["buy"])
        self.eur_to_usd = float( urllib2.urlopen("http://download.finance.yahoo.com/d/quotes.csv?s=EURUSD=X&f=sl1d1t1c1ohgv&e=.csv").read().split(',')[1] )
        f = open(self.cache_file, 'w')
        f.write("%f\n" % time.time())
        f.write("%f\n" % self.difficulty)
        f.write("%f\n" % self.usd_per_bitcoin)
        f.write("%f\n" % self.eur_to_usd)


    def run(self):
        try:
            f = open(self.cache_file)
            age = time.time() - float(f.readline())
            if age > self.cache_lifetime:
                print "cache too old"
                f.close()
                os.remove(self.cache_file)
                self.update_rates()
            else:
                self.difficulty = float(f.readline())
                self.usd_per_bitcoin = float(f.readline())
                self.eur_to_usd = float(f.readline())
                                        
        except IOError as e:
            print "Creating cache"
            self.update_rates()

        power = self.gpu_power + self.system_power        # in Watt
        hashrate = self.mhash_per_s * 10**6

        mhash_per_joule = 1.0 * self.mhash_per_s / power

        mhash_per_euro = 3.6 * 10**6 / self.kwh_price * mhash_per_joule

        # in seconds
        time_per_bitcoin = (self.difficulty * 2**32 / hashrate
                            / self.coins_per_block)

        # in euro
        cost_per_bitcoin = ((time_per_bitcoin / 3600.)
                            * (power / 1000. * self.kwh_price))

        print "assuming %.2f Mhash per s" % self.mhash_per_s
        print "==> %.3f Mhash per J" % mhash_per_joule
        print "==> %s Mhash per euro" % locale.format("%.2f",
                               mhash_per_euro,
                               grouping=True)
        print "energy cost: %.3f euro per bitcoin" % (cost_per_bitcoin)
        print ""

        eur_per_bitcoin = self.usd_per_bitcoin / self.eur_to_usd

        print "Mt. Gox exchange: %.2f USD per bitcoin" % self.usd_per_bitcoin
        print "or about %.2f EUR per bitcoin" % eur_per_bitcoin
        print ""

        bitcoins_per_day = 3600. * 24. / time_per_bitcoin
        profit_per_day = ((eur_per_bitcoin - cost_per_bitcoin)
                          * bitcoins_per_day)

        print "%.2f bitcoins / day = %.2f EUR" % (bitcoins_per_day,
                                                  profit_per_day)

        print "%.2f bitcoins / month = %.2f EUR" % (bitcoins_per_day * 30,
                                                    profit_per_day * 30)

        print "Break even in %.2f days" % (self.hardware_cost / profit_per_day)


b = BitcoinCalculator()
b.run()

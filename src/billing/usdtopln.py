import urllib2
import xmltodict
from django.conf import settings
from srvup.celery import app


def exchangeRateUSD():
    file = urllib2.urlopen('http://www.nbp.pl/Kursy/xml/LastC.xml')
    data = file.read()
    file.close()
    nbp = xmltodict.parse(data)

    dateOfListing = nbp['tabela_kursow']['data_notowania']
    dateOfPublication = nbp['tabela_kursow']['data_publikacji']
    usd = nbp['tabela_kursow']['pozycja'][0]

    buyingRate = None
    sellingRate = None
    
    if usd['kod_waluty'] == 'USD':
        buyingRate = usd['kurs_kupna'].replace(",",".")
        sellingRate = usd['kurs_sprzedazy'].replace(",",".")
        return (dateOfListing, dateOfPublication, sellingRate, buyingRate)
    else:
        raise Exception("No USD exchange data")


@app.task()
def getTotal():
    EXCHANGE_RATE = float(exchangeRateUSD()[2]) # sell price
    UNIT_PRICE = 25 # USD
    TOTAL_AMOUNT = int(UNIT_PRICE) * EXCHANGE_RATE
    return TOTAL_AMOUNT
    
    
if __name__ == '__main__':
    nbp = exchangeRateUSD()
    print(nbp)

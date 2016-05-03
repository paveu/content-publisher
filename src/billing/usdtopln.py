import urllib2
import xmltodict

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

if __name__ == '__main__':
    nbp = exchangeRateUSD()
    print(nbp)

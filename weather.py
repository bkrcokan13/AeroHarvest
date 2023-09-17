import random, time, requests
from requests import RequestException
from bs4 import BeautifulSoup



class Weather:

    # Search Query
    searchQuery = "https://www.accuweather.com/en/search-locations?query="

    _bsSoup = None

    _weatherCodes = []


    def SearchLocation(self ,location):


        HEADERS = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                        'AppleWebKit/537.36 (KHTML, like Gecko)'
                        'Chrome/116.0.0.0 Safari/537.36'),
            'Accept-Language': 'en-US, en;q=0.5'
        }



        try:
            
            print(self.searchQuery + location)
            weahtherCode = requests.get(
                url=f"{self.searchQuery + location}",
                headers=HEADERS,
                timeout=3
            )



            
        except RequestException:
            print("Error ! ")

    def _GetWeatherCode(data):
        pass
    
    
    # Get Weather Status
    def _WeatherTemp(data):
        return ""
    
    def _AirQuality(data):
        return ""

    def _WindStatus(data):
        return ""

    def _DownloadMap(data):
        return ""



app = Weather()


app.SearchLocation(
    location="Amsterdam"
)
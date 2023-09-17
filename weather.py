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

            if (weahtherCode.status_code == 403):
                print("Status : Forbidden, check your agent or change another agent !.")
            elif (weahtherCode.status_code == 200):
                print("Status : OK !")
                self._GetWeatherCode(data=weahtherCode.content)
                
                


            
        except RequestException:
            print("Error, url not working or not founded !")


    def checkLocationExists(self,data):

        checkResultText = self._bsSoup.find('div', attrs={
            'class':'no-results-text'
        })
        
        if checkResultText:
            
            if checkResultText.text == "No results found.":
                return False
            else:
                return True

    def _GetWeatherCode(self,data):
        

        # Weather Dict
        weatherList = {}

        try:
            # Bs4 Initlaize 
            self._bsSoup = BeautifulSoup(data, "html.parser")
            

            # Check result
            if self.checkLocationExists(data):
                print("Location is not found")
                return weatherList
            else:

                # Collect Weather Code's 
                getAllCode = self._bsSoup.find('div', attrs={'class':'locations-list content-module'})

                # Check Value 
                if getAllCode:

                    # Find div inside all A tag's 
                    weatherCode = getAllCode.find_all('a')

                    count = 0

                    # Clear prev data's
                    weatherList.clear()
                    for code in weatherCode:
                            
                        textLocation = code.text.strip()
                        url = ("https://www.accuweather.com/"+ code.get('href'))

                        count += 1

                        # Convert count Int to Str
                        urlID = str(count)

                        # Create dict
                        weatherList[urlID] = {
                            "location":f"{textLocation}",
                            "apiUrl": f"{url}"
                        }
                    print(f"Location's {len(weatherCode)} found...!")
                
                return weatherList
        except Exception as error:
            print("Error, weather code's not collected or url is broken !! check url or user-agent !")
            print(error.with_traceback())
        

       

    
    # Get Weather Status
    def _WeatherTemp(self, data):
        return ""
    
    def _AirQuality(self, data):
        return ""

    def _WindStatus(self, data):
        return ""

    def _DownloadMap(self, data):
        return ""



app = Weather()


app.SearchLocation(
    location="Rotterdam"
)
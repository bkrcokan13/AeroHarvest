import random, time, requests
from requests import RequestException
from bs4 import BeautifulSoup


class Weather:
    def __init__(self):
        # Search Query
        self.searchQuery = "https://www.accuweather.com/en/search-locations?query="

        self.selectedApiUrl = None

        # Weather Code Check Status
        self.weatherCodeStatus = False

        # Bs4 Object
        self._bsSoup = None

        # Weather Dict
        self.weatherList = {}

        # Weather List's
        self.date = []
        self.pharseDate = []
        self.tempsList = []
        self.panelList = []

        # Config header
        self.HEADERS = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                           'AppleWebKit/537.36 (KHTML, like Gecko)'
                           'Chrome/116.0.0.0 Safari/537.36'),
            'Accept-Language': 'en-US, en;q=0.5'
        }

    def UserUI(self):
        menuTemplate = """               
            .d8b.  d88888b d8888b.  .d88b.  db   db  .d8b.  d8888b. db    db d88888b .d8888. d888888b 
            d8' `8b 88'     88  `8D .8P  Y8. 88   88 d8' `8b 88  `8D 88    88 88'     88'  YP `~~88~~' 
            88ooo88 88ooooo 88oobY' 88    88 88ooo88 88ooo88 88oobY' Y8    8P 88ooooo `8bo.      88    
            88~~~88 88~~~~~ 88`8b   88    88 88~~~88 88~~~88 88`8b   `8b  d8' 88~~~~~   `Y8b.    88    
            88   88 88.     88 `88. `8b  d8' 88   88 88   88 88 `88.  `8bd8'  88.     db   8D    88    
            YP   YP Y88888P 88   YD  `Y88P'  YP   YP YP   YP 88   YD    YP    Y88888P `8888Y'    YP
            
            
            --------------------------------------------------------------------------------------- 
               
        """

        while True:
            print(menuTemplate)

            locationName = input("Location: ")

            if locationName is None:
                input("Please do not enter empty text, press the any key !")
            elif locationName.isdigit():
                input("Please do not enter digit text, press the any key !")
            elif locationName.isalpha() is False:
                input("Please only enter text, press the any key !")
            else:
                self.SearchLocation(location=locationName.lower())

    def SearchLocation(self, location):
        try:

            print(self.searchQuery + location)

            weatherCode = requests.get(
                url=f"{self.searchQuery + location}",
                headers=self.HEADERS,
                timeout=3
            )

            # Check status code
            if weatherCode.status_code == 403:
                print("Status : Forbidden, check your agent or change another agent !.")

            elif weatherCode.status_code == 200:
                print("Status : OK !")
                self._get_weather_code(data=weatherCode.content)

        except RequestException as reqExp:
            print("Error, url not working or not founded !")
            print(reqExp.strerror)

    def checkLocationExists(self, data):

        checkResultText = self._bsSoup.find('div', attrs={
            'class': 'no-results-text'
        })

        if checkResultText:

            if checkResultText.text == "No results found.":
                return False
            else:
                return True

    def _get_weather_code(self, data):

        try:
            # Bs4 Initialize
            self._bsSoup = BeautifulSoup(data, "html.parser")

            # Check result
            if self.checkLocationExists(data):
                print("Location is not found")
                return self.weatherList
            else:

                # Collect Weather Code's 
                getAllCode = self._bsSoup.find('div', attrs={'class': 'locations-list content-module'})

                # Check Value 
                if getAllCode:

                    # Find div inside all A tag's 
                    weatherCode = getAllCode.find_all('a')

                    count = 0
                    # Clear prev data's
                    self.weatherList.clear()
                    for code in weatherCode:
                        # Clear whitespace
                        textLocation = code.text.replace(" ", " ").replace("\n", " ").replace("\t", "")
                        url = ("https://www.accuweather.com" + code.get('href'))

                        # Add count
                        count += 1

                        # Convert count Int to Str
                        urlID = str(count)

                        # Create dict
                        self.weatherList[urlID] = {
                            "location": f"{textLocation}",
                            "apiUrl": f"{url}"
                        }

                    # Check Weather List Length
                    if len(self.weatherList) != 0:
                        print(f"Location {len(self.weatherList)} founded !.")
                        self.weatherCodeStatus = True
                        self.SelectLocation()
                        # print(self.weatherList)

        except Exception as error:
            print("Error, weather code's not collected or url is broken !! check url or user-agent !")
            print(error)

    def SelectLocation(self):
        locationId = None
        while True:

            for location in range(len(self.weatherList)):
                locationName = self.weatherList[str(location + 1)]["location"]
                print(f"({location + 1}) : {locationName}\n")

            # Choice User Input
            inputLocation = input("Select Location : ")

            #
            # print(f"{len(self.weatherList)} - {inputLocation}")

            # Check list out range
            if int(inputLocation) >= (len(self.weatherList) + 1):

                print("Location is not available...!!!")
                input("Press any key !")
            else:
                locationId = str(inputLocation)
                break

        self.CollectData(id=locationId)

    def CollectData(self, id):

        global getDailyUrl

        # Check Page Status
        pageStatus = False

        # Get Page
        getWeather = requests.get(self.weatherList[id]["apiUrl"], headers=self.HEADERS)

        # Check Status Code
        if getWeather.status_code == 200:
            # Get daily weather url
            weatherSoup = BeautifulSoup(getWeather.content, 'html.parser')

            getDailyUrl = weatherSoup.find('a', attrs={
                'data-pageid': 'daily'
            }).get("href")

            # Complete Url
            getDailyUrl = 'https://www.accuweather.com' + getDailyUrl

            pageStatus = True
        elif getWeather.status_code == 403:
            print("403 Forbidden, check headers !")

        if pageStatus:
            try:

                dailyData = requests.get(getDailyUrl, headers=self.HEADERS)

                if dailyData.status_code == 200:

                    dailySoup = BeautifulSoup(dailyData.content, 'html.parser')

                    # Wrapper Panel
                    wrapper = dailySoup.find_all(
                        'div', attrs={
                            'class': 'daily-wrapper'
                        }
                    )

                    # Clear ALl List's
                    self.date.clear()
                    self.pharseDate.clear()
                    self.tempsList.clear()
                    self.panelList.clear()

                    # Wrapper Data's Extract
                    for wrap in wrapper:

                        # Date
                        dowDate = wrap.find('span', attrs={
                            'class': 'module-header dow date'
                        }).text

                        subDate = wrap.find(
                            'span', attrs={
                                'class': 'module-header sub date'
                            }
                        ).text

                        self.date.append(f"(Month:{subDate}-{dowDate})")

                        # Phrase
                        pharse = wrap.find(
                            'div', attrs={
                                'class': 'phrase'
                            }
                        ).text

                        self.pharseDate.append(pharse)

                        # Temps
                        temps = wrap.find_all(
                            'div', attrs={
                                'class': 'temp'
                            }
                        )
                        for temp in temps:
                            high = temp.find(
                                'span', attrs={
                                    'class': 'high'
                                }
                            ).text

                            low = temp.find(
                                'span', attrs={
                                    'class': 'low'
                                }
                            ).text

                            # Clear ('/') and replace empty string
                            low = low.replace('/', "")

                            self.tempsList.append(f"{low}/{high}")

                        # Panels
                        panels = wrap.find(
                            'div', attrs={
                                'class': 'panels'
                            }
                        ).text

                        panels = panels.replace("\n", " ").replace("\t", "-")
                        self.panelList.append(panels)

                    weather_list_zip = zip(self.date, self.pharseDate, self.tempsList, self.panelList)
                    weatherData = list(weather_list_zip)

                    for weather in weatherData:
                        template = f"""
                               |----> {self.weatherList[id]["location"].strip().upper()} {weather[0]}
                               |----------------------------------------------------------------------------------------|                                                                
                               |    -> Temp:   {weather[1]}                                                               
                               |    -> Status: {weather[2]}                                                              
                               |    -> Detail: {weather[3]}                                                              
                               |----------------------------------------------------------------------------------------|
                               """
                        print(template, end="", sep="\n")

                elif dailyData.status_code == 403:
                    print("Daily Weather Page : 403 Forbidden ! ")

            except AttributeError:
                print("Text is not available !")
            except Exception as errorEx:
                print("Error, data not fetched or not found !")
                errorDetails = f"""
                Error Traceback :\n\t{errorEx.with_traceback()}\n\t
                """
                print(errorDetails)


app = Weather()
app.UserUI()

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

        # Config header
        self.HEADERS = {
                'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                            'AppleWebKit/537.36 (KHTML, like Gecko)'
                            'Chrome/116.0.0.0 Safari/537.36'),
                'Accept-Language': 'en-US, en;q=0.5'
        }


    def SearchLocation(self ,location):
        try:
            
            print(self.searchQuery + location)

            weahtherCode = requests.get(
                url=f"{self.searchQuery + location}",
                headers=self.HEADERS,
                timeout=3
            )

            # Check status code
            if (weahtherCode.status_code == 403):
                print("Status : Forbidden, check your agent or change another agent !.")

            elif (weahtherCode.status_code == 200):
                print("Status : OK !")
                self._get_weather_code(data=weahtherCode.content)

        except RequestException as reqExp:
            print("Error, url not working or not founded !")
            print(reqExp.strerror)


    def checkLocationExists(self,data):

        checkResultText = self._bsSoup.find('div', attrs={
            'class':'no-results-text'
        })
        
        if checkResultText:
            
            if checkResultText.text == "No results found.":
                return False
            else:
                return True

    def _get_weather_code(self,data):
        
        try:
            # Bs4 Initlaize 
            self._bsSoup = BeautifulSoup(data, "html.parser")
            
            # Check result
            if self.checkLocationExists(data):
                print("Location is not found")
                return self.weatherList
            else:

                # Collect Weather Code's 
                getAllCode = self._bsSoup.find('div', attrs={'class':'locations-list content-module'})

                # Check Value 
                if getAllCode:

                    # Find div inside all A tag's 
                    weatherCode = getAllCode.find_all('a')

                    count = 0
                    # Clear prev data's
                    self.weatherList.clear()
                    for code in weatherCode:
                        
                        # Clear whitespace
                        textLocation = code.text.replace(" ", " ").replace("\n", " ").replace("\t","")
                        url = ("https://www.accuweather.com/"+ code.get('href'))

                        # Add count
                        count += 1

                        # Convert count Int to Str
                        urlID = str(count)

                        # Create dict
                        self.weatherList[urlID] = {
                            "location":f"{textLocation}",
                            "apiUrl": f"{url}"
                        }
                    
                    # Check Weather List Lenght
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


        # Check Page Status
        pageStatus = False
    

        # Get Page
        getWeather = requests.get(self.weatherList[id]["apiUrl"], headers=self.HEADERS)

        # Check Status Code
        if getWeather.status_code == 200:
            pageStatus = True
        elif getWeather.status_code == 403:
            print("403 Forbidden, check headers !")
        

        if pageStatus:
            try:
                # Parse weather page
                soup = BeautifulSoup(getWeather.content, "html.parser")

          

                cardContent = soup.find_all(
                    'div', attrs={
                        'class':'card-content'
                    }
                )

                for card in cardContent:
                    
                    temp  = card.find('div', attrs={
                        'class':'temp'
                    })

                    tempData = temp.text.split('\n')


                    for data in tempData:
                        splitData = data.split('°')

                        degree = splitData[0]
                        status = splitData[1]

                        print(degree + "°", status)

                    
                    
                   



            except AttributeError:
                print("Text is not available !")
            except Exception as errorEx:
                print("Error, datas not fetched or not found !")
                errorDetails = f"""
                Error Traceback :\n\t{errorEx.with_traceback()}\n\t
                """

                print(errorDetails)
            

            
          

            

            
           

            

            


app = Weather()
app.SearchLocation(location="Amsterdam")
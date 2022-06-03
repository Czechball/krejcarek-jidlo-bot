import sys
import requests
from bs4 import BeautifulSoup
import unidecode
import datetime
import config

url = config.foodUrl
endpoint = config.webhookEndpoint

with open("jidlo.html","r") as file:
	page = file.read()

# #page = requests.get(url)
# file = open("jidlo.html")
# page = file.read()
# file.close()
#soup = BeautifulSoup(page.content, 'html.parser')
soup = BeautifulSoup(page, 'html.parser')

dayNames = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
dayNamesNums = list(range(2,9)) + list(range(11,18)) + list(range(20,27)) + list(range(29,35)) + list(range(38,44))
day1 = list(range(3,9))
day2 = list(range(12,18))
day3 = list(range(21,27))
day4 = list(range(30,36))
day5 = list(range(39,45))
lunches = soup.find("table", {"width" : "709"})
lunInfos = (lunches.findAll("tr"))

def getDay(dayNum):
	match dayNum:
		case 0:
			foodNames = []
			foodPrices = []
			for cells in day1:
				dayInfo = (lunInfos[cells].text.strip()).split("\n")
				foodNames.append(dayInfo[1])
				foodPrices.append(dayInfo[-1])
		case 1:
			foodNames = []
			foodPrices = []
			for cells in day2:
				dayInfo = (lunInfos[cells].text.strip()).split("\n")
				foodNames.append(dayInfo[1])
				foodPrices.append(dayInfo[3])
		case 2:
			foodNames = []
			foodPrices = []
			for cells in day3:
				dayInfo = (lunInfos[cells].text.strip()).split("\n")
				foodNames.append(dayInfo[1])
				foodPrices.append(dayInfo[3])
		case 3:
			foodNames = []
			foodPrices = []
			for cells in day4:
				dayInfo = (lunInfos[cells].text.strip()).split("\n")
				foodNames.append(dayInfo[1])
				foodPrices.append(dayInfo[3])
		case 4:
			foodNames = []
			foodPrices = []
			for cells in day5:
				dayInfo = (lunInfos[cells].text.strip()).split("\n")
				foodNames.append(dayInfo[1])
				foodPrices.append(dayInfo[3])
	finalFoodOutput = []
	finalPriceOutput = []
	for food in range(0,6):
		finalFoodOutput.append(str(food + 1) + ": " + foodNames[food] + "\nCena: " + foodPrices[food])
		mergedFoodOutput = "\n".join(finalFoodOutput) + "\n".join(finalPriceOutput)
 		#return("Jídlo "+str(food + 1),":\n",foodNames[food],"\nCena: ",foodPrices[food])
	return('{}'.format(mergedFoodOutput))
currentDayNum = (datetime.datetime.today().weekday())
hookString = "Jídelníček na " + dayNames[currentDayNum] + ":\n--------\n" + str(getDay(currentDayNum))
print(hookString)

params = '{"text": "' + hookString + '"}'
webhook = requests.post(url = endpoint, data = params.encode('utf-8'))
print(webhook)

def getCurrentDate():

	#date = soup.findAll('strong')[7].text
	date = soup.find(style='text-align: center;', width='579').text
	return date

currentDate = getCurrentDate()
#print(currentDate)

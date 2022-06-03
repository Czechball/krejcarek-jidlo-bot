import sys
import requests
from bs4 import BeautifulSoup
import unidecode
import datetime
import config

url = config.foodUrl
endpoint = config.webhookEndpoint

## Debug for local development ##

#with open("jidlo.html","r") as file:
#	page = file.read()
# file = open("jidlo.html")
# page = file.read()
# file.close()
#soup = BeautifulSoup(page, 'html.parser')

page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

dayNames = ["Pondělí", "Úterý", "Středa", "Čtvrtek", "Pátek"]
#dayNamesNums = list(range(2,9)) + list(range(11,18)) + list(range(20,27)) + list(range(29,35)) + list(range(38,44))
day1 = list(range(3,9))
day2 = list(range(12,18))
day3 = list(range(21,27))
day4 = list(range(30,36))
day5 = list(range(39,45))
lunches = soup.find("table", {"width" : "709"})
lunInfos = (lunches.findAll("tr"))

def getDay(dayNum):
	day = [day1, day2, day3, day4, day5][dayNum]

	foodNames = [lunInfos[cells].text.strip().split("\n")[1] for cells in day]
	foodPrices = [lunInfos[cells].text.strip().split("\n")[-1] for cells in day]
	# print("Food Names: " + str(foodNames))
	# print("Food Prices: " + str(foodPrices))

	finalFoodOutput = ["{i}: {foodName}\nCena: {foodPrice}".format(i=i+1, foodName=foodNames[i], foodPrice=foodPrices[i]) for i in range(0,6)]

	return('{}'.format(finalFoodOutput))



currentDayNum = (datetime.datetime.today().weekday())
hookString = "Jídelníček na " + dayNames[currentDayNum] + ":\n--------\n" + str(getDay(currentDayNum))


if 0 <= currentDayNum <= 4:
	print("Retrieving food menu for day " + str(currentDayNum) + "...")
	params = '{"text": "' + hookString + '"}'
	webhook = requests.post(url = endpoint, data = params.encode('utf-8'))
	print(webhook)
else:
	print("Day " + str(currentDayNum) + " is not a workday, skipping")

## Unused function for retrieving current date from canteen website, might use in future

def getCurrentDate():

	date = soup.find(style='text-align: center;', width='579').text
	return date

currentDate = getCurrentDate()

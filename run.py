# coding=utf-8

import sys
import requests
from bs4 import BeautifulSoup
import unidecode
import datetime
import config

currentDayNum = (datetime.datetime.today().weekday())

url = config.foodUrl
endpoint = config.webhookEndpoint

if 0 <= currentDayNum <= 4:
	print("Retrieving food menu for day " + str(currentDayNum + 1) + "...")
else:
	print("Day " + str(currentDayNum + 1) + " is not a workday, skipping")
	exit()

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

	finalFoodOutput = []
	finalPriceOutput = []
	for food in range(0,6):
		finalFoodOutput.append(str(food + 1) + ": " + foodNames[food] + "\nCena: " + foodPrices[food])
		mergedFoodOutput = "\n".join(finalFoodOutput) + "\n".join(finalPriceOutput)
	return('{}'.format(mergedFoodOutput))

hookString = "Jídelníček na " + dayNames[currentDayNum] + ":\n--------\n" + str(getDay(currentDayNum))
params = '{"text": "' + hookString + '"}'
webhook = requests.post(url = endpoint, data = params.encode('utf-8'))

## Unused function for retrieving current date from canteen website, might use in future

def getCurrentDate():

	date = soup.find(style='text-align: center;', width='579').text
	return date

currentDate = getCurrentDate()

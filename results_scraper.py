from selenium import webdriver
from bs4 import BeautifulSoup
import json
import os
import requests
import WinnerFormat as fwin

clear = lambda: os.system('cls') #on Windows System

url = "https://www.bbc.co.uk"

def toList(list):
	arr = []
	for i in list:
		arr.append(i)
	return arr

def getResults(link):
	sauce = requests.get(url+link)
	soup = BeautifulSoup(sauce.content)
	result = {}
	parties = {}
	turnout = {}
	voteshare = {}
	winner = soup.find("p", {"class": "ge2019-constituency-result-headline__text"})
	result["winner"] = fwin.formatParty(winner.text)
	table = soup.find("ol",{"class": "ge2019-constituency-result__list"})
	info = table.findChildren("li")
	for x in info:
		try:
			c = x.find("div", {"class":"ge2019-constituency-result__row"})
			results =toList(x.find("div", {"class":"ge2019-constituency-result__details"}).findAll("li"))
			candidate = c.find("span",{"class": "ge2019-constituency-result__candidate-name"}).text
			party =  c.find("span",{"class": "ge2019-constituency-result__party-name"}).text
			vote =  results[0].find("span",{"class": "ge2019-constituency-result__details-value"}).text
			share =  results[1].find("span",{"class": "ge2019-constituency-result__details-value"}).text
			change =  results[2].find("span",{"class": "ge2019-constituency-result__details-value"}).text
			parties[party] = {"candidate" : candidate, "vote":vote, "vote_share_%": share,"vote_share_change": change}
		except:
			continue


	result["parties"] = parties
	tout = soup.find("div",{"class": "ge2019-constituency-result-turnout"}).findAll("li", {"role":"listitem"})
	result["turnout"] = {"party_majority": tout[0].find("span", {"class": "ge2019-constituency-result-turnout__value"}).text,
	"registered_voters": tout[1].find("span", {"class": "ge2019-constituency-result-turnout__value"}).text,
	"shares": tout[2].find("span", {"class": "ge2019-constituency-result-turnout__value"}).text,
	"changes_since_2017" :  tout[3].find("span", {"class": "ge2019-constituency-result-turnout__value"}).text}
	return result


soup = BeautifulSoup(requests.get("https://www.bbc.co.uk/news/politics/constituencies").content)
print("Getting Constitutes...")
constitutes =  soup.findAll("tr",{"class":"az-table__row"})
num = 0
results = {}
print("Downloading data...")
for i in constitutes:
	print("{} out of {} downloaded".format(num,len(constitutes)))
	results[i.find("a").text] = getResults(i.find("a", href=True)['href'])
	num = num + 1
	clear()
print("Dumping to file...")
f = open("results.json", "w")
json.dump(results,f, indent=4)
f.close()
print("Data Dumped!!!")


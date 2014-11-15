# This should get data for Gen I Base Stats

# Import stuff
# This is for handling urls
import requests
import re
# This is for web parsing
from bs4 import BeautifulSoup
# This is for writing to a csv
import csv

def getType1(text):
	info = text.split("/")
	type = info[-1][:-4].strip()
	return(type)

def getType2(text):
	info = text.split('\n')
	type = info[-2].strip()
	return(type)
	
f = open('C:/PandP/GenITypes/GenITypes.csv','wb')
writer = csv.writer(f)

# Write the header for the file
writer.writerow(['Number', 'Name', 'Type1', 'Type2'])

for number in range(1,86):
	num = str(number).zfill(3)
	url = "http://www.serebii.net/pokedex/" + num + ".shtml"
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	# To see the actual page,
	# print(soup)

	table = soup.find(bordercolor="#868686")
	rows = table.find_all('tr')

	nameRow = rows[1]
	cells = nameRow.find_all('td')
	name = cells[3].text.strip()
	
	# Catch Nidorans
	if number == 29:
		name = 'Nidoran_F'
	if number == 32:
		name = 'Nidoran_M'
	# Surprisingly, leaving this out won't break everything
	# They are listed as Nidoran (F) and Nidoran (M)

	typeRow = rows[2]
	cells = typeRow.find_all('td')
	if number <= 68:
		if len(cells) == 4:
			type1 = cells[3].find('img').get('src')
			type1 = getType1(type1)
			type2 = 'N/A'
		elif len(cells)== 5:
			type1 = cells[3].find('img').get('src')
			type1 = getType1(type1)
			type2 = cells[4].find('img').get('src')
			type2 = getType1(type2)
	else:
		type1 = cells[3].text
		type1 = getType2(type1)
		type2 = cells[4].text
		type2 = getType2(type2)

	# Fix mistake on Butterfree's 2nd type
	if number == 012:
		type2 = 'flying'
	# Remove Magnemite's and Magneton's Steel typing
	if number == 81 or number == 82:
		type2 = 'N/A'
	
	print(num + ' ' + name)
	writer.writerow([num,name,type1,type2])
	
for number in range(86,152):
	num = str(number).zfill(3)
	url = "http://www.serebii.net/pokedex/" + num + ".shtml"
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	# To see the actual page,
	# print(soup)

	table = soup.find(bordercolor="#868686")
	rows = table.find_all('tr')

	nameRow = rows[1]
	cells = nameRow.find_all('td')
	name = cells[3].text.strip()
	
	cells = table.find_all('td')
	type1 = cells[11].text
	type1 = getType2(type1)
	type2 = cells[12].text
	type2 = getType2(type2)

	if number == 120:
		type2 = 'N/A'
		
	print(num + ' ' + name)
	writer.writerow([num,name,type1,type2])
	
# Close file
f.close()

# Show finished
print 'Done'
	
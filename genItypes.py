# This should get data for Gen I Types

# Import stuff
# This is for handling urls
import requests
# This is for structuring the web page
from bs4 import BeautifulSoup
# This is for read/write csvs
import csv

# This function pulls the data out of some text
# for 001 to 068
def getType1(text):
	info = text.split("/")
	type = info[-1][:-4].strip()
	return(type)
	
# This function pulls the data out of some text
# for 069 to 151
def getType2(text):
	info = text.split('\n')
	type = info[-2].strip()
	return(type)
	
# Open the file to write to	
f = open('C:/PandP/GenITypes/GenITypes.csv','wb')
writer = csv.writer(f)

# Write the header for the file
writer.writerow(['Number', 'Name', 'Type1', 'Type2'])

# Loop through the number to get the right webpage
# for 001 to 086, the webpage follows this structure
for number in range(1,86):
	# Fills in zeros (1 => 001)
	num = str(number).zfill(3)
	url = "http://www.serebii.net/pokedex/" + num + ".shtml"
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	# To see the actual page,
	# print(soup)

	# Grab the white-ish table in the middle of the webpage
	table = soup.find(bordercolor="#868686")
	rows = table.find_all('tr')

	# Get the first row to get the Pokemon's name
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

	# Get the cells with the types
	typeRow = rows[2]
	cells = typeRow.find_all('td')
	# Send to the right formatting function
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
	if number == 12:
		type2 = 'flying'
	# Remove Magnemite's and Magneton's Steel typing
	if number == 81 or number == 82:
		type2 = 'N/A'
	
	# I personally like 'NA' better than 'N/A'
	if type2 == 'N/A':
		type2 = 'NA'	

	# Print/write stuff out
	# I print it out because it might take a while
	# and I like to know it's working
	print(num + ' ' + name)
	writer.writerow([num,name,type1,type2])
	
# For 086 to 151, the webpage changes stucture a little
# Somehow a <tr> gets lost so using find_all('tr') for rows won't work	
for number in range(86,152):
	# Fills in zeros (1 => 001)
	num = str(number).zfill(3)
	url = "http://www.serebii.net/pokedex/" + num + ".shtml"
	page = requests.get(url)
	soup = BeautifulSoup(page.text)

	# To see the actual page,
	# print(soup)

	# Grab the white-ish table in the middle of the webpage
	table = soup.find(bordercolor="#868686")
	rows = table.find_all('tr')

	# Get the first row to get the Pokemon's name
	nameRow = rows[1]
	cells = nameRow.find_all('td')
	name = cells[3].text.strip()
	
	# The different structure changes here
	# find 'td' instead of 'tr'
	# Get the cells with the types
	# Send to the right formatting function	
	cells = table.find_all('td')
	type1 = cells[11].text
	type1 = getType2(type1)
	type2 = cells[12].text
	type2 = getType2(type2)

	# Fix mistake on Staryu, says 'N?A' instead of 'N/A'
	if number == 120:
		type2 = 'N/A'
	
	# I personally like 'NA' better than 'N/A'
	if type2 == 'N/A':
		type2 = 'NA'	
		
	# Print/write stuff out
	# I print it out because it might take a while
	# and I like to know it's working
	print(num + ' ' + name)
	writer.writerow([num,name,type1,type2])
	
# Close file
f.close()

# Show finished
print 'Done'
	
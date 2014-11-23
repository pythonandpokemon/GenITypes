# This cleans up an excel file that has
# a table with the type advantages/disadvantages

# Use pandas to read/write excel/csv
# and to handle
import pandas

# Copy/pasted into Excel from 
# http://bulbapedia.bulbagarden.net/wiki/Type/Type_chart
# Used Generation I
excelFile = pandas.ExcelFile("C:\PandP\GenITypes\genItypechart.xlsx")
table = excelFile.parse('Sheet1')
# To see the table:
# print(table)	

# To really see the table:
# print(table.values)

# Clean out the mess of the first row/column
newTable = table.ix[1:,1:]

# Reindex the columns
# Some instructions in that top right blank
types = ['Attack Down Defense Right']
# Add to new index and change unicode to ascii
for text in newTable.ix[:,0].values:
	types.append(text.encode('ascii'))
newTable.columns = types

# Function to convert weird unicode to specific numbers
def putNumbers(text):
	# I don't think this try/except is used, but there for safety
	try:
		if text == u'0\xd7':
			return 0.0
		elif text == u'1\xd7':
			return 1.0
		elif text == u'2\xd7':
			return 2.0
		elif text == u'\xbd\xd7':
			return 0.5
		else:
			return text
	except:
		return text
# Apply the function		
newTable = newTable.applymap(putNumbers)

# Print and write
print(newTable)
newTable.to_csv("C:\PandP\GenITypes\genItypechart.csv",index=False)

# Finished
print('Done')
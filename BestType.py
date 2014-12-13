# Do to:
# Go through all possible combinations to find best theoretical one
# Go through the actual ones
# Weight by attack and Defence values (need to get special and physical)

# Import stuff
import pandas 	# for dataframes/series
import numpy	# for math
import itertools# for combinations

# Read in the datasets
typeChart = pandas.read_csv('C:\PandP\GenITypes\genItypechart.csv')
# print(typeChart)

# Build empty dataframe for all the combinations of Types
# Number of different Types
nTypes = len(typeChart)
# Number of different Combos
#    Number of combinations with two different types
nCombos = (nTypes * (nTypes-1))/2
#    Plus number of single types
nCombos = nCombos + nTypes
# Build the dataframe
typeMatches = pandas.DataFrame(index=numpy.arange(nCombos),columns=['Type1','Type2'])

# Get a list of all the types
types=typeChart.ix[:,0]
# Don't forget a blank for single type Pokemon
types[15]='na'

# Fill in the DataFrame with all the combinations
count = 0
for i in itertools.combinations(types,2):
	typeMatches.ix[count] = i
	count = count+1
#print(typeMatches)

# This function gets the Average Defence for one/two types
def defenceAvg(types):
	# Get the numbers for the first type
	typeStats = typeChart[types[0]]
	# If there is a second type, get the crossproduct of the two
	if types[1] != 'na':
		typeStats = typeStats*typeChart[types[1]]
	# Return Average and Root Mean Squared Error
	Average = numpy.mean(typeStats)
	RMSE = numpy.sqrt(numpy.mean(typeStats**2))
	return(pandas.Series({'DAverage':Average,'DRMSE':RMSE}))
dStats = typeMatches.apply(defenceAvg,axis=1)
	
# Combine dStats and the different types
finalStats=pandas.merge(typeMatches,dStats,left_index=True,right_index=True)
	
# This function gets the Average Attack for one/two types	
def attackAvg(types):
	# Get the numbers for the first type
	typeStats = typeChart[typeChart.ix[:,0]==types[0]].ix[:,1:]
	# If there is a second type, get the maximum of the two
	if types[1] != 'na':
		typeStats = numpy.maximum(typeStats,typeChart[typeChart.ix[:,0]==types[1]].ix[:,1:])
	# Return Average and Root Mean Squared Error
	Average = numpy.mean(typeStats,axis=1)
	RMSE = numpy.sqrt(numpy.mean(typeStats**2,axis=1))
	return(pandas.Series({'AAverage':Average.values[0],'ARMSE':RMSE.values[0]}))
aStats = typeMatches.apply(attackAvg,axis=1)

# Combine dStats and the different types
finalStats=pandas.merge(finalStats,aStats,left_index=True,right_index=True)

# Get the Overall Average and Overall RMSE
finalStats['OAverage']=finalStats['AAverage'] - finalStats['DAverage']
finalStats['ORMSE']=numpy.sqrt(numpy.abs(finalStats['ARMSE']**2 - finalStats['DRMSE']**2))
finalStats.ix[(finalStats['AAverage']**2 - finalStats['DAverage']**2)<0,'ORMSE']=-finalStats.ix[(finalStats['AAverage']**2 - finalStats['DAverage']**2)<0,'ORMSE']

#print(finalStats)
finalStats.to_csv("C:\PandP\GenITypes\AllTypeStats.csv",index=False)

# Read in the datasets
GenITypes = pandas.read_csv('C:\PandP\GenITypes\GenITypes.csv')
# print(GenITypes)



# Look at just normal vs normal and flying
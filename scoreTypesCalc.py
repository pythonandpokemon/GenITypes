# Import stuff
import pandas 	# for dataframes/series
import numpy	# for math
import itertools# for combinations

# Make the type chart
typeChart = { 
'ATTACK DOWN DEFENSE RIGHT' : ['NORMAL', 'FIGHTING', 'FLYING', 'POISON', 'GROUND', 'ROCK', 'BUG', 'GHOST', 'FIRE', 'WATER', 'GRASS', 'ELECTRIC', 'PSYCHIC', 'ICE', 'DRAGON'], 
'NORMAL' : [1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], 
'FIGHTING' : [1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0], 
'FLYING' : [1.0, 0.5, 1.0, 1.0, 0.0, 2.0, 0.5, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0], 
'POISON' : [1.0, 0.5, 1.0, 0.5, 2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0], 
'GROUND' : [1.0, 1.0, 1.0, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 2.0, 2.0, 0.0, 1.0, 2.0, 1.0], 
'ROCK' : [0.5, 2.0, 0.5, 0.5, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0], 
'BUG' : [1.0, 0.5, 2.0, 2.0, 0.5, 2.0, 1.0, 1.0, 2.0, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0], 
'GHOST' : [0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0], 
'FIRE' : [1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 0.5, 1.0, 0.5, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0], 
'WATER' : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 2.0, 2.0, 1.0, 0.5, 1.0], 
'GRASS' : [1.0, 1.0, 2.0, 2.0, 0.5, 1.0, 2.0, 1.0, 2.0, 0.5, 0.5, 0.5, 1.0, 2.0, 1.0], 
'ELECTRIC' : [1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0], 
'PSYCHIC' : [1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 1.0], 
'ICE' : [1.0, 2.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0], 
'DRAGON' : [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0.5, 1.0, 2.0, 2.0] }
typeChart = pandas.DataFrame(typeChart)

for i in xrange(1,len(typeChart)+1):
	for j in xrange(i+1,len(typeChart)+1):
		typeChart[typeChart.columns.values[i] + "/" + typeChart.columns.values[j]] = pandas.Series(typeChart[typeChart.columns.values[i]]*typeChart[typeChart.columns.values[j]],index=typeChart.index)

# Getter for the type chart
def getTypeChart():
	return(typeChart)

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
types[15]='NA'

# Fill in the DataFrame with all the combinations
count = 0
for i in itertools.combinations(types,2):
	typeMatches.ix[count] = i
	count = count+1

# Getter for the type matches	
def getTypesList():
	return(typeMatches)

# Get the stats for Defense 	
def scoreTypesDefense(function):
	# Use this function to apply through the type matches
	# This uses the input function for the computation
	def defFunc(types):
		type1Stats = typeChart[types[0]]
		type2Stats = None
		if types[1] != 'NA':
			type2Stats = typeChart[types[1]]
		return(function(type1Stats,type2Stats))
	# Apply through and name the DataFrame
	stats = pandas.DataFrame(typeMatches.apply(defFunc,axis=1))
	stats.columns = [function.__name__]
	return stats

# Get the stats for Attack	
def scoreTypesAttack(function):
	# Use this function to apply through the type matches
	# This uses the input function for the computation
	def attFunc(types):
		type1Stats = typeChart[typeChart.ix[:,0]==types[0]].ix[:,1:].squeeze()
		type1Stats.name = types[0]
		type2Stats = None
		if types[1] != 'NA':
			type2Stats = typeChart[typeChart.ix[:,0]==types[1]].ix[:,1:].squeeze()
			type2Stats.name = types[1]
		return(function(type1Stats,type2Stats))
	# Apply through and name the DataFrame
	stats = pandas.DataFrame(typeMatches.apply(attFunc,axis=1))
	stats.columns = [function.__name__]
	return stats	

	
	
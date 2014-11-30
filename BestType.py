# Do to:
# Go through all possible combinations to find best theoretical one
# Go through the actual ones
# Weight by attack and Defence values (need to get special and physical)


# Import stuff
import pandas 	# for dataframes/series
import numpy	# for math

types = pandas.read_csv('C:\PandP\GenITypes\GenITypes.csv')
# print(types)

typeChart = pandas.read_csv('C:\PandP\GenITypes\genItypechart.csv')
# print(typeChart)

# print(types.ix[0,])

def defenseAvg(type1,type2='blank'):
	type1Stats = typeChart[type1]
	if type2 == 'blank':
		type2Stats = pandas.Series(1.0,index=type1Stats.index)
	else:
		type2Stats = typeChart[type2]
	# print(type1Stats)
	# print(type2Stats)
	
	typeStats = type1Stats*type2Stats
	Average = numpy.mean(typeStats)
	MSE = numpy.mean(typeStats**2)
	return(pandas.Series({'DAverage':Average,'DMSE':MSE}))
	
first=types.ix[5,]

def sendToDefenseAvg(row):
	if not pandas.isnull(row['Type2']):
		return(defenseAvg(row['Type1'].capitalize(),row['Type2'].capitalize()))
	else:
		return(defenseAvg(row['Type1'].capitalize()))

stats = types.apply(sendToDefenseAvg,axis=1)

print(pandas.merge(types,stats,left_index=True,right_index=True))	

# Look at just normal vs normal and flying
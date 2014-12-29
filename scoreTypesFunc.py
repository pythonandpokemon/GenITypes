# Imports
import scoreTypesCalc
import numpy
import pandas

# Baseline dataset
typeMatches = scoreTypesCalc.getTypesList()
#print(typeMatches)

# Average Defense function
def avgDef(type1Stats,type2Stats):
	stats = type1Stats
	if type2Stats is not None:
		stats = stats*type2Stats
	return(numpy.mean(stats))
	
# Use scoreTypeCalc module to get the Defense scores
statsList = scoreTypesCalc.scoreTypesDefense(avgDef)
#print(statsList)

# Merge together
finalStats=pandas.merge(typeMatches,statsList,left_index=True,right_index=True)

# Average Attack Function
def avgAtt(type1Stats,type2Stats):
	stats = type1Stats
	if type2Stats is not None:
		stats = numpy.maximum(type1Stats,type2Stats)
	return(numpy.mean(stats))

# Use scoreTypeCalc module to get the Attack scores	
statsList = scoreTypesCalc.scoreTypesAttack(avgAtt)
#print(statsList)

# Merge together
finalStats=pandas.merge(finalStats,statsList,left_index=True,right_index=True)

# Unique Defense Function
def uniDef(type1Stats,type2Stats):

	def getNum(stat):
		return {
			0 : 100,
			.25 : 75,
			.5 : 50,
			1 : 0,
			2 : -75,
			4 : -150,
			}.get(stat, 0)

	stats = type1Stats
	
	if stats.name == "BUG":
		return None
	else:
		if type2Stats is not None:
			if type2Stats.name == "BUG":
				return None
			stats = stats*type2Stats
		stats = stats.apply(getNum)
		return(numpy.mean(stats))

# Use scoreTypeCalc module to get the Defense scores
statsList = scoreTypesCalc.scoreTypesDefense(uniDef)

# Merge together
finalStats=pandas.merge(finalStats,statsList,left_index=True,right_index=True)

# Unique Attack Function
def uniAtt(type1Stats,type2Stats):

	def getNum(stat):
		return {
			0 : -100,
			.25 : -75,
			.5 : -50,
			1 : 0,
			2 : 75,
			4 : 150,
			}.get(stat, 0)

	stats = type1Stats
	
	if stats.name == "BUG":
		return None
	else:
		if type2Stats is not None:
			if type2Stats.name == "BUG":
				return None
			stats = numpy.maximum(stats,type2Stats)
		stats = stats.apply(getNum)
		return(numpy.mean(stats))

# Use scoreTypeCalc module to get the Attack scores		
statsList = scoreTypesCalc.scoreTypesAttack(uniAtt)

# Merge together
finalStats=pandas.merge(finalStats,statsList,left_index=True,right_index=True)

# Write to csv
finalStats.to_csv("C:\PandP\GenITypes\UniqueFunctionStats.csv",index=False)

# Finished
print('Done')

import scoreTypesCalc

import numpy
import pandas

typeMatches = scoreTypesCalc.getTypesList()
#print(typeMatches)

def avgDef(type1Stats,type2Stats):
	stats = type1Stats
	if type2Stats is not None:
		stats = stats*type2Stats
	return(numpy.mean(stats))
	
statsList = scoreTypesCalc.scoreTypesDefense(avgDef)
#print(statsList)

finalStats=pandas.merge(typeMatches,statsList,left_index=True,right_index=True)

def avgAtt(type1Stats,type2Stats):
	stats = type1Stats
	if type2Stats is not None:
		stats = numpy.maximum(type1Stats,type2Stats)
	return(numpy.mean(stats))

statsList = scoreTypesCalc.scoreTypesAttack(avgAtt)
#print(statsList)

finalStats=pandas.merge(finalStats,statsList,left_index=True,right_index=True)

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

statsList = scoreTypesCalc.scoreTypesDefense(uniDef)

finalStats=pandas.merge(finalStats,statsList,left_index=True,right_index=True)

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

statsList = scoreTypesCalc.scoreTypesAttack(uniAtt)

finalStats=pandas.merge(finalStats,statsList,left_index=True,right_index=True)

finalStats.to_csv("C:\PandP\GenITypes\UniqueFunctionStats.csv",index=False)

print('Done')

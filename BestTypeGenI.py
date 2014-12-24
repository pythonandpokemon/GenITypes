# Import stuff
import pandas 	# for dataframes/series
import numpy	# for math

# Read in the datasets
GenITypes = pandas.read_csv('C:\PandP\GenITypes\GenITypes.csv')
#print(GenITypes)
typeScores = pandas.read_csv("C:\PandP\GenITypes\AllTypesStats.csv")
#print(typeScores)

# Combine where Type1 matches Type1 and Type2 matches Type2 from the two sets
combined1 = pandas.merge(left=GenITypes,right=typeScores, 
	left_on=['Type1','Type2'], right_on=['Type1','Type2'], how='inner')
	
# Combine where Type1 matches Type2 and Type2 matches Type1
combined2 = pandas.merge(left=GenITypes,right=typeScores, 
	left_on=['Type1','Type2'], right_on=['Type2','Type1'], 
	how='inner', suffixes=('','_right'))
	
# Remove the extra 'Type1_right' and 'Type2_right' columns
combined2 = combined2.drop(['Type1_right','Type2_right'],axis=1)
# Combine the two sets
combined = pandas.concat([combined1,combined2])
#combined.index.names=[None]
combined.index = combined['Number']


# Flip high/low
dRanks = combined[['DAverage','DRMSE']].rank(method='min')
aRanks = combined[['AAverage','ARMSE','OAverage','ORMSE']].rank(
			method='min',ascending=False)
combined = combined.join(dRanks,rsuffix='Ranks')
combined = combined.join(aRanks,rsuffix='Ranks')
#print(typeScores)

combined.to_csv("C:\PandP\GenITypes\GenITypeStats.csv",index=False)

# Show finished
#print(combined)
print('Done')
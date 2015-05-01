import csv
import numpy
import pandas
import os
aggregatedData = []

def createOutputFile(folderName):
	return folderName

def outputPlateData(plate, folderName):
	aggregatedData.extend([[plate.Name]+t.ToTable() for t in plate.DataArray]);
	return 0



def finish(folderName):

	# read data
	dataFrame = pandas.DataFrame(aggregatedData, columns=['Plate','Coordinate','Medium','Strain']+list(range(1,49)))
	dataFrame.set_index(['Strain']);


	
	# separate by blank /nonblank	
	dataFrameNonBlanks = dataFrame.loc[(dataFrame['Strain'] != 'BLANK')]
	dataFrameNonBlanks.set_index(['Plate','Medium','Strain'])

	dataFrameBlanks = dataFrame.loc[dataFrame['Strain'] == 'BLANK']
	dataFrameBlanks.set_index(['Plate','Medium']);
	dataFrameBlanks[["Medium"]+(list(range(1,49)))].groupby(['Medium']).aggregate(['mean','std']).to_csv(os.path.join(folderName, "output_blanks.csv"), sep = '\t');

	#correct for blank by medium
	corrected = dataFrameNonBlanks.apply(correctForBlank,axis=1,args=[dataFrameBlanks])

	#select only non-mcpsm for next step
	dataFrameMedia = corrected.loc[corrected['Medium'] == 'MCPSM']
	dataFrameMedia.set_index(['Plate','Medium','Strain'])

	#correct for medium (positive test)
#	corrected = corrected.loc[corrected['Medium'] != 'MCPSM']
	corrected = corrected.apply(correctForMedium,axis=1,args=[dataFrameMedia])

	corrected.to_csv(os.path.join(folderName, "output_table.csv"),sep='\t')

	# generate aggregated by experiment file
	aggregated = corrected.groupby(['Medium','Strain']).aggregate(['mean'])
	aggregated.to_csv(os.path.join(folderName, "output_table_corr_by_strain_medium.csv"), sep='\t')


	# generate global result file
	correctedColumns = list(map(lambda x:"Cor_"+str(x), list(range(1,49))))
	posTestColumns = list(map(lambda x:"PosTest_"+str(x), list(range(1,49))))

	corrected["MaxCorOD"] = corrected[correctedColumns].max(axis=1);
	corrected["MaxPosTestOD"] = corrected[posTestColumns].max(axis=1);

	corrected[["Medium","MaxCorOD","MaxPosTestOD"]].groupby(["Medium"]).aggregate(['mean','std']).to_csv(os.path.join(folderName,"output_conclusion_by_medium.csv"), sep='\t');

	corrected[["Medium","Strain","MaxCorOD","MaxPosTestOD"]].groupby(["Strain","Medium"]).aggregate(['mean','std']).to_csv(os.path.join(folderName,"output_conclusion_by_strain_medium.csv"), sep='\t');

	corrected[["Strain","MaxCorOD","MaxPosTestOD"]].groupby(["Strain"]).aggregate(['mean','std']).to_csv(os.path.join(folderName, "output_conclusion_by_strain.csv"), sep='\t');


	
	
	

#grouped = dataFrameNonBlanks[['Strain','Medium','ODMax']].groupby(['Strain','Medium']).aggregate(['max','min','mean','std','count'])
	


	return 0

def correctForBlank(row, dataFrameBlanks):
	
	medium = row['Medium']
	
	#get corresponding blanks
	df=dataFrameBlanks.loc[(dataFrameBlanks['Medium']==medium)]
	blankMean=df[list(range(0,52))].mean()
	numBlanks = len(df.index)
	
	if numBlanks == 0:
		print("ERROR NO BLANKS FOUND FOR "+medium)
	
	#attach corrected data!
	row['NumberBlanks'] = len(df.index);

	for x in range(1,49):
		row['Blank_'+str(x)] = blankMean[x]

	for x in range(1,49):
		row['Cor_'+str(x)] = row[x]-blankMean[x]

	return row;

def correctForMedium(row, dataFrameMedia):
	strain = row['Strain']
	plate = row['Plate']
	medium = "MCPSM"

	
	
	df=dataFrameMedia.loc[(dataFrameMedia['Strain']==strain) & (dataFrameMedia['Medium']==medium)]
	correctedColumns = list(map(lambda x:"Cor_"+str(x), list(range(1,49))))
	
	mediaMean=df[["Plate","Strain"]+correctedColumns].mean()
		
	numPosTests = len(df.index)
	
	if numPosTests == 0:
		print("ERROR NO POSMEDIA FOUND FOR "+plate+"/"+strain)

	row['NumberPosTests'] = numPosTests

	for x in range(1,49):
		if(numPosTests == 0):
			row['PosTest_'+str(x)] = 0
		else:
			row['PosTest_'+str(x)] = mediaMean['Cor_'+str(x)]


	return row

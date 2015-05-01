import numpy
import re
import classPlateEntry
import classPlate
from os.path import isfile, join

def parseIndex(fStrain):
	rawDataStrain = numpy.genfromtxt(fStrain,delimiter='\t',dtype='str')
	plateName = re.search(r'(L\d*).*\.txt',fStrain).group(1)

	fMedium = fStrain.replace("STRAIN","MEDIUM")
	rawDataMedium = numpy.genfromtxt(fMedium,delimiter='\t',dtype='str')


	if rawDataStrain.shape != (9,13):
		raise NameError('Not enough entries in file ' + fStrain)

	if rawDataMedium.shape != (9,13):
		raise NameError('Not enough entries in file ' + fMedium)

	parsedPlate = classPlate.Plate()
	parsedPlate.Name = plateName
	parsedPlate.MachineType = 'L'

	for x in range(0,8): #A-H
		for y in range(0,12): #0-11
			
			entry = classPlateEntry.PlateEntry()
		
			entry.Coordinate = str(chr(x+65))+str(y+1);
			entry.Medium = rawDataMedium[x+1,y+1]
			entry.Strain = rawDataStrain[x+1,y+1].replace(" ","").replace(".","").upper()
			if(re.search(r'^(B|blank)',entry.Strain,re.IGNORECASE)):
				entry.Strain = "BLANK"

	
			#check data consistency
			if (entry.Strain != '' and entry.Medium == '')or(entry.Strain == '' and entry.Medium != ''):
				raise NameError('Data not complete in file '+fStrain+"/"+fMedium)

			#check cordinate with calculated coordinate
			if entry.Coordinate != (rawDataStrain[x+1,0]+rawDataStrain[0,y+1]):
				print(entry.Coordinate)
				raise NameError("Coordinate error in file "+fStrain)
			if entry.Coordinate != (rawDataMedium[x+1,0]+rawDataMedium[0,y+1]):
					raise NameError("Coordinate error in file "+fMedium)
			


			
			if entry.Valid():
				parsedPlate.DataArray.append(entry)



	return parsedPlate



def parsePlateData(plate, platesFolder):
	CONST_FIRST_DATA_COL = 1

	#get file
	print(plate.Name)
	rawData = numpy.genfromtxt(join(platesFolder,plate.Name+".txt"), delimiter='\t',dtype='str',deletechars=None)

	if rawData.shape != (50,98):
		raise NameError('Not enough data points in plate data:' + plate.Name);
	
	# go trough points
	for entry in plate.DataArray:

		#calc column in rawData
		firstColAsNum = ord(entry.Coordinate[0])-65;
		secondColAsNum = int(entry.Coordinate[1:])

		col = CONST_FIRST_DATA_COL+((firstColAsNum*12+secondColAsNum))
		
		#check coordinate match
		if rawData[0][col] != entry.Coordinate:
			raise NameError('Coordinate error in '+plate.Name);

		#get data
		entry.ODSeries = [float(t.replace(',','.')) for t in rawData[1:49,col].tolist()]
		
	return 0



import numpy
import re
import classPlateEntry
import classPlate
from os.path import isfile, join

CONST_NUM_PER_PLATE = 200;
CONST_FIRST_INDEX = 101

def parseIndex(f):
	rawData = numpy.genfromtxt(f, delimiter='\t',dtype='str')
	plateName = re.search(r'(H\d*).*\.txt',f).group(1)

	parsedPlate = classPlate.Plate()
	parsedPlate.Name = plateName
	parsedPlate.MachineType = 'H'

	if rawData.shape[0] != 200:
		raise NameError('Not enough entries in file ' +f)

	for i in range(CONST_FIRST_INDEX, CONST_FIRST_INDEX+CONST_NUM_PER_PLATE):

		#check if coordinate is correct
		if i != int(rawData[i-CONST_FIRST_INDEX,0]):
			raise NameError('Coordinate error in file '+f)

		entry = classPlateEntry.PlateEntry()
		entry.Coordinate = str(i)
		entry.Strain = rawData[i-CONST_FIRST_INDEX,1].replace(" ","").replace(".","").upper()

		# correct blanks
		if(re.search(r'B|blank',entry.Strain,re.IGNORECASE)):
			entry.Strain = "BLANK"

		entry.Medium = rawData[i-CONST_FIRST_INDEX,2]
		
		#check data!
		if (entry.Strain != '' and entry.Medium == '')or(entry.Strain == '' and entry.Medium != ''):
			raise NameError('Data not complete in file '+f)

		#append parsed entry
		if(entry.Valid()):
			parsedPlate.DataArray.append(entry)

	return parsedPlate



def parsePlateData(plate, platesFolder):
	CONST_FIRST_DATA_COL = 2

	#get file
	rawData = numpy.genfromtxt(join(platesFolder,plate.Name+".txt"), delimiter='\t',dtype='str')

	if rawData.shape != (49,202) and rawData.shape != (50,202):
		raise NameError('Not enough data points in plate data:' + plate.Name);
	
	# go trough points
	for entry in plate.DataArray:

		#calc column in rawData
		col = CONST_FIRST_DATA_COL+(int(entry.Coordinate)-CONST_FIRST_INDEX)
		

		#check coordinate match
		if rawData[0][col] != entry.Coordinate:
			raise NameError('Coordinate error in '+plate.Name);

		#get data
		entry.ODSeries = [float(t.replace(',','.')) for t in rawData[1:49,col].tolist()]
		

	return 0


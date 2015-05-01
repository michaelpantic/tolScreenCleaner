import csv
import re
import parseH
import parseL
import outputAdapterTable
import outputAdapterODMax
from os import listdir
from os.path import isfile, join

indexFolder = "../tolScreenCleanerData/INDEX"
platesFolder = "../tolScreenCleanerData/PLATES"
outputFolder = "../tolScreenCleanerData/OUTPUT"

# Get available index files
indexFilesH = [ join(indexFolder,f) for f in listdir(indexFolder) if isfile(join(indexFolder,f)) and re.match("H.+.txt",f)]
indexFilesL = [ join(indexFolder,f) for f in listdir(indexFolder) if isfile(join(indexFolder,f)) and re.match("L\d+_STRAIN.txt",f)]


# Parse all Indexes
plates =[];
for fileL in indexFilesL:
	plates.append(parseL.parseIndex(fileL));

for fileH in indexFilesH:
	plates.append(parseH.parseIndex(fileH));

print('Found ' + str(len(plates)) + ' different plates:')
for plate in plates:
	print ("\t",plate)

outputInfoTable = outputAdapterTable.createOutputFile(outputFolder);
outputInfoODMax = outputAdapterODMax.createOutputFile(outputFolder);

# go trough found Plates
for plate in plates:
	if plate.MachineType=='H':
		parseH.parsePlateData(plate, platesFolder)
	elif plate.MachineType=='L':
		parseL.parsePlateData(plate, platesFolder)
	else:
		raise NameError("Unknown plate type")
	
	outputAdapterTable.outputPlateData(plate,outputInfoTable);
	outputAdapterODMax.outputPlateData(plate,outputInfoODMax);


outputAdapterTable.finish(outputInfoTable)
outputAdapterODMax.finish(outputInfoODMax)


import csv

def createOutputFile(name):
	csvFile = open(name, 'w');	#not so clean (ressource deletion not possible...)
	return [csvFile, csv.writer(csvFile,delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)]

def outputPlateData(plate, outputInfo):
	csvWriter = outputInfo[1];
	rowHeader = [plate.Name, plate.MachineType]
	
	for entry in plate.DataArray:
		rowEntryHeader = [entry.Coordinate, entry.Medium, entry.Strain]
		
		row = []
		row.extend(rowHeader)
		row.extend(rowEntryHeader)
		row.extend(entry.ODSeries)


		csvWriter.writerow(row)
	outputInfo[0].flush();
	return 0

def finish(outputInfo):

	outputInfo[0].close()

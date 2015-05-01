class PlateEntry:
	def __init__(self):
		self.Coordinate = ""
		self.Medium = ""
		self.Strain = ""
		self.ODSeries = []
		
	def Valid(self):
		if self.Medium != "" and self.Strain != "":
			return 1
		else:
			return 0;

	def ToTable(self):
		attributes = [self.Coordinate, self.Medium, self.Strain]
		return attributes+self.ODSeries

	def __str__(self):
		return self.Coordinate+", "+self.Medium+", "+self.Strain+", "+str(self.Valid())+", "+str(self.ODSeries)+"\n"

	def __repr__(self):
		return self.__str__()
	

class Plate:
	def __init__(self):
		self.Name = ""
		self.MachineType = ""
		self.DataArray = []

	def __str__(self):
		return self.Name+" of type "+self.MachineType+": "+str(len(self.DataArray))+" valid items"

	def __repr__(self):
		return self.__str__()
	
	def ODMax(self):
		return max(self.DataArray)

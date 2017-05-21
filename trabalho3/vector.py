class VectorClock:
	def __init__(self, ident):
		self.identificador = ident
		self.time = { self.identificador: 0 }

	def __lt__(self, other):
		return self.time < other.time


	def __str__(self):
		return str(self.identificador + " : " + self.time)

	def add(self):
		self.time[self.identificador] += 1

	def union(self, v):
		v = list(v)
		for k, e in v.time.items():
			if not k in self.time or self.time[k] < e :
				self.time[k] = e	

	def getClocks(self):
		saida = str(list(self.time))
		return saida

#			if k in self.time :
#				if self.time[k] < e :
#					self.time[k] = e	
#			else :
#				self.time[k] = e

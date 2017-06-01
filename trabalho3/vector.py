import json

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

    def unionClocks(self, v):
        v = json.loads(v)
        for k, e in v.items():
            if not k in self.time or self.time[k] < e :
                self.time[k] = e

    def getClocks(self):
        saida = json.dumps(self.time)
        return str(saida)

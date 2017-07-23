import hashlib
import base64


class dhtkad:
    def __init__(self, ident):
        self.myHash = hashlib.sha256()
        self.myHash.update(ident)
        self.dht = {}


    def compare(other):
    	numberEquals = 0;
        for (n,m) in (other, self.myHas.digest()):
        	if (n == m) :
        		numberEquals=+1
        return numberEquals
        
	def add(host):
		hostHash = haslib.sha256()
		hostHash.update(host)
		if self.compare(hostHash.digest()) > 1 :
			if self.dht[hostHash.digest()] != NULL:
				self.dht[hostHash.digest()] = host
				return 1
		return 0

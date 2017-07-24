import hashlib
import base64

class dhtkad:
    def __init__(self, ident):
        self.myHash = hashlib.sha256()
        ident_bytes = ident.encode('utf-8')
        self.myHash.update(ident_bytes)
        self.dht = {}

    def compare(self, other):
        numberEquals = 0;
        ident =  self.myHash.hexdigest()
        for (n,m) in zip(other, ident):
            if (n == m) :
                numberEquals=+1
        return numberEquals

    def addHost(self, host):
        hostHash = hashlib.sha256()
        host_bytes = host.encode('utf-8')
        hostHash.update(host_bytes)
#        if self.compare(hostHash.hexdigest()) > 1 :
        if(not hostHash.hexdigest() in self.dht):
            self.dht[hostHash.hexdigest()] = host
        return 1

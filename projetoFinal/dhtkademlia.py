import hashlib
import base64

class dhtkad:
    def __init__(self, ident):
        self.myHash = hashlib.sha256()
        ident_bytes = ident.encode('utf-8')
        self.myHash.update(ident_bytes)
        self.peers = {}
        self.files = {}

    def compare(self, other):
        numberEquals = 0;
        ident =  self.myHash.hexdigest()
        for (n,m) in zip(other, ident):
            if (n == m) :
                numberEquals=+1
        return numberEquals

    def compareTwo(first, second):
        numberEquals = 0;
        for (n,m) in zip(first, second):
            if (n == m) :
                numberEquals=+1
        return numberEquals

    def addHost(self, host):
        hostHash = hashlib.sha256()
        host_bytes = host.encode('utf-8')
        hostHash.update(host_bytes)
        if(not hostHash.hexdigest() in self.peers):
            self.peers[hostHash.hexdigest()] = host
        return 1
        
    def addFile(self, fileName):
        fileHash = hashlib.sha256()
        fileHash.update(fileName.encode('utf-8'))
        if (self.compare(fileHash.hexdigest()) is 1):
            if(not fileHash.hexdigest() in self.files):
                self.files[fileHash.hexdigest()] = fileName
            return 1
        return 0
        
    #search for the host
    def mostLikely(self, f):
        keys = list(self.peers.keys())
        like = ''
        value = 0
        fileHash = hashlib.sha256()
        fileHash.update(f.encode('utf-8'))
        for n in keys:
            temp = self.compareTwo(fileHash.hexdigest(), n)
            if (temp > value ):
                value = temp
                like = n
        return like
        
        

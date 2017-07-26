import sys
import time
import json
import requests
from threading import Thread
from bottle import run, get, post, view, request, redirect
import bottle
from dhtkademlia import dhtkad
from urllib3.exceptions import MaxRetryError

url = "http://localhost:"
myId = sys.argv[1]
myDht = dhtkad(myId)
firstPeer = sys.argv[2]
myDht.addHost(firstPeer)
message = ""

#ServerSide
@get('/')
@view('index')
def index():
    return message
    

@post('/send')
def sendMessage():
    global nick
    m = request.forms.get('arquivo')
    r = myDht.addFile(m)
    if (r is 0):
        message = "Não foi possível inserir o arquivo, por favor insira o mesmo no servidor "
    redirect('/')

@post('/peers')
def myPeers():
	host = request.forms.get('id')
	myDht.addHost(host)
	data = json.dumps(list(myDht.dht))
	return data

def getPeersFrom(host):
    link = url + host + "/peers"
    try:
        resposta = requests.post(link, data={'id' : myId})
        if resposta.status_code == 200:
            payload=json.loads(resposta.text)
            return set(payload)
    except MaxRetryError:
        print("Conection Error, numero maximo de tentativas")
    except requests.exceptions.ConnectionError:
        print("Conection Error!")
    return set([])

def serverSide():
    while True:
        time.sleep(5)
        N = set([])
        for key in myDht.dht:
            lista = getPeersFrom(myDht.dht[key])
            if lista.difference(myDht.dht) and lista:
                N = N.union(lista.difference(myDht.dht))
                myDht.dht = myDht.dht.union(N)

#ClienteSide
@get('/file')
def getPeers():
	data = json.dumps(list(messages))
	return data

def clientSide():
	while True:
		time.sleep(5)
		N = set([])
		global messages
		for key in myDht.dht:
			resposta = getMessagesFrom(myDht.dht[key])
			if resposta.difference(messages) and resposta:
				N = N.union(resposta.difference(messages))
		messages = messages.union(N)


threadClient=Thread(None, clientSide, (), {}, None)
threadClient.start()
threadServer=Thread(None, serverSide, (), {}, None)
threadServer.start()


run(host='localhost', port=sys.argv[1])
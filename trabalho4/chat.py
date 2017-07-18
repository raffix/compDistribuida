import sys
import time
import json
import requests
from threading import Thread
from bottle import run, get, post, view, request, redirect
import bottle
import hashlib
from urllib3.exceptions import MaxRetryError

messages = set([("Nobody", "Hello!")])
nick = "Nobody"
myId = sys.argv[1]

myHash = hashlib.sha256(myId."UmSalMuitoLongoParaIssoFuncionar+-131231241231241512431251231231232")
dht = list[(myHash, myID)]

files = set(['myHash', 'Meu Id'])

#ServerSide
@get('/')
@view('index')
def index():
    return {'messages': messages, 'nick': nick}

@post('/send')
def sendMessage():
    global nick
    m = request.forms.get('message')
    nick = request.forms.get('nick')
    messages.add((nick, m))
    redirect('/')

@post('/peers')
def myPeers():
	peers.union(request.forms.get('id'))
	data = json.dumps(list(peers))
	return data

def getPeersFrom(host):
	link = "http://localhost:"+ host + "/peers"
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
		global peers
		for host in peers:
			lista = getPeersFrom(host)
			if lista.difference(peers) and lista:
				N = N.union(lista.difference(peers))
		peers = peers.union(N)

#ClienteSide
@get('/message')
def getPeers():
	data = json.dumps(list(messages))
	return data

def getMessagesFrom(host):
	link = "http://localhost:"+ host + "/message"
	try:
		resposta = requests.get(link)
		if resposta.status_code == 200:
			mensagens = json.loads(resposta.text)
			payload = set((a, b) for [a,b] in mensagens)
			return payload
	except MaxRetryError:
		print ("Conection Error, numero maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print ("Conection Error!")

	return set([])

def clientSide():
	while True:
		time.sleep(5)
		N = set([])
		global messages
		for host in peers:
			resposta = getMessagesFrom(host)
			if resposta.difference(messages) and resposta:
				N = N.union(resposta.difference(messages))
		messages = messages.union(N)


threadClient=Thread(None, clientSide, (), {}, None)
threadClient.start()
threadServer=Thread(None, serverSide, (), {}, None)
threadServer.start()


run(host='localhost', port=sys.argv[1])

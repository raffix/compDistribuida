import sys
import time
import json
import requests
from vector import VectorClock
from threading import Thread
from bottle import run, get, post, view, request, redirect
import bottle
from urllib3.exceptions import MaxRetryError

bottle.debug(True)

peers = set(sys.argv[2:])
messages = set([("Nobody", "Hello!", 0)])
	

messages.sort(key=lambda x: x[2])

nick = "Nobody"
myId = sys.argv[1]
clock = 1

#ServerSide
@get('/')
@view('index')
def index():
    return {'messages': messages, 'nick': nick}

@post('/send')
def sendMessage():
	global clock
	clock += 1 
    global nick
    m = request.forms.get('message')
    nick = request.forms.get('nick')
    messages.add((nick, m, clock))   
    redirect('/')

@post('/peers')
def myPeers():
	global clock
	clock += 1
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
	global clock
	clock += 1
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
	global clock
	clock += 1
	data = json.dumps(list(messages))
	return data

def getMessagesFrom(host):
	link = "http://localhost:"+ host + "/message"
	try:
		resposta = requests.get(link)
		if resposta.status_code == 200:
			mensagens = json.loads(resposta.text)
			payload = set((a, b, c) for [a,b,c] in mensagens)
			return payload
	except MaxRetryError:
		print ("Conection Error, numero maximo de tentativas!")
	except requests.exceptions.ConnectionError:
		print ("Conection Error!")

	return set([])

def clientSide():
	global clock
	clock += 1
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


# Relogios vetores

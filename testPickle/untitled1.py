from multiprocessing import Process, Manager
from multiprocessing.connection import Client, Listener
import pickle
import traceback
import time

class Patata():
    def __init__(self, i):
        self.p = i
        self.pa = "patatat"
        self.zapato = "zapato"

def on_message(client, userdata, msg):
    p = pickle.loads(msg.payload)
    print("Mensaje recibido")
    print(p.p)
    print(p.pa)

client = Client()
client.on_message = on_message
broker = "simba.fdi.ucm.es"
client.connect(broker)
topic = "/clients/testeandoCosas"
client.subscribe(topic)


        
    
    

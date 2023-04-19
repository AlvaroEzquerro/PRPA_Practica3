import pickle
import traceback
import time
from paho.mqtt.client import Client

class Patata():
    def __init__(self, i):
        self.p = i
        self.pa = "patata"

client = Client()
broker = "simba.fdi.ucm.es"
client.connect(broker)
topic = "/clients/testeandoCosas"

p = Patata(5)
a = input("Presiona tecla para enviar")
client.publish(topic, pickle.dumps(p))

        
    

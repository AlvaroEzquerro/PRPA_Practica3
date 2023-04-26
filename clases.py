import numpy as np
import sys, os
import socket
import pickle
import time


class Ciudad():
    def __init__(self, pos, cid, prop = None):
        self.pos = pos
        self.id = cid
        
        self.prop = prop
        self.poblacion = 20 if self.prop == None else 5
        self.nivel = 1
        self.prod = 1
        self.max_cap = 20
        
    def getPoblacion(self):
    	return int(self.poblacion)
    	
    def update(self):
        # La capacidad maxima se puede exceder si llegan refuerzos, pero a partir de ese punto, la ciudad no produce nuevos soldados
        if self.prop != None and self.poblacion < self.max_cap:
            self.poblacion += self.prod
            if self.poblacion > self.max_cap: self.poblacion = self.max_cap 

    def subirNivel(self):
        costesNivel = {2: 5, 3: 10, 4: 20, 5: 50}
        maxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200}
        prodNivel = {1:1, 2:1.5, 3:2, 4:2.4, 5:2.75}
        if self.nivel < 5 and self.poblacion > costesNivel[self.nivel+1] :
            self.nivel += 1
            # Actualizar la skin?
            self.poblacion -= costesNivel[self.nivel]
            self.prod = prodNivel[self.nivel]
            self.max_cap = maxCapNivel[self.nivel]

# Movimiento para que incluya los apoyos de un jugador a si mismo
class Movimiento():
    '''
    ciudad1: Origen
    ciudad2: Destino
    '''
    def __init__(self, ciudad1, ciudad2):
        self.c1 = ciudad1
        self.c2 = ciudad2
        self.prop = ciudad1.prop # OJO CON ESTO POR SI CAMBIA EL PROPIETARIO DE LA CIUDAD MIENTRAS EL ATAQUE ESTA LANZADO
        self.pos = ciudad1.pos
        self.direccion = np.array(ciudad2.c.pos) - np.array(ciudad1.c.pos)
        self.distancia=np.linalg.norm(self.direccion)
        self.vel = 5*self.direccion/self.distancia
        self.n_tropas = 5
        self.duracion = self.distancia/5
        self.c1.poblacion -= self.n_tropas
        

    def llegada(self):
        if self.prop == self.c2.prop:
            self.c2.poblacion += self.n_tropas
        else:
            self.c2.poblacion -= self.n_tropas
            if self.c2.poblacion < 1:
                self.c2.prop = self.c1.prop
                self.c2.poblacion *= -1
        del self

def move(movimiento):
    time.sleep(movimiento.duracion)
    movimiento.llegada()


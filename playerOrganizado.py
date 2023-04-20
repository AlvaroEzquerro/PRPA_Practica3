import traceback
import pygame
import sys, os

#DEFINIMOS LAS CLASES QUE SE MANEJAN QUE COMO SE ENVIAN DESDE LA SALA SUPONGO QUE TIENEN QUE SER LAS MISMAS QUE LAS DE LA SALA

class Player():
    def __init__(self, pid, ciudades, capital):
        self.pid = pid
        self.ciudades = ciudades
        self.capital = capital 
    
#TAMBIEN HAY QUE AÑADIR LOS METODOS DE ACTUALIZACION PERO COMO LA CLASE TIENE QUE SER IGUAL QUE EN LA SALA PARA EL PICKLE 
#PODEMOS DEFINIR ESTAS FUNCIONES DE ACTUALIZACION COMO UNA FUNCION EXTERNA

def update_jugador(player, playerAct):
    if player.pid == playerAct.pid: #Por si acaso comprobamos que tengan el mismo pid
        player.ciudades = playerAct.ciudades
        player.capital = playerAct.capital
        
#HACEMOS LO MISMO CON LAS CIUDADES
    
class Ciudad():
    def __init__(self, pos, cid, prop=None):
        self.posicion = pos
        self.id = cid
        self.propietario = prop
        self.poblacion = 20 if self.propietario == None else 5
        self.nivel = 1
        self.produccion = 1
        self.max_capacidad = 20
        
    #Metodo que actualiza la info cuando se sube de nivel
    def subirNivel(self):
        costesNivel = {2: 5, 3: 10, 4: 20, 5: 50}
        maxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200}
        prodNivel = {1:1, 2:1.5, 3:2, 4:2.4, 5:2.75}
        if self.nivel < 5 and self.poblacion > costesNivel[self.nivel+1] :
            self.nivel += 1
            self.poblacion -= costesNivel[self.nivel]
            self.prod = prodNivel[self.nivel]
            self.max_cap = maxCapNivel[self.nivel]
            
def update_ciudad(ciudad, ciudadAct):
    if ciudad.id == ciudadAct.id:
        ciudad.propietario = ciudadAct.propietario
        ciudad.poblacion = ciudadAct.poblacion
        ciudad.nivel = ciudadAct.nivel
        ciudad.produccion = ciudadAct.produccion
        ciudad.max_capacidad = ciudadAct.max_capacidad
        
#DEFINIMOS LA CLASE GAME

class Game():
    def __init__(self, pid, gameInfo): #A lo mejor es buena idea que cada jugador tenga su pid como parametro en el game
        self.gameInfo = gameInfo
        self.ciudades = gameInfo['ciudades']
        self.jugadores = gameInfo['jugadores']
        self.movimientos = gameInfo['movimientos']
        self.running = gameInfo['is_running']
        self.pid = pid
        
    def update(self, gameInfo):
        for i, c in self.ciudades:
            update_ciudad(c, gameInfo['ciudades'][i])
        for j, p in self.jugadores:
            update_jugador(p, gameInfo['jugadores'][j])
        self.running = gameInfo['is_running']
        
    def is_running(self):
        return self.running
    
    def stop(self):
        self.running = False
            
#AQUI IRIAN TODOS LOS SPRITES Y EL DISPLAY



##################################



def main():
    try:
        #conectarse
        pid, gameInfo = None, None #Aqui habria que poner que son el mensaje recibido
        print(f'I am playing as {pid}')
        game = Game(pid, gameInfo)
        #display = display(Game)
        while game.is_running():
            #Analizar eventos e ir mandando la info de lo que se teclea
            pass
    except:
        traceback.print_exc()
    finally:
        pygame.quit()
        
        
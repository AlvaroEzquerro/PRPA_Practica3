"""
Por hacer:
    Decidir como hacer los movimientos y como se elimina el sprite de este (mañana lo hablamos en clase para ver como compatibilizarlo con pygame)
    Copiar y pegar el código de Sprites aqui
    Funciones analyze_events, refresh y tick en display
            analyze_events estaria guay que tuviese un evento que al pulsar espacio, el jugador mande un ready. Cuando todos los conectados a la sala estan ready empieza la partida
"""

"""
Observaciones:
    Usamos 2 topics:
        En el topic clients/sala, solo escribe la sala y aqui es donde se envian los gameinfo y los indices de los jugadores cuando se conectan
        En el topic clients/players escriben los jugadores, con el formato (pid, evento) o "Nueva Conexion" para recibir su pid
"""

import sys, os, time, traceback, pickle, pygame
import numpy as np
from paho.mqtt.client import Client


class Player():
    def __init__(self, playerinfo):
        self.update_jugador(playerinfo)

    def update(self, playerinfo):
        if self.pid == playerinfo.pid: #Por si acaso comprobamos que tengan el mismo pid
            self.ciudades = playerinfo.ciudades

    
class Ciudad():
    def __init__(self, ciudadinfo):
        self.update_ciudad(ciudadinfo)
        self.sprite = None
            
    def update(self, ciudadinfo):
        if self.id == ciudadinfo.id:
            self.propietario = ciudadinfo.propietario
            self.poblacion = ciudadinfo.poblacion
            self.nivel = ciudadinfo.nivel
            self.produccion = ciudadinfo.produccion
            self.max_capacidad = ciudadinfo.max_capacidad
        
#DEFINIMOS LA CLASE GAME

class Game():
    def __init__(self, pid, gameInfo): #A lo mejor es buena idea que cada jugador tenga su pid como parametro en el game
        self.ciudades = gameInfo['ciudades']
        self.jugadores = gameInfo['jugadores']
        self.movimientos = gameInfo['movimientos']
        self.running = gameInfo['is_running']
        self.pid = pid
        
    def update(self, gameInfo):
        for i, c in enumerate(self.ciudades):
            c.update(gameInfo['ciudades'][i])
        for j, p in enumerate(self.jugadores):
            p.update(gameInfo['jugadores'][j])
        self.running = gameInfo['is_running']
        #Habria que definir bien como se gestionan los ataques. Quizas lo mejor sea que cada jugador tenga un almacen propio
        #con los ataques que realizar, que gameInfo solo le de la orden
        
    def is_running(self):
        return self.running
    
    def stop(self):
        self.running = False

################################
#AQUI IRIAN TODOS LOS SPRITES Y EL DISPLAY

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

FPS = 30

ANCHO_VENTANA = 900
ALTO_VENTANA = 900




class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, ventana):
        super(SpriteCiudad, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        
        imagen = pygame.image.load('PNGs/castle.png').convert_alpha()
        self.image = pygame.transform.smoothscale(imagen, (90, 90))
        
        self.rect = self.image.get_rect()
        self.rect.center = ciudad.posicion
        
     
class SpriteDato(pygame.sprite.Sprite):
    def __init__(self, ciudad, myFont, ventana, rect_ciudad):
        super(SpriteDato, self).__init__() # Para poder hacer sprites (dibujos) tienen que heredar de la clase sprite de pygame
        self.ciudad = ciudad
        self.font = myFont
        self.ventana = ventana
        
        self.image=pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.image.set_colorkey(BLACK)
        
        self.rect=rect_ciudad
        
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.render(f"Nivel {self.ciudad.nivel}", 1, BLACK)
        if self.ciudad.propietario==None:
            self.prop = self.font.render(f"{self.ciudad.propietario}", 1, BLACK)
        else:
            self.prop = self.font.render(f"J{self.ciudad.propietario+1}", 1, BLACK)
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,-15)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-20,10)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,10)))
        
    def update(self):
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, BLACK)
        self.nivel = self.font.render(f"Nivel {self.ciudad.nivel}", 1, BLACK)
        if self.ciudad.propietario==None:
            self.prop = self.font.render(f"{self.ciudad.propietario}", 1, BLACK)
        else:
            self.prop = self.font.render(f"J{self.ciudad.propietario+1}", 1, BLACK)
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,-15)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-20,10)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,10)))
        
class SpriteN_tropas(pygame.sprite.Sprite):
    def __init__(self, myFont, ventana):
        super(SpriteN_tropas, self).__init__()
        self.font = myFont
        self.ventana = ventana
        
        self.image = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.image.set_colorkey(BLACK)
        
        self.default = self.font.render("Attack mode: 5", 1, BLACK)
        self.half = self.font.render("Attack mode: 50%", 1, BLACK)
        self.full = self.font.render("Attack mode: 100%", 1, BLACK)
        self.current = self.default
        
        self.posicion=np.array((ANCHO_VENTANA*0.1, ALTO_VENTANA*0.1))
        self.ventana.blit(self.current, self.posicion+np.array((-100,0)))
        
    def update(self, mode):
        if mode == 1:
            self.current = self.default
        elif mode == 2:
            self.current = self.half
        elif mode == 3:
            self.current = self.full
        
        self.ventana.blit(self.current, self.posicion+np.array((-100,0)))
        
        
class SpriteMov(pygame.sprite.Sprite):
    def __init__(self, c1, c2, myFont, ventana, rect_final):
        super(SpriteMov, self).__init__()
        self.c1 = c1
        self.c2 = c2
        self.prop = c1.propietario # Por si queremos ponerlo de colores en funcion de quien ataque
        
        direccion = np.array(c2.posicion) - np.array(c1.posicion)
        self.vel = 50*direccion/np.linalg.norm(direccion)
        
        self.font = myFont
        self.ventana = ventana
        self.rect_final = rect_final
        
        imagen = pygame.image.load('PNGs/Ball.png').convert_alpha()
        self.image = pygame.transform.smoothscale(imagen, (40, 40))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.c1.posicion
        
        self.avance=self.vel/FPS #Avance por frame
        
    def update(self):
        self.rect.center += self.avance
        if self.rect_final.collidepoint(self.rect.center):
            self.kill()
        

class Display():
    def __init__(self, game):    
        self.jug = game.pid # Cuando se conecte, se le asigna el numero de jugador con on_connect
        self.game = game
        self.running = game.running
        
        pygame.init()
        pygame.font.init()
        
        # Definir la ventana del juego
        self.ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Times New Roman", 12)
        
        pygame.display.set_caption("Juego de Conquista")
        
        # Crear grupo de sprites para las ciudades
        self.ventana.fill(WHITE) #Rellenamos el fondo de blanco
        self.sprites_ciudades = pygame.sprite.Group()
        self.sprites_datos= pygame.sprite.Group()
        self.sprites_movimientos = pygame.sprite.Group()
        self.spriteN_tropas = SpriteN_tropas(self.font, self.ventana)
        
        for c in self.game.ciudades:
            #Se generan los sprites de las ciudades
            ciudad=SpriteCiudad(c, self.ventana)
            dato=SpriteDato(c, self.font, self.ventana, ciudad.rect)
            c.sprite = dato
            self.sprites_ciudades.add(ciudad)
            self.sprites_datos.add(dato)
            
        self.mode = 1
        '''
        mode = 1 -> Por defecto, se mandan 5
        mode = 2 -> 50%
        mode= 3 -> 100%
        '''
        pygame.display.flip()
    
    def update(self,gameinfo):
        #Se actualizan los datos de cada sprite
        self.ventana.fill(WHITE)
        self.game.update(gameinfo)
        self.sprites_datos.update()
        self.sprites_movimientos.update()
        self.spriteN_tropas.update(self.mode)

    def draw(self):
        self.sprites_ciudades.draw(self.ventana)
        self.sprites_datos.draw(self.ventana)
        self.sprites_movimientos.draw(self.ventana)

    def analyze_events(self, pos):
        '''
        'stop'->parar el programa
        (jug, cid1, cid2, mode) -> Generar movimiento
        (jug, cid1, cid1, mode) -> Subir de nivel
        '''
        events=[]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False
                events.append('quit')
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                #Deteccion de pulsacion del raton
                if pos == None:
                    pos = event.pos
                else:
                    pos2 = event.pos
                    cid1=-1
                    cid2=-1
                    for c in self.sprites_ciudades:
                        if c.rect.collidepoint(pos):
                            cid1 = c.ciudad.id
                        if c.rect.collidepoint(pos2):
                            cid2 = c.ciudad.id
                    if cid1!=-1 and cid2!=-1:
                        events.append((self.jug, cid1, cid2, self.mode))
                    pos = None
            if event.type == pygame.KEYDOWN:
                if event.unicode == '1':
                    self.mode = 1
                elif event.unicode == '2':
                    self.mode = 2
                elif event.unicode == '3':
                    self.mode = 3
                elif event.key == '8': #Tecla: Backspace (borrar)
                    pos = None
                elif event.key == pygame.K_ESCAPE:
                    events.append("quit")
                elif event.key == pygame.K_SPACE:
                    events.append((self.jug, "ready"))
        return pos, events
                

##################################


#FUNCIONES MQTT

def on_connect(client, userdata, flags, rc):
    print(f"Se ha conseguido conectar a {broker}")
    client.publish(sala, pickle.dumps("Nueva conexion"))
    
def on_message(client, userdata, msg):
    try:
        topic = msg.topic
        info = pickle.loads(msg.payload)
        if topic == new_player:
            client.unsubscribe(new_player)
            userdata["pid"] = info[0]
            userdata["gameinfo"] = info[1]
            userdata["display"] = Display(Game(userdata["pid"], userdata["gameinfo"]))
            print(userdata["display"])
            print(f"Iniciando como jugador {info[0]}")
            print("Pulsa espacio cuando estes preparado")
        else:
            userdata["gameinfo"] = info
            disp = userdata["display"]
            for c1, c2 in userdata["gameinfo"]['movimientos']:
                sprite=SpriteMov(c1, c2, disp.font, disp.ventana, c2.sprite.rect)           #rect_final no se si esta bien por que se le añade ese atributo al crear la clase
                # Esto no funciona por que en cada actualizacion con gameinfo, el sprite desaparece
                disp.sprites_movimientos.add(sprite)
            print("Informacion actualizada")        # Para testear
    except:
        # print error o lo de no se que traceback

        traceback.print_exc()
        pass

def main(broker):
    try:
        userdata = {"pid": None, "gameinfo": None, "display": None}
        client = Client(userdata = userdata)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(broker)
        client.subscribe(new_player)
        client.loop_start()
        
        display = None
        while display == None:
            display = userdata["display"]
        game = display.game
                
        pos = None
        while display.running:
            display.clock.tick(FPS)

            pos, events = display.analyze_events(pos)
            for ev in events:
                if ev == 'quit':
                    game.stop()
                    msg = ev
                elif ev[1] == "ready":
                    msg = ev
                    client.subscribe(players)
                elif ev[1] == ev[2]:
                    msg = (ev[0], "subirNivel" , ev[1])
                else:
                    msg = (ev[0], "movimiento", ev[1], ev[2], ev[3])
                client.publish(sala, pickle.dumps(msg))


            display.update(userdata["gameinfo"])
            display.draw()
            pygame.display.flip()

    except:
        traceback.print_exc()
        # Para que es esta llamada?
    finally:
        pygame.quit()
        

if __name__=="__main__":
    broker = "simba.fdi.ucm.es"
    sala = "clients/sala"
    players = "clients/players"
    new_player = "clients/new_players"
    if len(sys.argv)>1:
        broker = sys.argv[1]
    main(broker)

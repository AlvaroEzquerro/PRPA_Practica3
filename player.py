import sys, os, time, traceback, pickle, pygame
import numpy as np
from paho.mqtt.client import Client



BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

FPS = 30
velocidadMovimientos = 100
ANCHO_VENTANA = 900
ALTO_VENTANA = 900

# Primero definimos las clases para las ciudades y los jugadores que son necesarias para que pickle pueda hacer la transformacion, aunque no necesitan los mismos metodos

class Player():
    def __init__(self, playerinfo):
        self.update_jugador(playerinfo)

    def update(self, playerinfo):
        if self.pid == playerinfo.pid: #Por si acaso comprobamos que tengan el mismo pid
            self.ciudades = playerinfo.ciudades

    
class Ciudad():
    def __init__(self, ciudadinfo):
        self.update_ciudad(ciudadinfo)
            
    def update(self, ciudadinfo):
        if self.id == ciudadinfo.id:
            self.propietario = ciudadinfo.propietario
            self.poblacion = ciudadinfo.poblacion
            self.nivel = ciudadinfo.nivel
            self.produccion = ciudadinfo.produccion
            self.max_capacidad = ciudadinfo.max_capacidad
        
        
# Definimos la clase Game para que coleccione toda la informacion necesaria para el display

class Game():
    def __init__(self, pid, gameInfo): 
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
        
    def is_running(self):
        return self.running
    
    def stop(self):
        self.running = False


# Definimos los objetos que van a actuar como sprites, estos solo existen en el player.py

class SpriteCiudad(pygame.sprite.Sprite):
    def __init__(self, ciudad, ventana):
        # Hereda de la clase Sprite del modulo pygame
        super(SpriteCiudad, self).__init__()
        self.ciudad = ciudad
        
        # Escalamos la imagen del castillo
        imagen = pygame.image.load('PNGs/castle.png').convert_alpha()
        self.image = pygame.transform.smoothscale(imagen, (90, 90))
        
        self.rect = self.image.get_rect()
        self.rect.center = ciudad.posicion
        # Las ciudades no cambian durante la partida, por lo que no necesitan un update
     
class SpriteDato(pygame.sprite.Sprite):
    # Esta es la informacion en forma de texto que acompaña a cada ciudad y debe actualizarse en todo momento
    def __init__(self, ciudad, display, rect_ciudad):
        super(SpriteDato, self).__init__()
        self.ciudad = ciudad
        self.display = display
        self.font = display.font
        self.ventana = display.ventana
        
        # El color indicará si es una ciudad aliada, enemiga o propia
        if self.display.jug == self.ciudad.propietario:
            self.color = BLUE
        elif self.ciudad.propietario == None:
            self.color = BLACK
        else:
            self.color = RED
        
        self.image=pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.image.set_colorkey(BLACK)
        
        self.rect=rect_ciudad
        
        # Creamos los textos
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, self.color)
        self.nivel = self.font.render(f"Nivel {self.ciudad.nivel}", 1, self.color)
        if self.ciudad.propietario == None:
            self.prop = self.font.render(f"{self.ciudad.propietario}", 1, self.color)
        else:
            self.prop = self.font.render(f"J{self.ciudad.propietario+1}", 1, self.color)
        # Los mostramos por pantalla    
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,-15)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-20,10)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,10)))
        
    def update(self):            
        # Actualizamos los textos
        if self.display.jug == self.ciudad.propietario:
            self.color = BLUE
        elif self.ciudad.propietario == None:
            self.color = BLACK
        else:
            self.color = RED
        
        self.pob = self.font.render(f"{int(np.floor( self.ciudad.poblacion ))}", 1, self.color)
        self.nivel = self.font.render(f"Nivel {self.ciudad.nivel}", 1, self.color)
        if self.ciudad.propietario==None:
            self.prop = self.font.render(f"{self.ciudad.propietario}", 1, self.color)
        else:
            self.prop = self.font.render(f"J{self.ciudad.propietario+1}", 1, self.color)
        # Los mostramos por pantalla
        self.ventana.blit(self.pob, np.array(self.rect.bottomleft)+np.array((0,-15)))
        self.ventana.blit(self.nivel, np.array(self.rect.topright)+np.array((-20,10)))
        self.ventana.blit(self.prop, np.array(self.rect.topleft)+np.array((0,10)))
        
class SpriteN_tropas(pygame.sprite.Sprite):
    # Este texto indica el Modo de Desplazamiento seleccionado
    def __init__(self, myFont, ventana):
        super(SpriteN_tropas, self).__init__()
        self.font = pygame.font.SysFont("Times New Roman", 20)
        self.ventana = ventana
        
        self.image = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))
        self.image.set_colorkey(BLACK)
        
        self.default = self.font.render("Modo de Desplazamiento: 5", 1, BLACK)
        self.half = self.font.render("Modo de Desplazamiento: 50%", 1, BLACK)
        self.full = self.font.render("Modo de Desplazamiento: 100%", 1, BLACK)
        self.current = self.default
        
        self.posicion=np.array((ANCHO_VENTANA*0.5, ALTO_VENTANA*0))
        self.ventana.blit(self.current, self.posicion+np.array((-50,20)))
        
    def update(self, mode):
        if mode == 1:
            self.current = self.default
        elif mode == 2:
            self.current = self.half
        elif mode == 3:
            self.current = self.full
        self.ventana.blit(self.current, self.posicion+np.array((-50,20)))
        
        
class SpriteMov(pygame.sprite.Sprite):
    # Estos sprites representarán los desplazamientos en curso, asi como si son propios o de otro jugador
    # Se generan on_message y se añaden al display a traves de las ciudades de origen y destino
    def __init__(self, c1, c2, display):
        super(SpriteMov, self).__init__()
        self.c1 = c1
        self.c2 = c2
        
        self.direccion = np.array(c2.posicion) - np.array(c1.posicion)
        distancia = np.linalg.norm(self.direccion)
        self.tiempoTotal = distancia/velocidadMovimientos
        self.tiempoInicial = time.time()
        self.tiempo = 0
        
        self.display = display
        self.font = display.font
        self.ventana = display.ventana
        
        if c1.propietario == display.jug:
            archivo = 'PNGs/blueBall.png'
        else:
            archivo = 'PNGs/redBall.png'
            
        imagen = pygame.image.load(archivo).convert_alpha()
        self.image = pygame.transform.smoothscale(imagen, (40, 40))
        
        self.rect = self.image.get_rect()
        self.rect.center = self.c1.posicion

        
    def update(self):
        # Recalcula su posicion en funcion del tiempo y cuando este acaba, elimina el sprite para que no consuma recursos
        self.tiempo = (time.time()- self.tiempoInicial)/self.tiempoTotal
        self.rect.center = np.array(self.c1.posicion) + self.tiempo*self.direccion
        if self.tiempo > 1:
            self.kill()
        

class Display():
    # Esta es la clase principal encargada de ejecutar todo el codigo de pygame
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
        self.background = pygame.image.load("PNGs/mapa.png")
        #self.background = pygame.transform.smoothscale(self.background, (ANCHO_VENTANA, ALTO_VENTANA))
        self.sprites_ciudades = pygame.sprite.Group()
        self.sprites_datos= pygame.sprite.Group()
        self.sprites_movimientos = pygame.sprite.Group()
        self.spriteN_tropas = SpriteN_tropas(self.font, self.ventana)
        
        for c in self.game.ciudades:
            #Se generan los sprites de las ciudades y los datos de estas
            ciudad = SpriteCiudad(c, self.ventana)
            dato = SpriteDato(c, self, ciudad.rect)
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
        self.ventana.blit(self.background, (0, 0))
        
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
                        pos, pos2 = None, None
                    elif cid1 == -1:
                        pos = pos2
                    else:
                        pos, pos2 = None, None
            if event.type == pygame.KEYDOWN:
                if event.unicode == '1':
                    self.mode = 1
                elif event.unicode == '2':
                    self.mode = 2
                elif event.unicode == '3':
                    self.mode = 3
                elif event.key == '8': #Tecla: Backspace (borrar accion anterior, tambien puede hacerse pulsando en un espacio en blanco)
                    pos = None
                elif event.key == pygame.K_ESCAPE:
                    events.append("quit")
                elif event.key == pygame.K_SPACE:
                    events.append((self.jug, "ready"))
        return pos, events
                


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
            print(f"Iniciando como jugador {info[0]+1}")
            print("Pulsa espacio cuando estes preparado")
        else:
            if info == 'terminado':
                userdata['display'].running = False
            else:
                userdata["gameinfo"] = info
                disp = userdata["display"]
                # Añadimos los movimientos aqui por que estos solo aparecerán una vez en el gameinfo, y si la sala actualizase el gameinfo 2 veces antes de que el display lo añadiese, desaparecerian estos sprites
                for c1, c2 in userdata["gameinfo"]["movimientos"]:
                    sprite = SpriteMov(c1, c2, disp)
                    disp.sprites_movimientos.add(sprite)
    except:
        print("Ha habido un error")
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
                    display.running = False
                    msg = ev
                # ev[0] es el id del jugador que ejecuta la accion
                elif ev[1] == "ready":
                    msg = ev
                    client.subscribe(players)
                # ev[1] y ev[2] son las ciudades sobre las que ha pulsado el jugador
                elif ev[1] == ev[2]:
                    msg = (ev[0], "subirNivel" , ev[1])
                # ev[3] es el modo de desplazamiento seleccionado
                else:
                    msg = (ev[0], "movimiento", ev[1], ev[2], ev[3])
                client.publish(sala, pickle.dumps(msg))
                
            display.update(userdata["gameinfo"])
            display.draw()
            pygame.display.flip()

    except:
        print("Ha habido un error")
        traceback.print_exc()
    finally:
        print('El juego ha terminado')
        pygame.quit()
        

if __name__=="__main__":
    broker = "simba.fdi.ucm.es"
    sala = "clients/conquista/sala"
    players = "clients/conquista/players"
    new_player = "clients/conquista/new_players"
    if len(sys.argv)>1:
        broker = sys.argv[1]
    main(broker)

from multiprocessing import Process, Manager, Value, Lockimport tracebackfrom paho.mqtt.client import Clientimport numpy as npimport timeimport pickle, sys, randomPOSICIONES = [(125, 100), (150,300), (100,550), (200, 750), (400,200), (375, 550), (700, 75), (800, 225), (610, 399), (775, 640), (500, 800)] #Posiciones de las ciudadesrandom.shuffle(POSICIONES) #Hacemos que la distribución de las posiciones sea aleatoria en cada partidacostesNivel = {2: 10, 3: 20, 4: 50, 5: 100} #Costes para subir de nivelmaxCapNivel = {1: 20, 2: 50, 3: 100, 4:150, 5: 200} #Capacidad maxima de poblacion en cada nivelprodNivel = {1:1, 2:2, 3:2.75, 4:3.5, 5:4} #Poblacion que se producen en cada nivelmodosAtaque = {1: 0, 2: 50, 3:100} #Modos de ataque en los que varía la población envviada al ataquevelocidadMovimientos = 100 #Velocidad a la que se mueven los sprites de los ataquespobInicialJug = 5 #Poblacion con la que empieza la ciudad de cada jugadorpobInicialLibre = 10 #Poblacion con la que empieza cada ciudad sin propietarioFPS = 30#DEFINIMOS LAS CLASES DE LA SALAclass Ciudad():    def __init__(self, pos, cid, prop=None):        self.posicion = pos        self.id = cid        self.propietario = prop        self.nivel = 1        self.poblacion = pobInicialJug if self.propietario != None else pobInicialLibre        self.max_capacidad = maxCapNivel[self.nivel]        self.produccion = prodNivel[self.nivel]/FPS    def subirNivel(self): #Método para hacer que la ciudad suba de nivel        if self.nivel < 5 and self.poblacion >= costesNivel[self.nivel+1] :             self.nivel += 1            self.poblacion -= costesNivel[self.nivel]            self.produccion = prodNivel[self.nivel]/FPS            self.max_capacidad = maxCapNivel[self.nivel]        def update(self): #Método para actualizar la información de cada ciudad durante el juego        # La capacidad maxima se puede exceder si llegan refuerzos, pero a partir de ese punto, la ciudad no produce nuevos soldados        if self.propietario != None and self.poblacion < self.max_capacidad:            self.poblacion += self.produccion            if self.poblacion > self.max_capacidad: self.poblacion = self.max_capacidad    def __repr__(self):        return f"Posicion: {self.posicion}, id: {self.id}, propietario: {self.propietario}, nivel: {self.nivel}, poblacion: {self.poblacion}"        class Player():    def __init__(self, pid, ciudades):         self.pid = pid        self.ciudades = ciudades    def __repr__(self):        return f"Numero de jugador: {self.pid}, ciudades: {self.ciudades}"class Game(): #Clase que gestiona toda la información del juego    def __init__(self, gameinfo, cambios):        self.jugadores = gameinfo['jugadores']        self.ciudades = gameinfo['ciudades']        self.movimientos = gameinfo['movimientos']        self.running = gameinfo['is_running']        self.lock = Lock()                          # Esta clase actúa como un monitor que asegura la concurrencia        self.cambios = cambios            def is_running(self):        return self.running        def stop(self):        self.running =  False        def movimiento(self, c1, c2, mode): #Método que gestiona los ataques que se producen        with self.lock:            porcTropas = modosAtaque[mode]/100            if porcTropas != 0:                n_tropas = (c1.poblacion * porcTropas)            else:                if c1.poblacion <=5:                    n_tropas = c1.poblacion                else:                    n_tropas = 5            c1.poblacion -= n_tropas            self.movimientos.append((c1,c2))            p = Process(target = proc_movimientos,  args = (c1,c2,n_tropas, self.cambios, self.lock))            p.start()                   def subirNivel(self, ciudad): #Método para indicar cuando una ciudad debe subir de nivel        with self.lock:            ciudad.subirNivel()    def cambiarPropietario(self, ciudad, nuevoPropietario): #Método para indicar que se debe cambiar el propietario de una ciudad porque haya sido conquistada        with self.lock:            ciudad.propietario = nuevoPropietario    def update(self): #Método para actualizar toda la información del juego según lo que vaya ocurriendo en la partida        with self.lock:            for jug, cid, n in list(self.cambios):                c2 = self.ciudades[cid]                if c2.propietario == jug:                    c2.poblacion += n                else:                    c2.poblacion -= n                     if c2.poblacion <= 0:          #Si conquista la ciudad se le quita al otro y se la queda el atacante                        if c2.propietario != None:                            enemigo = c2.propietario                            self.jugadores[enemigo].ciudades.remove(c2)                        (self.jugadores[jug].ciudades).append(c2)                        c2.propietario = jug                        c2.poblacion *= -1                self.cambios.pop()            for ciudad in self.ciudades:                ciudad.update()        def get_info(self): #Método para recopilar toda la información del juego y enviársela a los jugadores        with self.lock:            gameinfo = {'ciudades': self.ciudades, 'jugadores': self.jugadores, 'movimientos': self.movimientos, 'is_running': self.running}        return gameinfo    def terminado(self): #Método para avisar de cuando termina el juego, es decir, cuando un jugador conquista todas las ciudades        with self.lock:            prop = self.ciudades[0].propietario            for ciudad in self.ciudades:                if ciudad.propietario != prop or ciudad.propietario == None:                    return False        return True#Esta función es la que se da a los procesos en self.movimientos para coordinar la ejecución de los sprites de cada jugador y la información que gestiona la saladef proc_movimientos(ciudad1, ciudad2, n_tropas, cambios, lock):    distancia = np.linalg.norm( np.array(ciudad2.posicion) - np.array(ciudad1.posicion) )    tiempo = distancia/velocidadMovimientos    time.sleep(tiempo)    with lock:        cambios.append((ciudad1.propietario,ciudad2.id, n_tropas))        #FUNCIONES MQTTdef on_connect(client, userdata, flags, rc):    print(f"Se ha conseguido conectar a {broker}")    print("Esperando a que se conecten los jugadores ...")def on_message(client, userdata, msg): #Función que gestiona cada uno de los mensajes que se reciben de los jugadores    info = pickle.loads(msg.payload)    try:            if info == "Nueva conexion" and not(userdata["start"]):            n = userdata["num_jug"]            ciudad_n = userdata["game"].ciudades[n]            userdata["num_jug"] += 1            ciudad_n.poblacion = pobInicialJug            userdata["game"].cambiarPropietario(ciudad_n, n)            userdata["game"].jugadores.append(Player(n,[ciudad_n]))            client.publish(new_player, pickle.dumps( (n, userdata["game"].get_info() )) )                    elif info == "quit":            userdata["game"].running = False                    elif info[1] == "ready" and not(userdata["start"]):            userdata["readys"].add(info[0])            userdata["start"] = (( userdata["num_jug"] == len(userdata["readys"]) ) and userdata["num_jug"] > 0 )                    elif info[1] == "subirNivel" and userdata["start"]:            ciudad = userdata["game"].ciudades[info[2]]                        if ciudad.propietario == info[0]:                userdata["game"].subirNivel(ciudad)                    elif info[1] == "movimiento" and userdata["start"]:            ciudad1 = userdata["game"].ciudades[info[2]]                       ciudad2 = userdata["game"].ciudades[info[3]]                       mode = info[4]            if ciudad1.propietario == info[0]:                userdata["game"].movimiento(ciudad1, ciudad2, mode)                except:        print("Ha habido un error")        traceback.print_exc()    finally:        pass    #FUNCIÓN PRINCIPALdef main(broker):    try:        # Generamos el juego        m = Manager()        cambios = m.list()        ciudades = [Ciudad(POSICIONES[i], i) for i in range(len(POSICIONES))] #Lista con todas las ciudades del tablero        gameinfo = {'ciudades': ciudades, 'jugadores': [], 'movimientos': [], 'is_running': True} #Declaramos el gameInfo        game = Game(gameinfo, cambios) #Creamos el juego                #Parte MQTT                userdata = {"game": game, "num_jug":0, "readys":set(), "start":False}        client = Client(userdata = userdata)        client.on_connect = on_connect        client.on_message = on_message        client.connect(broker)        client.subscribe(sala)        client.loop_start()                while game.running and not game.terminado(): #Bucle para el funcinamiento del juego            tiempo_inicio = time.time()            if userdata["start"]:                game.update()                             gameinfo = game.get_info()                client.publish(players, pickle.dumps(gameinfo))                game.movimientos =  []            tiempo_bucle = time.time()-tiempo_inicio            time.sleep( max(0, 1/FPS - tiempo_bucle))        game.running = False        msg = 'terminado'        client.publish(players, pickle.dumps(msg))           except:        print("Ha habido un error")        traceback.print_exc()    finally:        print('El juego ha terminado')    if __name__=="__main__":    broker = "simba.fdi.ucm.es"    sala = "clients/conquista/sala"    players = "clients/conquista/players"    new_player = "clients/conquista/new_players"    if len(sys.argv)>1:        broker = sys.argv[1]    main(broker)
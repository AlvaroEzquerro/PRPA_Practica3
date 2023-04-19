from Clases import *

ciu= Ciudad(POSICIONES[0], 0)
ciu=[ciu]
binar=pickle.dumps(ciu)
print(binar)
hola=pickle.loads(binar)
print(hola)
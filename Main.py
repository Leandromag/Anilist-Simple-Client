from modules import Ventana
from modules import AnilistReq

import time as reloj
import threading




miventana = Ventana.Gtkwindow()
proceso = threading.Thread(target=miventana.iniciar)
proceso.daemon = True
proceso.start()


reloj.sleep(3)


milista = AnilistReq.AnilistaRequest()
lista = milista.obtenerLista()

for elem in lista:
	miventana.agregarlabel(elem)


miventana.abrir()
reloj.sleep(15)

miventana.cerrar()
reloj.sleep(2)


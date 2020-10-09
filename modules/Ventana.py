import gi
import time as reloj
import os
import json
from modules import AnilistReq
from threading import Timer
import threading

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository.GdkPixbuf import Pixbuf
from gi.repository import Gio

class GtkInterface():

	def __init__(self):


		if(os.path.isfile('modules/data/user_data')):
			self.iniciarCliente()
		else:
			self.iniciarInterfaceRegistro()


	def iniciarCliente(self):
		builder = Gtk.Builder()
		builder.add_from_file("modules/GTKStructure/ventanaCliente.glade") #creo la interface Gtk

		self.listbo = builder.get_object("listbo")
		self.listbo2 = builder.get_object("listbo2")

		anilistApi = AnilistReq.AnilistaRequest()
		anilistApi.actualizar()
		lista_anime_emision=anilistApi.obtenerListaEnEmision()
		lista_anime_offseason=anilistApi.obtenerListaOffSeason()
		datos_usr=anilistApi.obtenerDatosdeUsuario()


		imgdata=anilistApi.obtenerAvatar()   #data byte img
		input_stream = Gio.MemoryInputStream.new_from_data(imgdata, None)
		pixbuf = Pixbuf.new_from_stream(input_stream, None)
		self.gtkimag = builder.get_object("avatar")
		self.gtkimag.set_from_pixbuf(pixbuf)


		self.labelprofilename = builder.get_object("labelprofilename")
		self.labelprofilename.set_text(datos_usr['profilename'])

		self.scrollwin = builder.get_object("scrollwindow")
		self.scrollwin.set_name("scrollwin")
		self.scrollwin = builder.get_object("scrollwindow2")
		self.scrollwin.set_name("scrollwin2")

		corrimientovent=135

		labelvistos = builder.get_object("total_cont")
		labelvistos.set_text(str(datos_usr['vistos']))
		labelepi = builder.get_object("episodios_cont")
		labelepi.set_text(str(datos_usr['episodios']))
		labeldias = builder.get_object("dias_cont")
		labeldias.set_text(str(datos_usr['dias']))
		labelsig = builder.get_object("siguiendo")
		labelsig.set_text(str(len(lista_anime_emision)))
		labelvie = builder.get_object("viendo")
		labelvie.set_text(str(len(lista_anime_offseason)))


		for elem in lista_anime_offseason:

			input_stream = Gio.MemoryInputStream.new_from_data(elem['coverimg'], None)
			pixbuf = Pixbuf.new_from_stream(input_stream, None)
			gtkimag = Gtk.Image()
			gtkimag.set_from_pixbuf(pixbuf)

			contenedorenlista = Gtk.Fixed()

			contenedorenlista.put(gtkimag,20,0)

			titulo_content = Gtk.Label()
			titulo_content.set_text(elem['titulo'])
			titulo_content.set_name("labelama")

			contenedorenlista.put(titulo_content,0+corrimientovent,0)

			temporada = Gtk.Label()
			temporada.set_text("Temporada:")

			temporada_content = Gtk.Label()
			temporada_content.set_text(elem['temporada']+" "+str(elem['anio']))
			temporada_content.set_name("labelblue")

			contenedorenlista.put(temporada,0+corrimientovent,20)
			contenedorenlista.put(temporada_content,85+corrimientovent,20)


			progreso = Gtk.Label()
			progreso.set_text("Progreso:")

			progreso_content = Gtk.Label()
			progreso_content.set_text("["+str(elem['progreso'])+"/"+str(elem['totepisodios'])+"]")
			progreso_content.set_name("labelverd")

			contenedorenlista.put(progreso,0+corrimientovent,40)
			contenedorenlista.put(progreso_content,80+corrimientovent,40)


			self.listbo2.add(contenedorenlista)

		for elem in lista_anime_emision:

			input_stream = Gio.MemoryInputStream.new_from_data(elem['coverimg'], None)
			pixbuf = Pixbuf.new_from_stream(input_stream, None)
			gtkimag = Gtk.Image()
			gtkimag.set_from_pixbuf(pixbuf)

			contenedorenlista = Gtk.Fixed()

			contenedorenlista.put(gtkimag,20,0)

			titulo = Gtk.Label()

			titulo_content = Gtk.Label()
			titulo_content.set_text(elem['titulo'])
			titulo_content.set_name("labelama")

			contenedorenlista.put(titulo_content,0+corrimientovent,0)


			temporada = Gtk.Label()
			temporada.set_text("Temporada:")

			temporada_content = Gtk.Label()
			temporada_content.set_text(elem['temporada']+" "+str(elem['anio']))
			temporada_content.set_name("labelblue")

			contenedorenlista.put(temporada,0+corrimientovent,20)
			contenedorenlista.put(temporada_content,85+corrimientovent,20)


			progreso = Gtk.Label()
			progreso.set_text("Progreso:")

			progreso_content = Gtk.Label()
			progreso_content.set_text("["+str(elem['progreso'])+"/"+str(elem['totepisodios'])+"]")
			progreso_content.set_name("labelverd")

			contenedorenlista.put(progreso,0+corrimientovent,40)
			contenedorenlista.put(progreso_content,80+corrimientovent,40)


			proximo = Gtk.Label()
			proximo.set_text("Episodio")

			proximo_content = Gtk.Label()
			proximo_content.set_text(str(elem['capitulo']))
			proximo_content.set_name("labelros")

			contenedorenlista.put(proximo,0+corrimientovent,60)
			contenedorenlista.put(proximo_content,65+corrimientovent,60)

			largo=len(str(elem['capitulo']))
			corrimiento=0+(10*(largo-1))
			proximo2 = Gtk.Label()
			proximo2.set_text("sale en")

			proximo_content2 = Gtk.Label()
			proximo_content2.set_text(elem['tiemposalida'])
			proximo_content2.set_name("labelros")

			contenedorenlista.put(proximo2,80+corrimiento+corrimientovent,60)
			contenedorenlista.put(proximo_content2,135+corrimiento+corrimientovent,60)

			self.listbo.add(contenedorenlista)


		self.cargarcss()
		self.window = builder.get_object("window") #muestro la ventana
		self.window.set_name("ventana")
		self.window.connect("destroy",self.cerrarGTK)
		self.window.show_all()
		self.iniciar()

	'''--------------	metodos relacionados a el cliente ------------------------------------'''









	'''--------------	metodos relacionados a la interface de registro principal ---------------'''

	def crearJsonData(self,id):
		data = {'userId':id}
		with open('modules/data/user_data', 'w') as outfile:
			json.dump(data,outfile)

	def spinn(self):
		self.revelador.set_reveal_child(False)
		self.spinnercargando.start()
		self.window.show_all()

	def reqid(self,userid):
		anilistApi = AnilistReq.AnilistaRequest()
		id=anilistApi.obtenerId(userid)
		if(id != 'none'):
			self.spinnercargando.stop()
			self.labelreveler.set_text("¡Encontrado!")
			self.revelador.set_reveal_child(True)
			reloj.sleep(1)
			self.revelador.set_reveal_child(False)
			reloj.sleep(2)
			self.crearJsonData(id)
			Gtk.main_quit()
			self.iniciarCliente()
		else:
			self.spinnercargando.stop()
			self.revelador.set_reveal_child(True)
			reloj.sleep(1)
			self.revelador.set_reveal_child(False)
			reloj.sleep(1)

	def guardarid(self,event):
		self.userid = self.entry.get_text()
		proceso = threading.Thread(target=self.spinn)
		proceso.daemon = True
		proceso.start()

		proceso2 = threading.Thread(target=self.reqid,args=(self.userid,))
		proceso2.start()


	def iniciarInterfaceRegistro(self):
		builder = Gtk.Builder()
		builder.add_from_file("modules/GTKStructure/ventanaRegistro.glade") #creo la interface Gtk

		self.closebutton = builder.get_object("closebutton")	#activo evento cerrar ventana
		self.closebutton.connect('clicked',self.cerrarGTK)

		self.selectbutton = builder.get_object("selectbutton")	#activo evento click select
		self.selectbutton.connect('clicked',self.guardarid)

		self.entry = builder.get_object("entry")
		self.spinnercargando = builder.get_object("cargando")
		self.revelador = builder.get_object("reveler")
		self.labelreveler = builder.get_object("labelreveler")

		self.window = builder.get_object("window") #muestro la ventana
		self.window.show_all()

		self.iniciar()

	'''----------------------------------------------------------------------------------------'''
	def cargarcss(self):
		css = b"""

		#labelama {
			color: #fff179;
		}
		#labelverd {
			color: #6aff4c;
		}
		#labelblue {
			color: #4da6ef;
		}
		#labelred {
			color: #f44336;
		}
		#labelros {
			color:#ff86d9;
		}
		#ventana {
			background-color: #19212d;
		}
		#scrollwin {
			border-top-width:0px;
			border-bottom-width:0px;
			background-color: #111721;
		}
		#scrollwin2 {
			border-top-width:0px;
			border-bottom-width:0px;
			background-color: #111721;
			margin-right:20px;
		}
		"""

		self.css_provider = Gtk.CssProvider()
		self.css_provider.load_from_data(css)
		self.context = Gtk.StyleContext()
		self.screen = Gdk.Screen.get_default()
		self.context.add_provider_for_screen(self.screen, self.css_provider,  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

	def cerrarGTK(self,event):
		Gtk.main_quit()

	def iniciar(self):									#iniciar GTK
		Gtk.main()

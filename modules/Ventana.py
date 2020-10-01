import cairo
import gi
import time as reloj
from threading import Timer

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk
from gi.repository import Gdk



class Gtkwindow(Gtk.Window):
	def __init__(self):
	
	
		Gtk.Window.__init__(self)
		self.set_size_request(360, 420)
		self.set_default_size(360, 420)
		
		
		
		self.connect('destroy', Gtk.main_quit)
		self.connect('draw', self.draw)
		self.connect ('button-press-event',self.destruirevent)
		self.set_decorated(False)		#cambiar para debugear ventana
		self.set_app_paintable(True)
		self.set_gravity(Gdk.Gravity.NORTH_EAST)
		screen = self.get_screen()
		
		tam=screen.get_width()
		tam-=360
		self.move(tam, 45) #766 border screen
		
		
		visual = screen.get_rgba_visual()
		if visual and screen.is_composited():
			self.set_visual(visual)
		
			
		"""   WIDGETS AGREGADOS A LA VENTANA   """
		
		
		self.revealer = Gtk.Revealer(name="titlebar-revealer-pv")
		self.revealer.set_transition_duration(1000)
		self.revealer.set_transition_type(Gtk.RevealerTransitionType(1))

		
		
		self.contenedor = Gtk.Fixed()
		self.box = Gtk.ListBox()
		self.box.set_name("listbox")
		self.revealer.add(self.box)
		
		
		self.contenedor.put(self.revealer,0,0)
		
		
		#self.box.pack_start(self.label2,True,True,1)
		
		

		# the scrolledwindow
		#self.scrolled_window = Gtk.ScrolledWindow()
		# there is always the scrollbar (otherwise: AUTOMATIC - only if needed- or NEVER)
		#self.scrolled_window.set_policy(Gtk.PolicyType.ALWAYS, Gtk.PolicyType.ALWAYS)
		# add the image to the scrolledwindow
		#self.scrolled_window.add_with_viewport(self.ficontain)
		# add the scrolledwindow to the window
		#self.add(self.scrolled_window)
		#self.add(ficontain)
		"""    Fin declaracion widgets    """
		self.add(self.contenedor)
		self.cargarcss()
		self.show_all()
		
		
	def iniciar(self):									#iniciar GTK
		Gtk.main()
		 
		   	   
	def terminar(self):
		self.destroy()
	def destruirevent(self,btn,event):
		self.destroy()
		
	def draw(self, widget, context):					#dibuja fondo transparente
		context.set_source_rgba(0, 0, 0, 0)
		context.set_operator(cairo.OPERATOR_SOURCE)
		context.paint()
		context.set_operator(cairo.OPERATOR_OVER)
	
	
	def cerrar(self):									#CERRAR VENTANA
		self.revealer.set_reveal_child(False)
		reloj.sleep(1.5)
		self.show_all()
		
	
	def abrir(self):     	#ABRIR VENTANA							
		self.revealer.set_reveal_child(True)


	def agregarlabel(self, tecsto):

		self.label3 = Gtk.Label()
		self.label3.set_text(tecsto)
		self.label3.set_name("label")
		
		self.box.add(self.label3)
		self.box.show_all()
		
		
	def cargarcss(self):
		css = b"""
		
		#label {
			margin-bottom: 10px;
			background-color: #161717;
			color: #5aff70;
		}

		#listbox {
		
			background-color:black;
		}
		"""
		
		self.css_provider = Gtk.CssProvider()
		self.css_provider.load_from_data(css)
		self.context = Gtk.StyleContext()
		self.screen = Gdk.Screen.get_default()
		self.context.add_provider_for_screen(self.screen, self.css_provider,  Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	



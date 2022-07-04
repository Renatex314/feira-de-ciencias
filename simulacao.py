from kivy.app 				import App
from kivy.uix.widget 		import Widget
from kivy.uix.label 		import Label
from kivy.lang 				import Builder
from kivy.clock 			import Clock
from kivy.properties 		import NumericProperty, StringProperty
from math 					import asin, sin, cos
import time

Builder.load_string(open("gui.kv", encoding="utf-8").read(), rulesonly=True)

class Portalb (Widget):
	pass

class Portalo (Widget):
	pass

class midplatform(Widget):
	pass

class Portais (Widget):

	clkblue = None
	canb = True
	cano = True
	
	def on_touch_down(self, touch):
		if (self.portalb.collide_point(touch.pos[0], touch.pos[1])):
			self.clkblue = True
		elif (self.portalo.collide_point(touch.pos[0], touch.pos[1])):
			self.clkblue = False

	def on_touch_move(self, touch):
		if (self.clkblue == True):
			self.portalb.center = touch.pos[0], touch.pos[1]
		elif (self.clkblue == False):
			self.portalo.center = touch.pos[0], touch.pos[1]

	def on_touch_up(self):
		self.clkblue = None

class Info (Widget):

	def resetar(self, bola, resettempo):
		bola.y = self.height / 2
		bola.x = (self.width * 5)/2
		bola.vx = 0
		bola.vyi = 0
		resettempo()

	def show_plataforma(self, plataforma, width):
		if (plataforma.x != 5):
			plataforma.x = 5
		else:
			plataforma.x = width

	def portals(self, portal, bola):
		if (portal.enabled == True):
			portal.portalo.x = 5000
			portal.portalb.x = 5000
			portal.enabled = False
			self.bola.arrowvis = 1
		else:
			portal.portalo.x = portal.width / 8
			portal.portalb.x = 500
			portal.enabled = True
			self.bola.arrowvis = 0
			
	def speedlight(self, bola):
		bola.vx = 300000
		
	def shide(self):
		if (self.btshide.text == "esconder"):
			self.box.x = 5000
			self.btshide.text = "mostrar"
			self.salfa = 0
		else:
			self.box.pos = self.pos
			self.btshide.text = "esconder"
			self.salfa = 0.5

	def hide_arrow(self, bola):
		if (self.btarrowhide.text == "esconder seta"):
			bola.arrowvis = 0
			self.btarrowhide.text = "mostrar seta"
		else:
			self.btarrowhide.text = "esconder seta"
			bola.arrowvis = 1
	
class Plataforma (Widget):
	pass

class Ball (Widget):

	vx = NumericProperty(0)
	vg = NumericProperty(0)
	vyi = NumericProperty(0)
	r = NumericProperty(1)
	g = NumericProperty(1)
	b = NumericProperty(1)
	direction = NumericProperty(0)
	arrowsize = NumericProperty(100)
	arrowvis = NumericProperty(1)
	imagevelo = StringProperty("drawables/velocity.png")
	canmove = True
	limitvel = False

	def mover(self, gravidade, width, height, tempo):
		self.g = (abs((-gravidade * tempo  + self.vyi))/20 + abs(self.vx))/2
		self.b = (abs((-gravidade * tempo  + self.vyi))/20 + abs(self.vx))/2
		self.vg = (-gravidade * tempo  + self.vyi)
		if (self.canmove):
			self.x += self.vx
			if (self.limitvel == False):
				self.y += (-gravidade * tempo  + self.vyi)
			elif (-gravidade < 0):
				self.y += -23
			elif (-gravidade > 0):
				self.y += 23
			if (self.right >= width or self.x <= 0):
				if (self.right > width):
					self.right = width
				if (self.x < 0):
					self.x = 0
				self.vx *= -1

		self.hipot = (abs(self.vx**2) + abs(self.vg**2))**0.5
		if (self.vg > 0):
			self.direc = -asin(abs(self.vx)/self.hipot)*180/3.14
		elif (self.vg < 0):
			self.direc = -((asin(abs(self.vg)/self.hipot)*180/3.14) + 90)
		else:
			self.direc = 0
		if (self.vx < 0):
			self.direc *= -1
			self.imagevelo = "drawables/velocityturned.png"
		else:
			self.imagevelo = "drawables/velocity.png"
		if (self.hipot < 5):
			self.arrowsize = 100 + 50 * self.hipot/5
		else:
			self.arrowsize = 150
		self.direction = self.direc

class Play (Widget):
	colidindo = False
	cronometer = None
	tempo = NumericProperty(time.time())
	#scale = 1.28/0.01
	scale = 0.01/0.01
	dy = 0
	dx = 0

	def resettempo(self):
		self.tempo = time.time()
	
	def on_touch_down(self, touch):
		self.info.on_touch_down(touch)
		self.portais.on_touch_down(touch)
		if (self.bola.collide_point(touch.pos[0], touch.pos[1])):
			self.colidindo = True
			self.cronometer = time.time()
			self.bola.canmove = False

	def on_touch_move(self, touch):
		self.portais.on_touch_move(touch)
		if (self.colidindo):
			self.dy = touch.pos[1] - self.bola.center[1]
			self.dx = touch.pos[0] - self.bola.center[0]
			self.bola.center = touch.pos
			if (self.cronometer + 0.05 <= time.time() - self.cronometer):
				self.cronometer = time.time()

	def on_touch_up(self, touch):
		self.portais.on_touch_up()
		if (self.colidindo):
			tempo = time.time() - self.cronometer
			self.bola.vyi = self.dy/tempo
			self.bola.vx = self.dx/tempo
			self.bola.canmove = True
			self.colidindo = False
			self.cronometer = None
			self.bola.limitvel = False
			self.tempo = time.time()

	def move_ball(self, nsei):
		if (self.info.ginput.text != "" and self.info.ginput.text != "-" and len(self.info.cinput.text) >= 3 and self.info.cinput.text != ""):
			self.bola.mover(float(self.info.ginput.text), self.width, self.height, (time.time() - self.tempo) * self.scale)
			if (self.bola.y <= self.height/10):
				self.bola.y = self.height/10
				self.bola.vx *= 0.99
				self.bola.limitvel = False
				self.bola.vyi = ((-float(self.info.ginput.text) * ((time.time() - self.tempo) * self.scale)  + self.bola.vyi) ) * -float(self.info.cinput.text)
				self.tempo = time.time()
			if (self.plataforma.x == 5 and self.bola.top >= self.height - self.height/10):
				self.bola.top = self.height - self.height/10
				self.bola.vx *= 0.99
				self.bola.limitvel = False
				self.bola.vyi = ((-float(self.info.ginput.text) * ((time.time() - self.tempo) * self.scale)  + self.bola.vyi)) * -float(self.info.cinput.text)
				self.tempo = time.time()
			if (self.bola.collide_widget(self.portais.portalo) and self.portais.cano and self.bola.top < self.portais.portalo.top 
				and self.bola.y > self.portais.portalo.y and self.bola.x > self.portais.portalo.x and self.bola.right < self.portais.portalo.right):
				self.portais.canb = False
				self.bola.center = self.portais.portalb.center
				if (abs((-float(self.info.ginput.text) * ((time.time() - self.tempo) * self.scale)  + self.bola.vyi)) > 18 and float(self.info.ginput.text) != 0):
					if (float(self.info.ginput.text) < 0):
						self.tempo = time.time() + (15 - self.bola.vyi)/(float(self.info.ginput.text) * self.scale)
					else:
						self.tempo = time.time() + (-15 - self.bola.vyi)/(float(self.info.ginput.text) * self.scale)
			elif (not self.bola.collide_widget(self.portais.portalo)):
				self.portais.cano = True
			if (self.bola.collide_widget(self.portais.portalb) and self.portais.canb and self.bola.top < self.portais.portalb.top 
				and self.bola.y > self.portais.portalb.y and self.bola.x > self.portais.portalb.x and self.bola.right < self.portais.portalb.right):
				self.portais.cano = False
				self.bola.center = self.portais.portalo.center
				if (abs((-float(self.info.ginput.text) * ((time.time() - self.tempo) * self.scale)  + self.bola.vyi)) > 18 and float(self.info.ginput.text) != 0):
					if (float(self.info.ginput.text) < 0):
						self.tempo = time.time() + ((15 - self.bola.vyi)/float(self.info.ginput.text) * self.scale)
					else:
						self.tempo = time.time() + (-15 - self.bola.vyi)/(float(self.info.ginput.text) * self.scale)
			elif (not self.bola.collide_widget(self.portais.portalb)):
				self.portais.canb = True
			self.info.txvel.text = "velocidade: " + str(int(self.bola.hipot)) + " m/s"
		self.info.txcoef.text = "coef. de restituição: \n" + self.info.cinput.text
		self.info.txgr.text = "gravidade:\n" + self.info.ginput.text + " m/s²"

class Main (App):

	def build(self):
		engine = Play()
		Clock.schedule_interval(engine.move_ball, 1.0 / 60.0)
		return engine

Main().run()
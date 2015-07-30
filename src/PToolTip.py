import pgui.src.PLabel as PLabel
import pgui.src.PTimer as PTimer
from .putil import *
import blf

class new(PLabel.new):
	def __init__(self, text="", timeout=2.0, fontfile="", font_size=12):
		PLabel.new.__init__(self, [0, 0, 100, 20], text, fontfile, font_size, 0)
		self.timeOut = timeout
		
		self._timer = PTimer.new() 
		
		self.visible = False
		
	def show(self, x, y):
		self.bounds[0] = x
		self.bounds[1] = y
		self._timer.reset()
		self.visible = True
	
	def update(self):
		dim = self.text_size()
		self.bounds[2] = dim[0]+4
		self.bounds[3] = dim[1]+4
		
		self._timer.update()
		
		if self._timer.time >= self.timeOut:
			self.visible = False
			
		self.zorder = 99999
		PLabel.new.update(self)
		
	def draw(self):
		if not self.visible: return
		
		h_draw_flat_frame(self.bounds, self.backColor)
		
		PLabel.new.draw(self)
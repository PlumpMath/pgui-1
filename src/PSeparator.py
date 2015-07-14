import pgui.src.PControl as PControl
from .putil import *
# Orientation
ORI_VERTICAL = 3
ORI_HORIZONTAL = 6

class new(PControl.new):
	def __init__(self, bounds=[0, 0, 100, 12]):
		PControl.new.__init__(self, bounds=bounds)
		
		self.orientation = ORI_HORIZONTAL
		
		self.drawSelection = False
	def draw(self):
		if self.orientation == ORI_HORIZONTAL:
			h_draw_3d_line_hor(self.bounds[0], self.bounds[1],
							   self.bounds[0]+self.bounds[2], self.bounds[1], self.backColor)
		else:
			h_draw_3d_line_ver(self.bounds[0], self.bounds[1], self.bounds[0], self.bounds[1]+self.bounds[3], self.backColor)
		
		PControl.new.draw(self)
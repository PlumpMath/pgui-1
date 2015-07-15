from .putil import *

class new:
	def __init__(self):
		self.bounds = [0, 0, 100, 100]
		self.padding = [4, 4, 4, 4]
		self.fit = False
		
		self._prevs = 0
		
	def apply_layout(self, control, count):
		if control.layout_order >= count-1:
			self._prevs = 0 
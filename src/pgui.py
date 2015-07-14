from bge import logic
import pgui.src.PManager as PManager

logic.handled = False
logic.current_focus = None

class new:
	
	def __init__(self):
		self._active = -1
		self.managers = []
	
	def newManager(self):
		pm = PManager.new()
		pm.index = len(self.managers)+1
		i = len(self.managers)
		self.managers.append(pm)
		return self.managers[i]
	
	def eventLoop(self):
		if self._active > -1 and self._active < len(self.managers):
			self.managers[self._active].update()
	
	@property
	def activeManager(self):
		return self._active
	
	@activeManager.setter
	def activeManager(self, v):
		self._active = v
		if v < 0: return
		if v > len(self.managers)-1: return		
		self.managers[v].bind()
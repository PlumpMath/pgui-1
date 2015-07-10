from .putil import *
from .pthemes import *
import pgui.src.PControl as PControl

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 25]):
        PControl.new.__init__(self, bounds)
        self.on_value_change = None
        
        self._min = 0
        self._max = 100
        self._value = 0
        
        self.step = 1
        
        self.bar = [0, 0, 200, 25]
        
        self.value = 50
        
    def performStep(self):
        self.value += self.step if self.step > 0 else 1
    
    def update(self):
        if not self.enabled: return
        
        vx = 1+((self.min+self.value) / self.max) * (self.bounds[2]-2)
            
        self.bar = [self.bounds[0]+1, self.bounds[1]+1, vx, self.bounds[3]-2]
        
        PControl.new.update(self)
    
    def draw(self):
        PControl.new.draw(self)
        
        if self.theme == None:
            h_draw_frame_d(self.bounds, default["control"], type=2)
            h_draw_frame_d(self.bar, default["button_hover"], type=1)
        else:
            bar = self.theme["bar"]
            pnl = self.theme["panel"]
            h_draw_9patch_skin(pnl, self.bounds)
            h_draw_9patch_skin(bar, self.bar)
    
    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, val):
        if val <= self._min:
            val = self._min+1
        self._max = val
    
    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, val):
        if val >= self._max:
            val = self._max-1
        self._min = val
            
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if val < self._min:
            val = self._min
        if val > self._max:
            val = self._max
        
        if val != self._value:
            fire_if_possible(self.on_value_change, self, val)
                
        self._value = val

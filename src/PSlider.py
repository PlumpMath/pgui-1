import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

# This control is currently kinda buggy...
# I would like some help to fix it, because I'm literally done with it :P
class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 18]):
        PControl.new.__init__(self, bounds)
        
        self._min = 0
        self._max = 100
        self._value = 0
        
        self.knob_bounds = [bounds[0]+12,bounds[1],12,18]
        self.track = []
        
        self.on_value_change = None
    
        self.drag = False
        
        self.ex1 = 0
        self.ex2 = 0
        
        self.khover = False
        self.ksize = 0
    def onClick(self, x, y, btn):
        if btn == events.LEFTMOUSE:
            if haspoint(self.knob_bounds, x, y):
                self.drag = True
                self.ex1 = self.ex2 = x                
    
    def onRelease(self, x, y, btn):
        self.drag = False
    
    def onDrag(self, x, y, b):
        if haspoint(self.knob_bounds, x, y):
            self.khover = True
        else:
            self.khover = False
        
        if self.drag:            
            self.ex1 = x
            dx = self.ex1 - self.ex2
            self.value += int(dx)
            self.ex2 = self.ex1
    
    def update(self):
        if not self.enabled: return
        
        ty = self.bounds[3]/2-2
        self.ksize = (self.bounds[3]-5)/2
        self.track = [self.bounds[0]+self.ksize, self.bounds[1]+ty, self.bounds[2]-self.ksize*2, 4]
        
        vx = (self.bounds[0]-self.track[0])+((self.min+self.value)/self.max) * self.track[2]
        vy = self.ksize/2
        
        self.knob_bounds[0] = self.track[0]+vx
        self.knob_bounds[1] = self.bounds[1]+vy-2
        
        PControl.new.update(self)
    
    def draw(self):
        PControl.new.draw(self)
        
        tbnds = self.knob_bounds
        
        if self.theme == None:
            h_draw_frame(self.track, default["control"], 2)        
            h_draw_frame(self.knob_bounds, default["control"], 1)  
        else:
            pnl = self.theme["panel"]
            kn = self.theme["track_normal"]
            kh = self.theme["track_hover"]
            kc = self.theme["track_click"]
            knb = kn
            
            if not self.khover and not self.clicked:
                knb = kn               
            elif self.khover and not self.clicked:
                knb = kh
            elif self.khover and self.clicked:
                knb = kc
            else:
                knb = kc
            
            h_draw_ninepatch(pnl["image"].id, pnl["image"].size[0], pnl["image"].size[1], self.track, pnl["padding"])
            h_draw_9patch_skin(knb, tbnds)
        
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

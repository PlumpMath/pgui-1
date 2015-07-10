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
        
        self.khover = False
        self.ksize = 0
        
    def onMouseClick(self, data):
        if data["button"] == events.LEFTMOUSE:
            self.drag = True
            self.onMouseMove(data)
    
    def onMouseRelease(self, mouse_data):
        self.drag = False
    
    def onMouseMove(self, data):
        if self.drag:
            kx = ((self.knob_bounds[0]+self.knob_bounds[2]/2)-self.bounds[0])
            dx = abs(data["x"]-kx)
            if data["x"] > kx:
                self.value += dx
            elif data["x"] < kx:
                self.value -= dx

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
            
            h_draw_9patch_skin(pnl, self.track)
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

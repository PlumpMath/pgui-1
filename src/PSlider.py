import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

# This control is currently kinda buggy...
# I would like some help to fix it, because I'm literally done with it :P
class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 20]):
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
        
        self._values = {}
        
    def onMouseClick(self, data):
        if data["button"] == events.LEFTMOUSE:
            self.drag = True
            self.onMouseMove(data)
    
    def onMouseRelease(self, mouse_data):
        self.drag = False
    
    def __snap_val(self, val):
        vals = 0
        for v, pos in self._values:
            if val == v:
                vals = pos
            else:
                vals = val
        return vals
    
    def onMouseMove(self, data):
        if self.drag:
            kx, ky = self.worldPos
            for v, pos in self._values.items():
                px = self.track[0]+pos
                b = [self.track[0]+pos, self.knob_bounds[1], self.track[2]/len(self._values), self.bounds[3]]
                if haspoint(b, kx, ky):
                    self.value = v
                    # print(v)
                    break

    def update(self):
        if not self.enabled: return
        
        ty = self.bounds[3]/2-2
        self.ksize = self.knob_bounds[2]
        self.track = [self.bounds[0]+self.ksize, self.bounds[1]+ty, self.bounds[2]-self.ksize*2, 4]
        
        self._values = {}
        range_ = self.max-self.min
        emin = self.min-range_ if abs(self.min) > 0 else self.min
        emax = self.max-range_ if abs(self.min) > 0 else self.max
        
        for i in range(range_+1):            
            self._values[i+self.min] = ((i+emin)/emax) * self.track[2]
        
        # print(self._values)
        
        vy = (self.ksize/2)-1
        ky = self.knob_bounds[3]/2
        
        val_norm = self.value-self.min
        vx = ((val_norm+emin)/emax) * self.track[2]
        vx -= vy
        
        self.knob_bounds[0] = self.track[0]+vx
        self.knob_bounds[1] = (self.bounds[1]+self.bounds[3]/2)-ky
        
        PControl.new.update(self)
    
    def draw(self):
        PControl.new.draw(self)
        
        tbnds = self.knob_bounds
        
        if self.theme == None:
            h_draw_frame_d(self.track, default["control"], 2)        
            h_draw_frame_d(self.knob_bounds, default["control"], 1)
            
           # for v, pos in self._values.items():
           #      h_draw_quad_wire([self.track[0]+pos, self.knob_bounds[1], self.track[2]/len(self._values), self.bounds[3]])
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
        
        # Convert to int
        tval = val
        if isinstance(val, str) or isinstance(val, float):
            tval = int(val)
        
        self._value = tval

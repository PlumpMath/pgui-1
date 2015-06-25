import pgui.src.PControl as PControl
import pgui.src.PButton as PButton
from .putil import *
from .pthemes import *

# This control is currently kinda buggy...
# I would like some help to fix it, because I'm literally done with it :P
class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 12]):
        PControl.new.__init__(self, bounds)
        
        self._value = 0
        self._max = 100
        self._min = 0
        
        self.addb = PButton.new(text="", text_align=1)
        self.decb = PButton.new(text="", text_align=1)
        
        _this = self
        def addf(s, x, y, b):
            _this.value += 1
        def decf(s, x, y, b):
            _this.value -= 1
        self.addb.on_click = addf
        self.decb.on_click = decf
        
        self.knob_bounds = []
        
        self.drag = False
    
        self.ex1 = 0
        self.ex2 = 0
    
        self.xpos = 0
        self.on_value_change = None
        
    def onClick(self, x, y, btn):
        if btn == events.LEFTMOUSE:
            if haspoint(self.knob_bounds, x, y):
                self.drag = True
                self.ex1 = self.ex2 = x
    
    def onRelease(self, x, y, btn):
        self.drag = False
    
    def onDrag(self, x, y, b):
        if self.drag:
            self.ex1 = x
            dx = self.ex2 - self.ex1

            self.value -= int(dx)
            
            self.ex2 = self.ex1
    
    def update(self):
        self.decb.bounds = [self.bounds[0], self.bounds[1], self.bounds[3], self.bounds[3]]
        self.addb.bounds = [(self.bounds[0]+self.bounds[2])-self.bounds[3], self.bounds[1], self.bounds[3], self.bounds[3]]
        
        innerb = [self.bounds[0]+self.bounds[3], self.bounds[1], self.bounds[2]-self.bounds[3], self.bounds[3]]
        vw = innerb[3]
        
        w = innerb[2] - (vw * 2)+3
        vx = ((self.min+self.value) / self.max) * w
        
        self.xpos = vx
        self.knob_bounds = [vx+innerb[0], self.bounds[1], vw, self.bounds[3]]
    
        self.decb.theme = self.addb.theme = self.theme
        
        self.decb.update()
        self.addb.update()
        
        PControl.new.update(self)
        
    def draw(self):
        PControl.new.draw(self)
        
        if not self.visible: return
        sp_bounds = [self.bounds[0]+self.bounds[3], self.bounds[1], self.bounds[2]-self.bounds[3]*2, self.bounds[3]]
        
        if self.theme == None:
            h_draw_quad(sp_bounds, default["control_dark"])
            bgl.glColor4f(*default["control_dark"])
            h_draw_quad_wire(sp_bounds)
        else:
            t = self.theme["panel_dark"]
            h_draw_9patch_skin(t, sp_bounds)

        self.decb.draw()
        self.addb.draw()
        
        h_draw_arrow_2(self.addb.bounds[0]+self.bounds[2]/2, self.addb.bounds[1]+self.addb.bounds[3]/2, 4, True, color=self.foreColor)
        h_draw_arrow_2(self.decb.bounds[0]+self.bounds[2]/2, self.decb.bounds[1]+self.decb.bounds[3]/2, 4, False, color=self.foreColor)
        
        if self.theme == None:
            if not self.drag:
                h_draw_frame(self.knob_bounds, default["control"], 1)
            else:
                h_draw_frame(self.knob_bounds, default["control"], 2)
        else:
            tn = self.theme["button_normal"]
            tc = self.theme["button_click"]
            t = tn
            
            if self.drag:
                t = tc
            else:
                t = tn
            
            h_draw_9patch_skin(t, self.knob_bounds)
    
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

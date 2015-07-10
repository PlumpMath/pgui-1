import pgui.src.PButton as PButton
import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *
from bge import render

# needs fix
class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 12]):
        PControl.new.__init__(self, bounds)
    
        self._value = 0
        self._oldvalue = 0
        self._max = 100
        self._min = 0
        
        self.addb = PButton.new(text="", text_align=1)
        self.decb = PButton.new(text="", text_align=1)
        
        def addf(s, d):
            self.value -= 1
        def decf(s, d):
            self.value += 1
            
        self.addb.on_mouse_click = addf
        self.decb.on_mouse_click = decf
        
        self.knob_bounds = []
        self.innerb = []
        
        self.drag = False
        
        self.ypos = 0
        self.on_value_change = None
    
    def onMouseHold(self, d):
        if d["button"] == events.LEFTMOUSE:
            x, y = self.worldPos
            if haspoint(self.innerb, x, y):
                self.drag = True
    
    def onMouseRelease(self, d):
        self.drag = False
    
    def onMouseMove(self, d):
        if self.drag:
            ky = ((self.knob_bounds[1]+self.knob_bounds[3]/2)-self.bounds[3])
            dy = abs(d["y"]-ky)
            if d["y"] > ky:
                self.value += dy
            elif d["y"] < ky:
                self.value -= dy

    def update(self):        
        self.decb.bounds = [self.bounds[0], (self.bounds[1]+self.bounds[3])-self.bounds[2], self.bounds[2], self.bounds[2]]
        self.addb.bounds = [self.bounds[0], self.bounds[1], self.bounds[2], self.bounds[2]]
        
        self.innerb = [self.bounds[0], self.bounds[1]+self.bounds[2], self.bounds[2], self.bounds[3]-self.bounds[2]]

        vw = self.innerb[2]
        
        h = self.innerb[3] - (vw+self.bounds[2])
        vy = ((self.min+self.value) / self.max) * h
        
        self.ypos = vy
        self.knob_bounds = [self.bounds[0], vy+self.innerb[1], self.bounds[2], vw]
    
        self.decb.theme = self.addb.theme = self.theme
        
        self.decb.update()
        self.addb.update()
        
        PControl.new.update(self)
        
    def draw(self):
        if not self.visible: return
        if self.bounds[3] < self.bounds[2]*4: return
        PControl.new.draw(self)
        
        sp_bounds = [self.bounds[0], self.bounds[1]+self.bounds[2], self.bounds[2], self.bounds[3]-self.bounds[2]]
        
        if self.theme == None:
            h_draw_quad(sp_bounds, default["control_dark"])
            bgl.glColor4f(*default["control_dark"])
            h_draw_quad_wire(sp_bounds)
        else:
            t = self.theme["panel_dark"]
            h_draw_9patch_skin(t, sp_bounds)

        self.decb.draw()
        self.addb.draw()
        
        h_draw_arrow(self.addb.bounds[0]+self.bounds[2]/2, self.addb.bounds[1]+self.addb.bounds[3]/2, 4, True, color=self.foreColor)
        h_draw_arrow(self.decb.bounds[0]+self.bounds[2]/2, self.decb.bounds[1]+self.decb.bounds[3]/2, 4, False, color=self.foreColor)
        
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
                
        self._oldvalue = self._value
        self._value = val

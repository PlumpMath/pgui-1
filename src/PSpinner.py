import pgui.src.PButton as PButton
import pgui.src.PLabel as PLabel
import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *
import blf

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 20], fontfile="", font_size=12):
        PControl.new.__init__(self, bounds)
        
        self.fid = blf.load(fontfile) if fontfile != "" else 0
        self.fontSize = font_size
        
        self._value = 0
        self._max = 100.0
        self._min = 0.0
        
        self.decimalPlaces = 0
        self.increment = 1
        
        self.addb = PButton.new(text="", fontfile=fontfile, text_align=1)
        self.decb = PButton.new(text="", fontfile=fontfile, text_align=1)
        
        _this = self
        def addf(s, d):
            _this.value += self.increment
        def decf(s, d):
            _this.value -= self.increment
        self.addb.on_mouse_click = addf
        self.decb.on_mouse_click = decf
    
        self.on_value_change = None
        
        self.backColor = default["text_background"]
        
    @property
    def max(self):
        return self._max
    
    @max.setter
    def max(self, val):
        if val <= self._min:
            val = self._min+self.increment
        self._max = val
    
    @property
    def min(self):
        return self._min
    
    @min.setter
    def min(self, val):
        if val >= self._max:
            val = self._max-self.increment
        self._min = val
            
    @property
    def value(self):
        return round(self._value, self.decimalPlaces)
    
    @value.setter
    def value(self, val):
        if val < self._min:
            val = self._min
        if val > self._max:
            val = self._max
        
        if val != self._value:
            fire_if_possible(self.on_value_change, self, round(val, self.decimalPlaces))
        
        self._value = val
    
    def update(self):
        self.addb.bounds = [(self.bounds[0]+self.bounds[2])-16, self.bounds[1], 16, self.bounds[3]/2]
        self.decb.bounds = [(self.bounds[0]+self.bounds[2])-16, self.bounds[1]+self.bounds[3]/2, 16, self.bounds[3]/2]
    
        self.decb.update()
        self.addb.update()
    
        self.decb.theme = self.addb.theme = self.theme
        
        PControl.new.update(self)
        
    def draw(self):
        if not self.visible: return
        PControl.new.draw(self)
        
        sp_bounds = [self.bounds[0], self.bounds[1], self.bounds[2]-16, self.bounds[3]]
        
        if self.theme == None:
            h_draw_quad_b(sp_bounds, self.backColor, 2)
        else:
            p = self.theme["panel_down"]
            h_draw_9patch_skin(p, sp_bounds)
        
        val = str(self.value)
        h_draw_text(self.fid, val, sp_bounds, self.foreColor, margin=0, font_size=self.fontSize, text_align=1, vertical_align=1, shadow=False)
        
        self.decb.draw()
        self.addb.draw()
        
        h_draw_arrow(self.decb.bounds[0]+self.decb.bounds[2]/2, self.decb.bounds[1]+self.decb.bounds[3]/2, 4, False, color=self.foreColor)
        h_draw_arrow(self.addb.bounds[0]+self.addb.bounds[2]/2, self.addb.bounds[1]+self.addb.bounds[3]/2, 4, True, color=self.foreColor)
        
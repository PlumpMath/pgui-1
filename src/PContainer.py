import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100]):
        PControl.new.__init__(self, bounds)        
        self._controls = {}
        self.border = 1        
        self.zorder = -9999
        
    @property
    def controls(self):
        return self._controls
    
    @controls.setter
    def controls(self, ctrl):
        self._controls = ctrl
        for k, c in self._controls.items():
            c.name = k
            c.parent = self
                    
        u_sort_post_draw(self)
    
    def draw(self):
        PControl.new.draw(self)
        
        if self.theme == None:
            h_draw_frame(self.bounds, self.backColor, self.border)
        else:
            t = self.theme["panel"]              
            h_draw_ninepatch(t["image"].id, t["image"].size[0], t["image"].size[1], self.bounds, t["padding"])

        for c, v in self._controls.items():
            v.draw()
            
    def update(self):
        for c, v in self._controls.items():
            v.foreColor = self.foreColor
            if v.theme == None:
                v.theme = self.theme
            v.update()
        
        PControl.new.update(self)

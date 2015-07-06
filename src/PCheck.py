import pgui.src.PLabel as PLabel
from .putil import *
from .pthemes import *

class new(PLabel.new):
    def __init__(self, bounds=[0, 0, 100, 100], text="", fontfile="", font_size=12, text_align=0):
        PLabel.new.__init__(self, bounds, text, fontfile, font_size, text_align)
        self._checked = True
        
        self.on_check = None
        
        self.backColor = (1,1,1,1)
    
    @property
    def checked(self):
        return self._checked
    
    @checked.setter
    def checked(self, v):
        if v != self._checked:
            fire_if_possible(self.on_check, self, v)
        self._checked = v
    
    def onMouseClick(self, d):
        if d["button"] == events.LEFTMOUSE:
            self.checked = not self.checked
    
    def draw(self):
        PControl.new.draw(self)
        if not self.visible: return
        tbnds = [self.bounds[0]+2, self.bounds[1]+(self.bounds[3]/2-7), 14, 14]
        
        if self.theme == None:
            h_draw_quad_b(tbnds, self.backColor, 2)
            if self.checked:
                h_draw_tick(tbnds[0]+7, tbnds[1]+7, 17, default["button_hover"])
        else:
            cun = self.theme["check_u_normal"]
            cuh = self.theme["check_u_hover"]
            cuc = self.theme["check_u_click"]
            cn = self.theme["check_normal"]
            ch = self.theme["check_hover"]
            cc = self.theme["check_click"]
            t = cun
            if not self.hovered and not self.clicked:
                if self.checked:
                    t = cn
                else:
                    t = cun
            elif self.hovered and not self.clicked:
                if self.checked:
                    t = ch
                else:
                    t = cuh
            elif self.hovered and self.clicked:
                if self.checked:
                    t = cc
                else:
                    t = cuc
            else:
                if self.checked:
                    t = cc
                else:
                    t = cuc
                
            h_draw_ninepatch(t["image"].id, t["image"].size[0], t["image"].size[1], tbnds, t["padding"])
        
        self.margin = 20
        PLabel.new.draw(self)

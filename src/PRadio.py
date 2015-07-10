import pgui.src.PLabel as PLabel
import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

class new(PLabel.new):
    def __init__(self, bounds=[0, 0, 100, 100], text="", fontfile="", font_size=12, text_align=0):
        PLabel.new.__init__(self, bounds, text, fontfile, font_size, text_align)
        self._checked = False
        self.group = None
        
        self.on_check = None
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
            if self.group == None:
                self.checked = not self.checked # Act like a CheckBox
            else:
                if self.group.previous != None:
                    self.group.previous.checked = False
                self.checked = True
                self.group.previous = self
    
    def draw(self):
        if not self.visible: return
        PControl.new.draw(self)
        
        tbnds = [self.bounds[0]+2, self.bounds[1]+(self.bounds[3]/2-7), 14, 14]
        if self.theme == None:
            h_draw_circle_d(tbnds[0]+7, tbnds[1]+7, 7, default["control"], type=1)                
            if self.checked:
                h_draw_circle(tbnds[0]+7, tbnds[1]+7, 4, default["button_hover"])
        else:
            cun = self.theme["radio_u_normal"]
            cuh = self.theme["radio_u_hover"]
            cuc = self.theme["radio_u_click"]
            cn = self.theme["radio_normal"]
            ch = self.theme["radio_hover"]
            cc = self.theme["radio_click"]
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

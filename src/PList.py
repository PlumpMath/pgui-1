import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *
import blf

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100], fontname=""):
        PControl.new.__init__(self, bounds)        
        self.items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7"]        
        self._ibounds = {}    
        self.fid = blf.load(fontname) if fontname != "" else 0        
        self.itemHeight = 16
        
        self.on_selected = None
        self.on_draw_item = None
        
        self.backColor = default["text_background"]
        
        self._selected = -1
                
    @property
    def selectedIndex(self):
        return self._selected
    
    @selectedIndex.setter
    def selectedIndex(self, i):
        self._selected = i
        fire_if_possible(self.on_selected, self)
        
    def onMouseClick(self, d):
        if d["button"] == events.LEFTMOUSE:
            for k, v in self._ibounds.items():                
                if haspoint(v, self.worldPos[0], self.worldPos[1]):
                    self.selectedIndex = k

    def update(self):
        howmanyitems = int(self.bounds[3] / self.itemHeight)
        
        for i in range(len(self.items)):
            ih = self.itemHeight * i
            
            self._ibounds[i] = [self.bounds[0]+1, self.bounds[1]+ih+1, self.bounds[2]-2, self.itemHeight]
        
        PControl.new.update(self)
        
    def draw(self):
        if not self.visible: return
        PControl.new.draw(self)
        
        if self.theme == None:
            h_draw_quad_b(self.bounds, self.backColor, 2)
        else:
            t = self.theme["panel"]
            h_draw_9patch_skin(t, self.bounds)
        
        for i in range(len(self.items)):
            li = self.items[i]
            istr = str(li)
            
            bnds = self._ibounds[i]
                        
            if bnds[1]+bnds[3] > self.bounds[1]+self.bounds[3] or bnds[1] < self.bounds[1]:
                continue
            
            tcol = default["text_dark"]
            
            if self.on_draw_item == None:                
                if self.selectedIndex == i:
                    if self.theme == None:
                        h_draw_frame_d(bnds, default["button_hover"], 0)
                    else:
                        tm = self.theme["select"]
                        h_draw_9patch_skin(tm, bnds)
                    tcol = default["text_dark"]
                else:
                    tcol = self.foreColor
                h_draw_text(self.fid, istr, bnds, tcol, margin=0, font_size=12, text_align=0, vertical_align=1, shadow=False)
            else:
                itm = {"selected": self.selectedIndex == i, "index": i, "bounds": bnds}
                self.on_draw_item(self, itm)

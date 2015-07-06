import pgui.src.PControl as PControl
import pgui.src.PVScroll as PVScroll
from .putil import *
from .pthemes import *
import blf

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 1, 1], fontname=""):
        PControl.new.__init__(self, bounds)        
        self.items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5", "Item 6", "Item 7"]        
        self._ibounds = {}        
        self.selectedIndex = -1    
        self._scroll = PVScroll.new(bounds=[bounds[0]+bounds[2]-12, bounds[1], 12, bounds[3]])        
        self.fid = blf.load(fontname) if fontname != "" else 0        
        self.itemHeight = 16
        
        self.on_selected = None
        self.on_draw_item = None
        
        self.backColor = default["text_background"]
        
    def onMouseClick(self, d):
        if d["button"] == events.LEFTMOUSE:
            for k, v in self._ibounds.items():                
                if haspoint(v, self.worldPos[0], self.worldPos[1]):
                    self.selectedIndex = k
                    fire_if_possible(self.on_selected, self)
    
    def update(self):
        howmanyitems = int(self.bounds[3] / self.itemHeight)
        
        self._scroll.max = len(self.items) - howmanyitems if len(self.items) > howmanyitems else 0
        
        for i in range(len(self.items)):
            ih = self.itemHeight * i            
            ih -= self._scroll.value * self.itemHeight
            
            self._ibounds[i] = [self.bounds[0]+1, self.bounds[1]+ih+1, self.bounds[2]-2, self.itemHeight]

        if len(self.items)*self.itemHeight > self.bounds[3]:
            self._scroll.visible = True
        else:
            self._scroll.visible = False
        
        self._scroll.bounds=[self.bounds[0]+self.bounds[2]-12, self.bounds[1], 12, self.bounds[3]]
        self._scroll.update()
        self._scroll.theme = self.theme
        PControl.new.update(self)
    
    def draw(self):
        if not self.visible: return
        PControl.new.draw(self)
        
        if self.theme == None:
            h_draw_quad_b(self.bounds, self.backColor, 2)
        else:
            t = self.theme["panel"]              
            h_draw_ninepatch(t["image"].id, t["image"].size[0], t["image"].size[1], self.bounds, t["padding"])
        
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
                        h_draw_frame(bnds, default["button_hover"], 0)
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
                
        self._scroll.draw()
    

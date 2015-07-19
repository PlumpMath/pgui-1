import pgui.src.PControl as PControl
import pgui.src.PList as PList
import pgui.src.PLabel as PLabel
from .putil import *
from .pthemes import *

class new(PLabel.new):
    def __init__(self, bounds=[0, 0, 100, 20], text="DropDown"):
        PLabel.new.__init__(self, bounds=bounds, text=text)
        self.margin = 2        
        self.visible = True
        
        self.on_selected = None
        
        self.ibounds = []
        
        def sel(sender):
            self.text = sender.items[sender.selectedIndex] if len(sender.items) > 0 else self.text
            sender.enabled = False
            sender.visible = False
                 
            fire_if_possible(self.on_selected, self)
            
            sender.requestFocus()
            
        self._list = PList.new(bounds=[bounds[0], bounds[1]+bounds[3], bounds[2], 0])
        self._list.enabled = False
        self._list.visible = False
        self._list.on_selected = sel
            
    @property
    def selectedIndex(self):
        return self._list.selectedIndex
    
    @selectedIndex.setter
    def selectedIndex(self, i):
        self._list.selectedIndex = i
    
    @property
    def items(self):
        return self._list.items
    
    @items.setter
    def items(self, newitems):
        self._list.items = newitems
    
    def onMouseClick(self, data):
        if data["button"] == events.LEFTMOUSE:
            self._list.enabled = not self._list.enabled
            self._list.visible = self._list.enabled
            
            if self._list.enabled:
                h = self._list.itemHeight * len(self._list.items) + 10
                self._list.bounds[3] = h
            else:
                self._list.bounds[3] = 0
    
    def draw(self):
        if not self.visible: return
        
        if self.drawFrame:
            if self.theme == None:
                h_draw_button(default["button_normal"], self.bounds, self.hovered, self.clicked)
            else:
                tn = self.theme["button_normal"]
                th = self.theme["button_hover"]
                tc = self.theme["button_click"]
                t = tn
                if not self.hovered and not self.clicked:
                    t = tn
                elif self.hovered and not self.clicked:
                    t = th
                elif self.hovered and self.clicked:
                    t = tc
                else:
                    t = tc                    
                h_draw_9patch_skin(t, self.bounds)
        
        PLabel.new.draw(self)
        h_draw_arrow((self.bounds[0]+self.bounds[2])-10, self.bounds[1]+(self.bounds[3]/2), 4, color=self.foreColor)
        
        self._list.draw()
    
    def update(self):        
        PLabel.new.update(self)
                    
        self._list.bounds[0] = self.bounds[0]
        self._list.bounds[1] = self.bounds[1]+self.bounds[3]
        self._list.bounds[2] = self.bounds[2]
                
        self._list.theme = self.theme
        self._list.zorder = self.zorder
        self._list.update()
        
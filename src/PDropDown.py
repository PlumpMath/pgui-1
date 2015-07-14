import pgui.src.PControl as PControl
import pgui.src.PList as PList
import pgui.src.PButton as PButton
from .putil import *
from .pthemes import *

class new(PButton.new):
    def __init__(self, bounds=[0, 0, 100, 20], text="DropDown"):
        PButton.new.__init__(self, bounds=bounds, text=text)
        self.margin = 2        
        self.visible = True
        
        self.on_selected = None
        
        self.ibounds = []
        
        def sel(sender):
            self.text = sender.items[sender.selectedIndex] if len(sender.items) > 0 else self.text
            sender.enabled = False
            sender.visible = False
                 
            fire_if_possible(self.on_selected, self)
            
            if sender.enabled:
                self.__nh = 100
            else:
                self.__nh = 0
            self.requestFocus()
            
        self._list = PList.new(bounds=[bounds[0], bounds[1]+bounds[3], bounds[2], 0])
        self._list.enabled = False
        self._list.visible = False
        self._list.on_selected = sel
        
        self.__nh = 0
    
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
            if self._list.enabled:
                max = 100
                h = self._list.itemHeight * len(self._list.items) + 10
                self.__nh = h if h < max else max
            else:
                self.__nh = 0
    
    def draw(self):
        if not self.visible: return
        PButton.new.draw(self)
        
        h_draw_arrow((self.bounds[0]+self.bounds[2])-10, self.bounds[1]+(self.bounds[3]/2), 4, color=self.foreColor)
        
        self._list.draw()
    
    def update(self):
        if not self.focused:
            self.__nh = 0
            self._list.enabled = False
            
        self._list.bounds[0] = self.bounds[0]
        self._list.bounds[1] = self.bounds[1]+self.bounds[3]
        self._list.bounds[2] = self.bounds[2]
        self._list.bounds[3] = lerp(self._list.bounds[3], self.__nh, 0.5)
        
        if self._list.bounds[3] > 2:
            self._list.visible = True
        else:
            self._list.visible = False
        
        self._list.theme = self.theme
        self._list.zorder = self.zorder
        self._list.update()
        
        PButton.new.update(self)
        
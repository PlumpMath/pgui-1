import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100]):
        PControl.new.__init__(self, bounds)        
        self._controls = {}
        self.border = 1        
        self.zorder = -9999
        self.layout = None
        self.drawSelection = False
        self.updating = False
    
    def createSubContainer(self, name="newSubContainer", controls={}, bounds=[0, 0, 100, 100]):
        cnt = new(bounds=bounds)
        cnt.controls = controls
        
        return self.addControl(name, cnt)
    
    # Add a simple control
    def addControl(self, name, control, mouse_down=None):
        print(self.controls)
        
        control.on_mouse_down = mouse_down
        
        nname = u_gen_name(self.controls.keys(), name)
        tmpc = self.controls.copy()
        tmpc[nname] = control
        self.controls = tmpc
        
        self.__refreshControls()        
        self.update()
        
        return control
    
    @property
    def controls(self):
        return self._controls
    
    @controls.setter
    def controls(self, ctrl):
        self._controls = ctrl
        self.__refreshControls()
        
    def __refreshControls(self):
        for k, c in self.controls.items():
            c.name = k
            c.manager = self.manager
            c.theme = self.theme
        
    def draw(self):
        if self.visible:
            PControl.new.draw(self)
            if self.drawFrame:
                if self.theme == None:                    
                    h_draw_frame(self.bounds, self.backColor, self.border)    
                    h_clip_begin(self.bounds, padding=[1, 1, 1, 1])                
                else:                    
                    t = self.theme["panel"]                    
                    h_draw_ninepatch(t["image"].id, t["image"].size[0], t["image"].size[1], self.bounds, t["padding"])
                    h_clip_begin(self.bounds, padding=t["padding"])
            
            ctrls = sorted(self._controls.values(), key=lambda x: x.zorder)
            for v in ctrls:
                if not self.updating:
                    v.draw()
                
            h_clip_end()
    
    def __zorder_update(self):
        ctrls = sorted(self._controls.values(), key=lambda x: x.layout_order)
        for c in ctrls:
            c.parent = self
            if c.focused:
                c.zorder = 99
            else:
                c.zorder = -99
    
    def update(self):
        if self.enabled and self.visible:
            self.updating = True
            
            if self.updating:
                self.__zorder_update()
                
                ctrls = sorted(self.controls.values(), key=lambda x: x.layout_order)
                for i in range(len(ctrls)):
                    v = ctrls[i]
                    v.foreColor = self.foreColor
                    if v.theme == None:
                        v.theme = self.theme
        
                    if self.layout != None:
                        self.layout.bounds = self.bounds
                        self.layout.apply_layout(v, i, len(ctrls))
                    
                    v.update()
                    
            self.updating = False
            
            PControl.new.update(self)

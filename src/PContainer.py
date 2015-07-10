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
        if isinstance(controls,  dict):
            cnt.controls = controls
        self.controls[u_gen_name(self._controls.keys(), name)] = cnt
        self.__refreshControls()
        self.update()
        return cnt
    
    # Add a simple control
    def addControl(self, name, control, mouse_down=None):
        control.on_mouse_down = mouse_down
        control.parent = self
        if name not in self.controls.keys():
            self.controls[name] = control
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
        prev = None
        for k, c in self._controls.items():
            c.name = k
            c.zorder = prev.zorder+1 if prev != None else 0
            c.manager = self.manager
            c.parent = self
            c.theme = self.theme
            prev = c
        
    def draw(self):
        if self.visible:
            if self.drawFrame:
                if self.theme == None:                    
                    h_draw_frame(self.bounds, self.backColor, self.border)    
                    h_clip_begin(self.bounds, padding=[1, 1, 1, 1])                
                else:                    
                    t = self.theme["panel"]                    
                    h_draw_ninepatch(t["image"].id, t["image"].size[0], t["image"].size[1], self.bounds, t["padding"])
                    h_clip_begin(self.bounds, padding=t["padding"])
            
            PControl.new.draw(self)
            
            ctrls = sorted(self._controls.values(), key=lambda x: x.zorder)
            for v in ctrls:
                if not self.updating:
                    v.draw()
                
            h_clip_end()
    
    def __zorder_update(self):
        ctrls = sorted(self._controls.values(), key=lambda x: x.layout_order)
        for c in ctrls:
            if c.focused:
                c.zorder = 99
            else:
                c.zorder = -99
    
    def update(self):
        if self.enabled and self.visible:
            self.updating = True
            if self.updating:
                self.__zorder_update()
                
                ctrls = sorted(self._controls.values(), key=lambda x: x.layout_order)
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

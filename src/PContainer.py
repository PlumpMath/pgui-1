import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100]):
        PControl.new.__init__(self, bounds)        
        self.controls = {}
        self.border = 1
        self.layout = None
        self.drawSelection = False
        
        self._corder = 0
    
    def createSubContainer(self, name="newSubContainer", bounds=[0, 0, 100, 100]):
        return self.addControl(name, new(bounds=bounds))
    
    # Add a simple control
    def addControl(self, name, control, mouse_down=None):
        control.on_mouse_down = mouse_down
        control.layout_order = self._corder
        
        keys = list(self.controls.keys())
        nname = u_gen_name(keys, name)
        
        control.name = nname
        control.manager = self.manager
        control.theme = self.theme
        control.parent = self
        
        self.controls[nname] = control
        
        self._corder+=1
        
        self.update()
        return control

    def draw(self):
        if self.visible:
            PControl.new.draw(self)
            
            if self.drawFrame:
                if self.theme == None:                    
                    h_draw_frame_d(self.bounds, self.backColor, self.border)    
                    h_clip_begin(self.bounds, padding=[1, 1, 1, 1])
                else:                    
                    t = self.theme["panel"]
                    h_draw_9patch_skin(t, self.bounds)
                    h_clip_begin(self.bounds, padding=t["padding"])
            
            ctrls = sorted(list(self.controls.values()), key=lambda x: x.zorder)
            for v in ctrls:
                v.draw()
                
            h_clip_end()
    
    def __zorder_update(self):
        ctrls = sorted(list(self.controls.values()), key=lambda x: x.layout_order)
        for c in ctrls:
            if c.focused:
                c.zorder = 99
            else:
                c.zorder = -99
    
    def update(self):
        if self.enabled and self.visible:
            self.__zorder_update()
            
            sort_key = (lambda x: x.layout_order) if self.layout is not None else (lambda x: x.zorder)
            ctrls = sorted(list(self.controls.values()), key=sort_key)
            for c in ctrls:
                c.foreColor = self.foreColor
                if c.theme == None:
                    c.theme = self.theme
                
                if self.layout is not None:
                    self.layout.bounds = self.bounds.copy()
                    self.layout.apply_layout(c, len(ctrls))
                    
                c.update()
                
            PControl.new.update(self)

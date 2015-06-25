import bgl
import blf
import math
import json
from bge import render, logic, events, types

from .putil import *
from .pthemes import *

class ExitEvent:
    def __init__(self, mgr):
        self.pmanager = mgr
        #print("PGUI Initialized")
            
    def __del__(self):
        tcnt = 0
        if self.pmanager._theme != None:            
            for k, v in self.pmanager._theme.items():
                if k != "PGUI_SKIN":
                    h_del_texture(v["image"].id)
                    tcnt += 1
        #print("PGUI Exited. %d textures deleted." % tcnt)

class new:
    def __init__(self):
        self._controls = {}
        self._theme = None                
        logic.exit = ExitEvent(self)
                        
    def createRadioGroup(self, radios):
        if not isinstance(radios, list): return
        rg = PRadioGroup()
        for r in radios:
            if r in self._controls.keys():
                rg.addToGroup(self._controls[r])
        return rg
    
    def loadTheme(self, path):
        self.theme = json.load(open(path))
    
    def saveTheme(self, path, theme):
        json.dump(theme, open(path, "w"))
    
    @property
    def theme(self):
        return self._theme
    
    @theme.setter
    def theme(self, v):
        self._theme = v
        if v != None:
            for k, v in self._theme.items():
                if k != "PGUI_SKIN":
                    path = v["image"]
                    v["image"] = Image(logic.expandPath(path))
                    
            for k, c in self._controls.items():
                c.theme = v

    @property
    def controls(self):
        return self._controls
    
    @controls.setter
    def controls(self, ctrl):
        self._controls = ctrl
        for k, c in self._controls.items():
            c.name = k
            c.manager = self
            c.theme = self.theme
            
        sce = logic.getCurrentScene()
        sce.post_draw = [self.draw]
        print(self.theme)
        
    def draw(self):
        ctrls = sorted(self._controls.values(), key=lambda x: x.zorder, reverse=True)
        for c in ctrls:
            c.draw()
    
    def update(self):
        ctrls = sorted(self._controls.values(), key=lambda x: x.zorder, reverse=True)
        for c in ctrls:
            c.update()

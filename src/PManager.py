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
        
        self.updating = False
        
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
        
    def draw(self):
        width = render.getWindowWidth()
        height = render.getWindowHeight()
        
        # 2D Projection
        bgl.glMatrixMode(bgl.GL_PROJECTION)
        bgl.glLoadIdentity()
        bgl.glOrtho(0, width, height, 0, -1, 1)
        bgl.glMatrixMode(bgl.GL_MODELVIEW)
        bgl.glLoadIdentity()
        
        # 2D Shading (Flat)
        bgl.glDisable(bgl.GL_CULL_FACE)
        bgl.glDisable(bgl.GL_LIGHTING)
        bgl.glDisable(bgl.GL_DEPTH_TEST)
        
        # 2D Blending (Alpha)
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Line antialias
        bgl.glEnable(bgl.GL_LINE_SMOOTH)
        bgl.glHint(bgl.GL_LINE_SMOOTH_HINT, bgl.GL_NICEST)
        
        ctrls = sorted(self._controls.values(), key=lambda x: x.zorder, reverse=True)
        for c in ctrls:
            c.draw()
    
    def update(self):
        self.updating = True
        ctrls = sorted(self._controls.values(), key=lambda x: x.zorder, reverse=True)
        for c in ctrls:
            if self.updating:
                oldv = c.visible
                c.visible = False if c.visible else True
                c.update()
                c.visible = oldv
            
        self.updating = False

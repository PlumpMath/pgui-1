import bgl
import blf
import math
import json
from bge import render, logic, events, types

from .putil import *
from .pthemes import *
import pgui.src.PContainer as PContainer
import pgui.src.PRadioGroup as PRadioGroup

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
        
        self.mouse = {"x":0, "y":0}
        
        self._gfc = (0, 0, 0, 1)
        
    def createRadioGroup(self, radios):
        if not isinstance(radios, list): return
        rg = PRadioGroup.new()
        for r in radios:
            if r in self._controls.keys():
                rg.addToGroup(self._controls[r])
        return rg
    
    def createContainer(self, name="newContainer", controls={}, bounds=[0, 0, 100, 100]):
        cnt = PContainer.new(bounds=bounds)
        cnt.controls = controls
        
        return self.addControl(name, cnt)
    
    # Add a simple control
    def addControl(self, name, control, mouse_down=None):
        control.on_mouse_down = mouse_down
        
        nname = u_gen_name(self.controls.keys(), name)
        tmpc = self.controls.copy()
        tmpc[nname] = control
        self.controls = tmpc
        
        return control
    
    def end(self):
        self.controls = {}
        sce = logic.getCurrentScene()
        sce.post_draw = []
    
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
    def globalForeColor(self):
        return self._gfc
    
    @globalForeColor.setter
    def globalForeColor(self, val):
        self._gfc = val
        for k, c in self._controls.items():
            c.foreColor = val
    
    @property
    def controls(self):
        return self._controls
    
    @controls.setter
    def controls(self, ctrl):
        self._controls = ctrl
        self.__refreshControls()
            
        sce = logic.getCurrentScene()
        sce.post_draw = [self.draw]
        
        self.update()
    
    def __refreshControls(self):
        for k, c in self.controls.items():
            c.name = k
            c.manager = self
            c.theme = self.theme
        self.update()
    
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
        
        if len(self.controls.values()) <= 0: return
        
        ctrls = sorted(self.controls.values(), key=lambda x: x.zorder)
        for c in ctrls:
            c.draw()
    
    def __zorder_update(self):
        ctrls = sorted(self.controls.values(), key=lambda x: x.layout_order)
        for c in ctrls:
            c.parent = None
            if c.focused:
                c.zorder = 99
            else:
                c.zorder = -99
    
    def update(self):
        if len(self.controls.values()) <= 0: return
        
        width = render.getWindowWidth()
        height = render.getWindowHeight()
        
        ex = int(logic.mouse.position[0] * width)  # World X
        ey = int(logic.mouse.position[1] * height) # World Y
        
        self.mouse["x"] = ex
        self.mouse["y"] = ey
        
        self.updating = True
        
        if self.updating:
            self.__zorder_update()
            
            ctrls = sorted(self._controls.values(), key=lambda x: x.zorder, reverse=True)
            for c in ctrls:
                c.update()
        
        self.updating = False

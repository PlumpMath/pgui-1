from .putil import *
from .pthemes import *

PGUI_MOUSE_DOWN = 1
PGUI_MOUSE_UP = 0
PGUI_MOUSE_CLICK = 2

class new:
    def __init__(self, bounds=[0, 0, 100, 100]):
        self.on_mouse_hold = None
        self.on_mouse_move = None
        self.on_mouse_down = None
        self.on_mouse_up = None
        self.on_key_down = None
        self.on_key_up = None
        self.on_key_press = None
        self.on_draw = None
        
        self.enabled = True
        self.name = "PControl"
        
        self.bounds = bounds
        
        self.backColor = default["control"]
        self.foreColor = default["text_color"]
        
        self.hovered = False
        self.clicked = False
        self.clickhold = False
        self.clickrelease = False
        self.once = True
        self.konce = False
        
        self.focused = False
        self.manager = None
        
        self.visible = True
        self.enabled = True
        
        self.zorder = 0
        
        self.parent = None
        
        self.x2 = 0
        self.y2 = 0
        
        self.relativePos = [0, 0]
        
        self.theme = None
        
    @property
    def bounds(self):
        return self._bounds
    
    @bounds.setter
    def bounds(self, b):
        self._obounds = [b[0], b[1], b[2], b[3]]
        self._bounds = b
        
    def onKeyTyped(self, key, shifted):
        pass
    
    def onClick(self, x, y, btn):
        pass
    
    def onRelease(self, x, y, btn):
        pass
    
    def onDown(self, x, y, btn):
        pass
    
    def onMove(self, x, y):
        pass
    
    def onKeyEvent(self, key, state):
        pass
    
    def onDrag(self, x, y, btn):
        pass

    def update(self):
        # TODO: Check this code to see if there's something you can fix.
        #       Debug to find errors/bugs.
    
        if not self.enabled: return
        
        global pressed_current
        global pressed
        
        if self.theme != None:
            if "PGUI_SKIN" not in self.theme:
                self.theme = None
                print("Invalid theme assigned to "+self.name)
        
        if self.parent != None:
            self._bounds[0] = self._obounds[0] + self.parent.bounds[0]
            self._bounds[1] = self._obounds[1] + self.parent.bounds[1]
            
        width = render.getWindowWidth()
        height = render.getWindowHeight()
        ex = int(logic.mouse.position[0] * width)
        ey = int(logic.mouse.position[1] * height)
        
        px = ex - self.bounds[0]
        py = ey - self.bounds[1]
        self.relativePos = [px, py]
        
        if self.focused:
            shift = k_down(events.LEFTSHIFTKEY) or k_down(events.RIGHTSHIFTKEY)
            for k, v in supported_keys.items():
                if k_pressed(v):                    
                    self.onKeyTyped(v, shift)
                    fire_if_possible(self.on_key_press, self, v, shift)                    
                elif k_down(v):
                    self.onKeyEvent(v, 0)
                    fire_if_possible(self.on_key_down, self, v, 0)
                elif k_released(v):
                    self.onKeyEvent(v, 1)
                    fire_if_possible(self.on_key_up, self, v, 1)

        k_mclick = k_mouse_action_click()
        k_mrelease = k_mouse_action_release()
        k_mdown = k_mouse_action_down()
        
        if k_mrelease["active"]:
            fire_if_possible(self.on_mouse_up, self, ex, ey, k_mrelease["button"])
            self.onRelease(px, py, k_mrelease["button"])
                
        self.onDrag(ex, ey, 0)
        
        if haspoint(self.bounds, ex, ey):
            self.hovered = True
            
            self.clickhold = k_mdown["active"]
            self.clicked = k_mdown["active"]
            if not k_mdown["active"]:
                self.once = True

            if px - self.x2 > 0 or py - self.y2 > 0:
                fire_if_possible(self.on_mouse_move, self, ex, ey)
                self.onMove(ex, ey)
            
            if self.clickhold:
                self.onDown(ex, ey, k_mdown["button"])
                fire_if_possible(self.on_mouse_hold, self, ex, ey, k_mdown["button"])
            
            if not logic.handled:
                if self.clicked:                    
                    if self.once:
                        if logic.current_focus != None:
                            logic.current_focus.focused = False
                        logic.current_focus = self
                        self.focused = True
                        
                        self.onClick(ex, ey, k_mdown["button"])
                        fire_if_possible(self.on_mouse_down, self, ex, ey, k_mclick["button"])
                        
                        self.once = False
                    logic.handled = True
                    
            if not self.clicked:
                logic.handled = False
                self.once = True
        else:
            self.hovered = False
            if self.clicked:
                self.clicked = False
            self.once = True
        
        self.x2 = px
        self.y2 = py
    
    def draw(self):
        if not self.visible: return
                
        if not fire_if_possible(self.on_draw, self):
            if self.focused:
                h_draw_selected(self.bounds)
            

from .putil import *
from .pthemes import *
from bge import events

class new:
    def __init__(self, bounds=[0, 0, 100, 20]):
        # Events
        self.on_mouse_hold = None
        self.on_mouse_release = None
        self.on_mouse_enter = None
        self.on_mouse_leave = None
        self.on_mouse_move = None
        self.on_mouse_click = None
                
        self.on_key_down = None
        self.on_key_up = None
        self.on_key_press = None
        
        self.on_draw = None
                
        self.on_focus = None
        self.on_blur = None
        
        self.name = "PControl" # default
        self.drawSelection = True
        self.fireClickOnEnter = True
        
        self.bounds = bounds
        
        self.backColor = default["control"]
        self.foreColor = default["text_color"]
        
        self.hovered = False
        self.clicked = False
        self.clickhold = False
        self.enter = False        
        self.focused = False
        self.manager = None
        self.drawFrame = True
        self.visible = True
        self.enabled = True
        self.theme = None
        self.zorder = 0
        self.layout_order = 0   
        self.parent = None        
        self.relativePos = [0, 0]
        self.worldPos = [0, 0]
        
        self.toolTipText = ""
        self.toolTipTimeOut = 2.0
        
    @property
    def bounds(self):
        return self._bounds
    
    @bounds.setter
    def bounds(self, b):
        self._obounds = [b[0], b[1], b[2], b[3]]
        self._bounds = b
    
    def serialize(self, method=0):
        if method == 0:
            import json
            return json.dumps(self, default=lambda x: x.__dict__, sort_keys=True, indent=4)
        else: # Add your serialization method here.
            return None
        return None
    
    def requestFocus(self):
        if logic.current_focus != None:
            if logic.current_focus.focused:
                logic.current_focus.onBlur()
                fire_if_possible(logic.current_focus.on_blur, logic.current_focus)
            logic.current_focus.focused = False
            
        logic.current_focus = self
        self.focused = True
        logic.handled = True
        
        self.onFocus()
        fire_if_possible(self.on_focus, self)
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return "%s('%s')" % (type(self).__name__, self.name)
    
    # New event system.
    def onMouseHold(self, mouse_data):
        pass
    
    def onMouseClick(self, mouse_data):
        pass
    
    def onMouseRelease(self, mouse_data):
        pass
    
    def onMouseMove(self, mouse_data):
        pass
    
    def onMouseEnter(self):
        pass
    
    def onMouseLeave(self):
        pass
    
    def onKeyDown(self, key_data):
        pass
    
    def onKeyUp(self, key_data):
        pass
    
    def onKeyPress(self, key_data):
        pass
    
    def onDraw(self):
        pass
        
    def onFocus(self):
        pass
    
    def onBlur(self):
        pass
    
    def update(self):
        # TODO: Check this code to see if there's something you can fix.
        #       Debug to find errors/bugs.
        
        if not self.enabled: return
        
        global pressed_current
        global pressed
        
        #if self.parent is not None:
        #    print(self.parent)
        
        # check theme
        if self.theme != None:
            if "PGUI_SKIN" not in self.theme:
                self.theme = None
                print("Invalid theme assigned to "+self.name)
        
        # update child bounds
        if self.parent != None:
            if self.parent.layout is None:
                self._bounds[0] = self._obounds[0] + self.parent.bounds[0]
                self._bounds[1] = self._obounds[1] + self.parent.bounds[1]
        
        if self.manager != None:
            ex, ey = self.manager.mouse["x"], self.manager.mouse["y"]
        else:
            # Get mouse position if the manager is null
            width = render.getWindowWidth()
            height = render.getWindowHeight()            
            ex = int(logic.mouse.position[0] * width)  # World X
            ey = int(logic.mouse.position[1] * height) # World Y 
            
        px = ex - self.bounds[0]                   # Local X
        py = ey - self.bounds[1]                   # Local Y
        
        self.relativePos = [px, py]
        self.worldPos = [ex, ey]
        
        if self.focused:
            shift = k_down(events.LEFTSHIFTKEY) or k_down(events.RIGHTSHIFTKEY)
            ctrl = k_down(events.LEFTCTRLKEY) or k_down(events.RIGHTCTRLKEY)
            alt = k_down(events.LEFTALTKEY) or k_down(events.RIGHTALTKEY)
            
            if self.fireClickOnEnter:
                if k_pressed(events.ENTERKEY):
                    t_mouse_data = {
                        "button": events.LEFTMOUSE,
                        "x": self.bounds[0]+1,
                        "y": self.bounds[1]+1
                    }
                    self.onMouseClick(t_mouse_data)
                    fire_if_possible(self.on_mouse_click, self, t_mouse_data)
            
            for k, v in supported_keys.items():
                key_data = {
                    "key": v,
                    "keyString": events.EventToString(v),
                    "shift": shift,
                    "control": ctrl,
                    "alt": alt
                }
                if k_pressed(v):                    
                    self.onKeyPress(key_data)
                    fire_if_possible(self.on_key_press, self, key_data)                    
                elif k_down(v):
                    self.onKeyDown(key_data)
                    fire_if_possible(self.on_key_down, self, key_data)
                elif k_released(v):
                    self.onKeyUp(key_data)
                    fire_if_possible(self.on_key_up, self, key_data)
                
        if haspoint(self.bounds, ex, ey):
            if not self.enter:
                self.onMouseEnter()
                fire_if_possible(self.on_mouse_enter, self)
                
                logic.current_hover = self
                
                self.enter = True
                
            self.hovered = True
                        
            m_down    = k_mouse_action_down()
            m_click   = k_mouse_action_click()
            m_release = k_mouse_action_release()
            
            mouse_move_data = {
                "x": px,
                "y": py
            }
            self.onMouseMove(mouse_move_data)
            fire_if_possible(self.on_mouse_move, self, mouse_move_data)
            
            if not logic.handled:                
                if m_click["active"]:                
                    self.clicked = True                
                    self.requestFocus()
                    
                    mouse_data = {
                        "button": m_click["button"],
                        "x": px,
                        "y": py
                    }
                    self.onMouseClick(mouse_data)
                    fire_if_possible(self.on_mouse_click, self, mouse_data)
                    
                    logic.handled = True
                    
                if m_down["active"]:
                    self.clickhold = True
                    
                    mouse_data = {
                        "button": m_down["button"],
                        "x": px,
                        "y": py
                    }
                    self.onMouseHold(mouse_data)
                    fire_if_possible(self.on_mouse_hold, self, mouse_data)
                    
                    logic.handled = True
                
            if m_release["active"]:
                mouse_data = {
                    "button": m_release["button"],
                    "x": px,
                    "y": py
                }
                self.onMouseRelease(mouse_data)
                fire_if_possible(self.on_mouse_release, self, mouse_data)
                
                self.clicked = False
                self.clickhold = False
                
                # Prevent from activating controls that are behind this control.
                logic.handled = False
        else:
            self.hovered = False
            if self.enter:
                self.onMouseLeave()
                fire_if_possible(self.on_mouse_leave, self)
                self.enter = False                             
            if self.clicked:
                self.clicked = False
    
    def draw(self):
        if not self.visible: return
                
        if not fire_if_possible(self.on_draw, self):
            if self.drawSelection:
                if self.focused:
                    h_draw_selected(self.bounds)
        self.onDraw()

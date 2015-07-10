import bgl
import blf
from bge import render, logic, events, types, texture
import math

def haspoint(bounds, x, y):
    return (x >= bounds[0]            and
            x <= bounds[0]+bounds[2]  and
            y >= bounds[1]            and
            y <= bounds[1]+bounds[3])

def m_clicked_act(btn, state=logic.KX_INPUT_JUST_ACTIVATED):
    return logic.mouse.events[btn] == state

def m_clicked_down(btn, state=logic.KX_INPUT_ACTIVE):
    return m_clicked_act(btn, state)

def m_release(btn, state=logic.KX_INPUT_JUST_RELEASED):
    return m_clicked_act(btn, state)

def k_down(btn, state=logic.KX_INPUT_ACTIVE):
    return logic.keyboard.events[btn] == state
def k_pressed(btn, state=logic.KX_INPUT_JUST_ACTIVATED):
    return logic.keyboard.events[btn] == state
def k_released(btn, state=logic.KX_INPUT_JUST_RELEASED):
    return logic.keyboard.events[btn] == state

def k_mouse_action_click():
    act = {"button": 0, "active": False}
    
    if m_clicked_act(events.LEFTMOUSE):
        act["button"] = events.LEFTMOUSE
        act["active"] = True
    elif m_clicked_act(events.RIGHTMOUSE):
        act["button"] = events.RIGHTMOUSE
        act["active"] = True
    elif m_clicked_act(events.MIDDLEMOUSE):
        act["button"] = events.MIDDLEMOUSE
        act["active"] = True
    else:
        act["active"] = False
    
    return act

def k_mouse_action_down():
    act = {"button": 0, "active": False}
    
    if m_clicked_down(events.LEFTMOUSE):
        act["button"] = events.LEFTMOUSE
        act["active"] = True
    elif m_clicked_down(events.RIGHTMOUSE):
        act["button"] = events.RIGHTMOUSE
        act["active"] = True
    elif m_clicked_down(events.MIDDLEMOUSE):
        act["button"] = events.MIDDLEMOUSE
        act["active"] = True
    else:
        act["active"] = False
    
    return act

def k_mouse_action_release():
    act = {"button": 0, "active": False}
    
    if m_release(events.LEFTMOUSE):
        act["button"] = events.LEFTMOUSE
        act["active"] = True
    elif m_release(events.RIGHTMOUSE):
        act["button"] = events.RIGHTMOUSE
        act["active"] = True
    elif m_release(events.MIDDLEMOUSE):
        act["button"] = events.MIDDLEMOUSE
        act["active"] = True
    else:
        act["active"] = False
    
    return act

def u_gen_name(availableNames, namestring):
    cnt = 0
    if isinstance(availableNames, list) or isinstance(availableNames, tuple):
        for i in availableNames:
            if i.startswith(namestring):
                cnt += 1
        if cnt == 0: cnt = ""
    else:
        cnt = ""
    return namestring + cnt

# Fire an event if it's possible
def fire_if_possible(event, *args):
    if not hasattr(event, "__call__"): return False
    if event != None:
        event(*args)
        return True
    return False

def clamp(val, min, max):
    if val > max:
        return max
    if val < min:
        return min
    return val

def xrange(s, e, st=1):
    while s <= e:
        yield s
        s += st

def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

def bright(color, factor=1.0):
    if factor < 0.0: factor = 0.0    
    return [clamp(color[0] * factor, 0.0, 1.0),
            clamp(color[1] * factor, 0.0, 1.0),
            clamp(color[2] * factor, 0.0, 1.0),
            color[3]]

def gen_coords_from_bounds(b, w, h):
    w+=0.0001 # Just to make sure we're not dividing by 0 =)
    h+=0.0001 #
    
    return [
        (b[0]/w, b[1]/w),
        ((b[0]+b[2])/w, b[1]/h),
        (b[0]+b[2], b[1]+b[3]),
        (b[0], b[1]+b[3])
    ]

def h_draw_texture(id, w, h, bounds, coords):    
    bgl.glEnable(bgl.GL_TEXTURE_2D)
    bgl.glBindTexture(bgl.GL_TEXTURE_2D, id)
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)
    
    bgl.glColor4f(*(1,1,1,1))
    
    B = bounds
    C = coords
    
    
    
    D = [
        (C[0][0]/w, C[0][1]/h),
        (C[1][0]/w, C[1][1]/h),
        (C[2][0]/w, C[2][1]/h),
        (C[3][0]/w, C[3][1]/h),
    ]
    #print(D)
    
    bgl.glBegin(bgl.GL_QUADS)
    bgl.glTexCoord2f(D[0][0], D[0][1])    
    bgl.glVertex2f(B[0], B[1])
    
    bgl.glTexCoord2f(D[1][0], D[1][1])    
    bgl.glVertex2f(B[0]+B[2], B[1])
    
    bgl.glTexCoord2f(D[2][0], D[2][1])    
    bgl.glVertex2f(B[0]+B[2], B[1]+B[3])
    
    bgl.glTexCoord2f(D[3][0], D[3][1])    
    bgl.glVertex2f(B[0], B[1]+B[3])
    bgl.glEnd()

    bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
    bgl.glDisable(bgl.GL_TEXTURE_2D)

def h_draw_ninepatch(id, w, h, bounds, padding, wire=False):
    if len(bounds) < 4: return
    if len(padding) < 4: return
    
    M = bgl.GL_LINE_LOOP if wire else bgl.GL_QUADS
    
    B = bounds
    P = padding
    Q = [padding[0], padding[1], padding[2], padding[3]]
    
    # TOP LEFT
    if padding[0] > 0 and padding[1] > 0:
        BTL = [B[0], B[1], P[0], P[1]]
        CTL = [
            (0, h),
            (Q[0], h),
            (Q[0], h-Q[1]),
            (0, h-Q[1])
        ]
        h_draw_texture(id, w, h, BTL, CTL)
    
    # TOP MIDDLE    
    if padding[1] > 0:
        BTT = [B[0]+P[0], B[1], B[2]-(P[0]+P[2]), P[1]]
        CTT = [
            (Q[0], h),
            (w-Q[2], h),        
            (w-Q[2], h-Q[1]),
            (Q[0], h-Q[1])
        ]
        h_draw_texture(id, w, h, BTT, CTT)
    
    # TOP RIGHT
    if padding[2] > 0 and padding[1] > 0:
        BTR = [B[0]+B[2]-P[2], B[1], P[2], P[1]]
        CTR = [
            (w-Q[2], h),
            (w,  h),
            (w,  h-Q[1]),
            (w-Q[2], h-Q[1])
        ]
        h_draw_texture(id, w, h, BTR, CTR)
    
    # MIDDLE LEFT
    if padding[2] > 0:
        BML = [B[0], B[1]+P[1], P[0], B[3]-(P[3]+P[1])]
        CML = [
            (0, h-Q[3]),
            (Q[0], h-Q[3]),
            (Q[0], Q[3]),
            (0, Q[3])
        ]
        h_draw_texture(id, w, h, BML, CML)
    
    # MIDDLE CENTER
    BMC = [B[0]+P[0], B[1]+P[1], B[2]-(P[0]+P[2]), B[3]-(P[3]+P[1])]
    CMC = [
        (Q[0], h-Q[3]),
        (w-Q[2], h-Q[3]),
        (w-Q[2], Q[3]),
        (Q[0], Q[3])
    ]
    h_draw_texture(id, w, h, BMC, CMC)
    
    # MIDDLE RIGHT
    if padding[2] > 0:
        BMR = [B[0]+B[2]-P[2], B[1]+P[1], P[0], B[3]-(P[3]+P[1])]
        CMR = [
            (w-Q[2], h-Q[3]),
            (w, h-Q[3]),
            (w, Q[3]),
            (w-Q[2], Q[3])
        ]
        h_draw_texture(id, w, h, BMR, CMR)
    
    # BOTTOM LEFT
    if padding[0] > 0 and padding[3] > 0:
        BBL = [B[0], B[1]+B[3]-P[3], P[0], P[3]]
        CBL = [
            (0,  Q[3]),
            (Q[0], Q[3]),
            (Q[0], 0),
            (0, 0)
        ]
        h_draw_texture(id, w, h, BBL, CBL)
    
    # BOTTOM MIDDLE
    if padding[3] > 0:
        BBM = [B[0]+P[0], B[1]+B[3]-P[3], B[2]-(P[0]+P[2]), P[3]]
        CBM = [
            (Q[0],  Q[3]),
            (w-Q[2], Q[3]),
            (w-Q[2], 0),
            (Q[0], 0)
        ]
        h_draw_texture(id, w, h, BBM, CBM)
    
    # BOTTOM RIGHT
    if padding[2] > 0 and padding[3] > 0:
        BBR = [B[0]+B[2]-P[2], B[1]+B[3]-P[3], P[2], P[3]]
        CBR = [
            (w-Q[2], Q[3]),
            (w, Q[3]),
            (w, 0),
            (w-Q[2], 0)
        ]
        h_draw_texture(id, w, h, BBR, CBR)

def h_draw_arrow(x, y, size, up=False, color=(0, 0, 0, 1)):
    bgl.glColor4f(*color)
    if not up:
        bgl.glBegin(bgl.GL_TRIANGLES)
        bgl.glVertex2f(x-size, y-size/2)
        bgl.glVertex2f(x, y+size/2)
        bgl.glVertex2f(x+size, y-size/2)
        bgl.glEnd()
    else:
        bgl.glBegin(bgl.GL_TRIANGLES)
        bgl.glVertex2f(x-size, y+size/2)
        bgl.glVertex2f(x, y-size/2)
        bgl.glVertex2f(x+size, y+size/2)
        bgl.glEnd()

def h_draw_arrow_2(x, y, size, right=False, color=(0, 0, 0, 1)):
    bgl.glColor4f(*color)
    if not right:
        bgl.glBegin(bgl.GL_TRIANGLES)
        bgl.glVertex2f(x-size/2, y-size)
        bgl.glVertex2f(x+size/2, y)
        bgl.glVertex2f(x-size/2, y+size)
        bgl.glEnd()
    else:
        bgl.glBegin(bgl.GL_TRIANGLES)
        bgl.glVertex2f(x+size/2, y-size)
        bgl.glVertex2f(x-size/2, y)
        bgl.glVertex2f(x+size/2, y+size)
        bgl.glEnd()

def h_clip_begin(bounds):
    vp = bgl.Buffer(bgl.GL_INT, 4)
    bgl.glGetIntegerv(bgl.GL_VIEWPORT, vp)
    
    scp = [0, 0, bounds[2], bounds[3]]
    scp[0] = bounds[0] + vp[0]
    scp[1] = vp[3] - (bounds[1] + vp[1])
    
    bgl.glEnable(bgl.GL_SCISSOR_TEST)
    bgl.glClearColor(0, 0, 0, 0)
    bgl.glClear(bgl.GL_COLOR_BUFFER_BIT | bgl.GL_SCISSOR_BIT)
    bgl.glScissor(*scp)

def h_clip_end():
    bgl.glDisable(bgl.GL_SCISSOR_TEST)

def h_draw_text(fid, text, bounds, color, margin=0, font_size=16, text_align=0, vertical_align=0, shadow=False):
    text = str(text)
    width = render.getWindowWidth()
    height = render.getWindowHeight()
    
    #h_clip_begin(bounds)
    
    blf.size(fid, font_size, 72)
    if shadow:
        blf.enable(fid, blf.SHADOW)
        blf.shadow(fid, 3, 0.0, 0.0, 0.0, 1.0)
        blf.shadow_offset(fid, 0, -1)
    else:
        blf.disable(fid, blf.SHADOW)
    bgl.glPushMatrix()
    
    # Fix upside-down text =)
    w, h = blf.dimensions(fid, text)
    bgl.glTranslated(0.0, h, 0.0)
    bgl.glScalef(1.0, -1.0, 1.0)
    
    bgl.glColor4f(*color)

    texts = text.split("\n")
    yn = 0
    if vertical_align == 0:
        yn = margin
    elif vertical_align == 1:
        yn = bounds[3]/2-(h*len(texts))/2
    elif vertical_align == 2:
        yn = (bounds[3]-(h*len(texts)))-margin
    for i in range(len(texts)):            
        texts[i] = texts[i].replace("\t", "        ")
        wl, hl = blf.dimensions(fid, texts[i])
        xn = 0
        
        if text_align == 0:
            xn = margin
        elif text_align == 1:
            xn = bounds[2]/2-wl/2
        elif text_align == 2:
            xn = (bounds[2]-wl)-margin
            
        blf.position(fid, bounds[0]+xn, -bounds[1]-(i*h)-yn, 1)
        
        blf.draw(fid, texts[i])
        
    bgl.glScalef(1.0, 1.0, 1.0)
    bgl.glPopMatrix()
    
    #h_clip_end()

# type: 1 = Raised, 2 = Sunken, 0 = None
def h_draw_frame_d(bounds, color, type=1):
    if len(bounds) < 4: return

    DRK = bright(color, 0.5)
    LGT = bright(color, 4.0)
    
    bgl.glLineWidth(1)
    bgl.glColor4f(*color)
    bgl.glBegin(bgl.GL_QUADS)
    bgl.glVertex2f(bounds[0]          , bounds[1])
    bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
    bgl.glVertex2f(bounds[0]+bounds[2], bounds[1]+bounds[3])
    bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
    bgl.glEnd()
    
    if type == 1:
        bgl.glColor4f(*LGT)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
        bgl.glVertex2f(bounds[0]          , bounds[1])
        bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
        bgl.glEnd()
        bgl.glColor4f(*DRK)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
        bgl.glVertex2f(bounds[0]+bounds[2], bounds[1]+bounds[3])
        bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
        bgl.glEnd()
    elif type == 2:
        bgl.glColor4f(*DRK)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
        bgl.glVertex2f(bounds[0]          , bounds[1])
        bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
        bgl.glEnd()
        bgl.glColor4f(*LGT)
        bgl.glBegin(bgl.GL_LINE_STRIP)
        bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
        bgl.glVertex2f(bounds[0]+bounds[2], bounds[1]+bounds[3])
        bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
        bgl.glEnd()


def h_draw_quad(bounds, color, type=0):
    h_draw_frame_d(bounds, color, type)

def h_draw_quad_b(bounds, bg, type=2):
    bnds = [bounds[0]+1, bounds[1]+1, bounds[2]-2, bounds[3]-2]
    h_draw_frame_d(bounds, (0.83, 0.815, 0.78, 1), type)
    h_draw_frame_d(bnds, bg, 0)

def h_draw_quad_wire(bounds):
    if len(bounds) < 4: return
    bgl.glLineWidth(0.5)
    bgl.glBegin(bgl.GL_LINE_LOOP)
    bgl.glVertex2f(bounds[0]          , bounds[1])
    bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
    bgl.glVertex2f(bounds[0]+bounds[2], bounds[1]+bounds[3])
    bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
    bgl.glEnd()

def h_draw_frame(bounds, color, t):
    bgl.glEnable(bgl.GL_BLEND)
    bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)
    h_draw_quad(bounds, color, t)

def h_draw_rect(bounds):
    if len(bounds) < 4: return
    bgl.glBegin(bgl.GL_QUADS)
    bgl.glVertex2f(bounds[0]          , bounds[1])
    bgl.glVertex2f(bounds[0]+bounds[2], bounds[1])
    bgl.glVertex2f(bounds[0]+bounds[2], bounds[1]+bounds[3])
    bgl.glVertex2f(bounds[0]          , bounds[1]+bounds[3])
    bgl.glEnd()

def h_draw_button(ncolor, bounds, hover, click):
    if not hover and not click:
        h_draw_frame(bounds, ncolor, 1)
    elif hover and not click:
        h_draw_frame(bounds, ncolor, 1)
    elif hover and click:
        h_draw_frame(bounds, ncolor, 2)
    else:
        h_draw_frame(bounds, ncolor, 2)

def h_draw_tick(x, y, size, color):
    bgl.glColor4f(*bright(color, 0.2))
    bgl.glLineWidth(1.0)
    bgl.glBegin(bgl.GL_LINE_STRIP)
    bgl.glVertex2f(x-size/4, y)
    bgl.glVertex2f(x, y+size/4)
    bgl.glVertex2f(x+size/4, y-size/4)
    bgl.glEnd()
    bgl.glLineWidth(1.0)

def h_draw_selected(bounds):
    selbounds = [bounds[0]+2, bounds[1]+2, bounds[2]-4, bounds[3]-4]
    bgl.glEnable(bgl.GL_LINE_STIPPLE)
    bgl.glLineStipple(2, 0xAAAAAA)
    bgl.glLineWidth(0.5)
    bgl.glColor4f(*(0,0,0,1))
    h_draw_quad_wire(selbounds)
    bgl.glDisable(bgl.GL_LINE_STIPPLE)

def h_draw_circle(x, y, r, color, segs=16):
    bgl.glBegin(bgl.GL_TRIANGLE_FAN)
    bgl.glColor4f(*color)
    for i in range(segs):
        theta = 2.0 * 3.1415926 * float(i) / float(segs)
        tx = r * math.cos(theta)
        ty = r * math.sin(theta)
        
        bgl.glVertex2f(tx+x, ty+y)
    
    bgl.glEnd()
        
def h_draw_circle_wire(x, y, r, segs=16):
    bgl.glLineWidth(0.5)
    bgl.glBegin(bgl.GL_LINE_LOOP)
    
    for i in range(segs):
        theta = 2.0 * 3.1415926 * float(i) / float(segs)
        tx = r * math.cos(theta)
        ty = r * math.sin(theta)
        
        bgl.glVertex2f(tx+x, ty+y)
    
    bgl.glEnd()

def h_draw_circle_d(x, y, r, color, type=1):
    DRK = bright(color, 0.3)
    LGT = bright(color, 4.0)
    
    h_draw_circle(x, y, r, color)
    bgl.glLineWidth(1)
    if type == 1:
        bgl.glColor4f(*DRK)
        h_draw_circle_wire(x, y, r)
        bgl.glColor4f(*LGT)
        h_draw_circle_wire(x-0.5, y-0.5, r)        
    elif type == 2:        
        bgl.glColor4f(*LGT)
        h_draw_circle_wire(x, y, r)
        bgl.glColor4f(*DRK)
        h_draw_circle_wire(x-0.5, y-0.5, r)

def h_draw_line(x1,y1,x2,y2,col):
    bgl.glColor4f(*col)
    bgl.glBegin(bgl.GL_LINES)
    bgl.glVertex2f(x1, y1)
    bgl.glVertex2f(x2, y2)
    bgl.glEnd()

def h_gen_texture():
    id = bgl.Buffer(bgl.GL_INT, 1)
    bgl.glGenTextures(1, id)
    return id.to_list()[0]

def h_del_texture(tex):
    id = bgl.Buffer(bgl.GL_INT, 1, [tex])
    bgl.glDeleteTextures(1, id)

def u_sort_post_draw(manager):
    if manager is None: return
    sce = logic.getCurrentScene()
    sce.post_draw = [x for (x, y) in sorted(zip(sce.post_draw, manager._controls.values()), key=lambda x: x[1].zorder)]

def get_all_keys():
    keys = {}
    for k, v in events.__dict__.items():
        if not k.startswith("__"):
            if k not in ["EventToCharacter", "EventToString", "RETKEY", "WHEELUPMOUSE", "WHEELDOWNMOUSE", "MOUSEY", "MOUSEX", "LEFTMOUSE", "MIDDLEMOUSE", "RIGHTMOUSE"]:
                keys[k] = v
    return keys

supported_keys = get_all_keys()

# Based on Moguri's BGUI
class Texture2D:
    def __init__(self, path, interpolation):
        self.id = h_gen_texture()
        self.size = [0, 0]
        self.path = None
        self._interpolation = None
        
        self.bind()
        bgl.glTexEnvf(bgl.GL_TEXTURE_ENV, bgl.GL_TEXTURE_ENV_MODE, bgl.GL_MODULATE)
        self.interpolation = interpolation
        
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_S, bgl.GL_REPEAT)
        bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_WRAP_T, bgl.GL_REPEAT)
        
        self.reload(path)
    
    @property
    def interpolation(self):
        return self._interpolation
    
    @interpolation.setter
    def interpolation(self, i):
        if i != self._interpolation:
            self.bind()
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MAG_FILTER, i)
            bgl.glTexParameteri(bgl.GL_TEXTURE_2D, bgl.GL_TEXTURE_MIN_FILTER, i)
            self._interpolation = i
    
    def bind(self):
        bgl.glBindTexture(bgl.GL_TEXTURE_2D, self.id)

class Image(Texture2D):
    _cache = {}
    def __init__(self, path, interp=bgl.GL_LINEAR, cache=True):
        self._cache = cache
        Texture2D.__init__(self, path, interp)
        
    def reload(self, path):
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        
        if path == self.path: return
        if path in Image._cache:
            img = Image._cache[path]
        else:
            img = texture.ImageFFmpeg(path)
            img.scale = False
            if self._cache:
                Image._cache[path] = img
        
        data = img.image
        if data == None:
            print("Could not load the image", img)
            return
                
        self.bind()
        bgl.glTexImage2D(bgl.GL_TEXTURE_2D, 0, bgl.GL_RGBA, img.size[0],
                         img.size[1], 0, bgl.GL_RGBA,
                         bgl.GL_UNSIGNED_BYTE, data)
        
        self.size = img.size[:]
        self.path = path
        
        img = None

def h_draw_9patch_img(img, bounds, pad):
    h_draw_ninepatch(img.id, img.size[0], img.size[1], bounds, pad)

def h_draw_9patch_skin(skin, bounds):
    if "image" not in skin: return
    img = skin["image"]
    h_draw_9patch_img(img, bounds, skin["padding"])
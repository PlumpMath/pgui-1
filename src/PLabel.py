import blf
import bgl

from .putil import *
from .pthemes import *
import pgui.src.PControl as PControl

class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100], text="", fontfile="", font_size=12, text_align=0, vertical_align=1, shadow=False):
        PControl.new.__init__(self, bounds)
        self._text = text
        self.textAlign = text_align
        self.verticalAlign = vertical_align
        self.fontSize = font_size
        
        self.fid = blf.load(fontfile) if fontfile != "" else 0
        
        self.margin = 0
        self.shadow = shadow
    
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, nt):
        self._text = nt
    
    def draw(self):
        if not self.visible: return
        width = render.getWindowWidth()
        height = render.getWindowHeight()
        PControl.new.draw(self)
        
        h_draw_text(self.fid, self.text, self.bounds, self.foreColor, self.margin, self.fontSize, self.textAlign, self.verticalAlign, self.shadow)
        

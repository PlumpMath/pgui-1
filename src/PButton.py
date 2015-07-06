import pgui.src.PLabel as PLabel
import pgui.src.PImage as PImage
import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

class new(PLabel.new):
    def __init__(self, bounds=[0, 0, 100, 100], text="", fontfile="", image_file="", image_align=1, font_size=12, text_align=0):
        PLabel.new.__init__(self, bounds, text, fontfile, font_size, text_align)
        
        if image_file != "":
            self._image = PImage.new(image_path=image_file)            
        else:
            self._image = None
        
        self.imageAlign = image_align
        self.imageOffset = 0
        
        self.drawFrame = True
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, path):
        self._image = PImage.new(image_path=path)
    
    def update(self):        
        w = self._image._texture.size[0] if self._image != None else 16
        h = self._image._texture.size[1] if self._image != None else 16
        px = self.imageOffset
        py = self.bounds[3]/2-h/2
        
        if self.imageAlign == 1:
            px = self.bounds[2]/2-w/2
        elif self.imageAlign == 2:
            px = self.bounds[2]-w-self.imageOffset
        
        if self._image != None:
            self._image.drawFrame = False
            self._image.bounds = [self.bounds[0]+px, self.bounds[1]+py, self._image._texture.size[0], self._image._texture.size[1]]
        
        PLabel.new.update(self)
   
    def draw(self):
        if not self.visible: return
        
        if self.drawFrame:
            if self.theme == None:
                h_draw_button(default["button_normal"], self.bounds, self.hovered, self.clicked)
            else:
                tn = self.theme["button_normal"]
                th = self.theme["button_hover"]
                tc = self.theme["button_click"]
                t = tn
                if not self.hovered and not self.clicked:
                    t = tn
                elif self.hovered and not self.clicked:
                    t = th
                elif self.hovered and self.clicked:
                    t = tc
                else:
                    t = tc                    
                h_draw_9patch_skin(t, self.bounds)
                
        if self._image != None:
            self._image.draw()
        
        PLabel.new.draw(self)
        PControl.new.draw(self)
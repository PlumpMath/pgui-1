import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

import bgl
from bge import texture
        
class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100], image_path=""):
        PControl.new.__init__(self, bounds)        
        self._texture = None
        
        if image_path != "":
            self._texture = Image(image_path)
        
        self.textureCoords = [
            (0, 1),
            (1, 1),
            (1, 0),
            (0, 0)
        ]
    
        self.drawFrame = True
        self.padding = [2,2,2,2]
    
    def draw(self):
        PControl.new.draw(self)
        if not self.visible: return
    
        gbounds = self.bounds
        if self.drawFrame:
            gbounds = [self.bounds[0]+self.padding[0], self.bounds[1]+self.padding[1], self.bounds[2]-self.padding[2]*2, self.bounds[3]-self.padding[3]*2]
            if self.theme == None:
                h_draw_frame(self.bounds, self.backColor, 1)
                h_draw_frame(gbounds, bright(self.backColor, 0.9), 2)
            else:
                p = self.theme["panel"]
                h_draw_9patch_skin(p, gbounds)
        
        if self._texture == None: return
        
        self.textureCoords = [
            (0, self._texture.size[1]),
            (self._texture.size[0], self._texture.size[1]),
            (self._texture.size[0], 0),
            (0, 0)
        ]        
        
        h_draw_texture(self._texture.id, self._texture.size[0], self._texture.size[1], gbounds, self.textureCoords)
    
    @property
    def interpolation(self):
        return self._texture.interpolation
    
    @interpolation.setter
    def interpolation(self, i):
        self._texture.interpolation = i
    
    @property
    def imageSize(self):
        return self._texture.size
    
    @property
    def imagePath(self):
        if self._texture != None:
            return self._texture.path
        return ""
    
    @imagePath.setter
    def imagePath(self, path):
        if self._texture != None:
            self._texture.reload(path)
        else:
            self._texture = Image(path)

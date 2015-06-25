import pgui.src.PControl as PControl
from .putil import *
from .pthemes import *

import bgl
from bge import texture
        
class new(PControl.new):
    def __init__(self, bounds=[0, 0, 100, 100], image_path=""):
        PControl.new.__init__(self, bounds)        
        
        if image_path != None:
            if image_path != "":
                self._texture = Image(image_path)
        else:
            self._texture = None
        
        self.foreColor = (1,1,1,1)
        self.textureCoords = [
            (0, 1),
            (1, 1),
            (1, 0),
            (0, 0)
        ]
    
        self.drawFrame = True
        self.padding = 2
    
    def draw(self):
        PControl.new.draw(self)
        if not self.visible: return
    
        gbounds = self.bounds
        if self.drawFrame:
            gbounds = [self.bounds[0]+self.padding, self.bounds[1]+self.padding, self.bounds[2]-self.padding*2, self.bounds[3]-self.padding*2]
            if self.theme == None:
                h_draw_frame(self.bounds, self.backColor, 0)
                h_draw_frame(gbounds, bright(self.backColor, 0.5), 1)
            else:
                p = self.theme["panel"]
                h_draw_9patch_skin(p, gbounds)
        
        if self._texture == None: return
        
        bgl.glEnable(bgl.GL_TEXTURE_2D)
        
        bgl.glEnable(bgl.GL_BLEND)
        bgl.glBlendFunc(bgl.GL_SRC_ALPHA, bgl.GL_ONE_MINUS_SRC_ALPHA)

        self._texture.bind()
        bgl.glColor4f(*self.foreColor)

        bgl.glBegin(bgl.GL_QUADS)
        
        bgl.glTexCoord2f(self.textureCoords[3][0], self.textureCoords[3][1])
        bgl.glVertex2f(gbounds[0], gbounds[1]+gbounds[3])
        
        bgl.glTexCoord2f(self.textureCoords[2][0], self.textureCoords[2][1])
        bgl.glVertex2f(gbounds[0]+gbounds[2], gbounds[1]+gbounds[3])
        
        bgl.glTexCoord2f(self.textureCoords[1][0], self.textureCoords[1][1])
        bgl.glVertex2f(gbounds[0]+gbounds[2], gbounds[1])
        
        bgl.glTexCoord2f(self.textureCoords[0][0], self.textureCoords[0][1])
        bgl.glVertex2f(gbounds[0], gbounds[1])
        
        bgl.glEnd()

        bgl.glBindTexture(bgl.GL_TEXTURE_2D, 0)
    
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
        self._texture.reload(path)

import blf
import bgl

import pgui.src.PControl as PControl
import pgui.src.PLabel as PLabel
import pgui.src.PTimer as PTimer
from .putil import *
from .pthemes import *

from bge import events

class new(PLabel.new):
    def __init__(self, bounds=[0, 0, 100, 20], text="", fontfile="", font_size=14):
        PLabel.new.__init__(self, bounds, text, fontfile, font_size, 0, vertical_align=0)

        self.caretx = 0
        self.cx = 0
        
        self.backColor = default["text_background"]
        self.foreColor = default["text_color"]
        
        self.shadow = False
        self.margin = 4
        
        self.readOnly = False
        self.charSpacing = 1
        self.numbersOnly = False
        self.masked = False
        
        self.fw, self.fh = blf.dimensions(self.fid, "Ee|{^")
                
        self._tim = PTimer.new()
        self.blink = False
        
        self.on_text_changed = None
        
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, nt):
        if nt == None:
            self._text = ""
            self.caretx = 0
            
        if len(nt) < 1023:
            self._text = nt
            
            if self.caretx > len(self._text):
                self.caretx = len(self._text)
    
    def update(self):
        self._tim.update()
        
        if self._tim.time >= 0.5:
            self._tim.reset()
            self.blink = not self.blink
        
        PLabel.new.update(self)
       
    def onKeyPress(self, data):
        if self.readOnly: return
        
        key, shift = data["key"], data["shift"]
        
        chr = events.EventToCharacter(key, shift)
        self.blink = True
        
        ln = self.text
        
        if self.numbersOnly:
            if key not in [events.ONEKEY, events.TWOKEY, events.THREEKEY, events.FOURKEY, events.FIVEKEY,
                events.SIXKEY, events.SEVENKEY, events.EIGHTKEY, events.NINEKEY, events.ZEROKEY, events.PAD0,
                events.PAD1, events.PAD2, events.PAD3, events.PAD4, events.PAD5, events.PAD6, events.PAD7, 
                events.PAD8, events.PAD9, events.PADPERIOD, events.PADMINUS, events.PERIODKEY, events.MINUSKEY,
                events.LEFTARROWKEY, events.RIGHTARROWKEY, events.BACKSPACEKEY, events.DELKEY]:
                return
            
        if key == events.LEFTARROWKEY:            
            if self.caretx > 0:
                self.caretx -= 1
            else:
                self.caretx = 0
        elif key == events.RIGHTARROWKEY:            
            if self.caretx < len(ln):
                self.caretx += 1
            else:
                self.caretx = len(ln)
        elif key == events.TABKEY:
            ln = ln[:self.caretx] + "    " + ln[self.caretx:]
            self.text = ln
            self.caretx += 4
        elif key == events.BACKSPACEKEY:
            if self.caretx > 0:   
                if self.caretx < len(self.text):
                    self.caretx -= 1                
                    ln = ln[:self.caretx] + ln[self.caretx+1:]
                else:
                    ln = ln[:self.caretx-1] + ln[self.caretx:]
                self.text = ln                
            else:
                self.caretx = 0
        elif key == events.DELKEY:
            stln = ln[self.caretx:]            
            if len(stln) > 0:
                ln = ln[:self.caretx] + ln[self.caretx+1:]
                self.text = ln
        elif key == events.LEFTSHIFTKEY or key == events.RIGHTSHIFTKEY:
            pass
        else:
            if self.caretx >= len(ln):
                ln += chr
            else:
                ln = ln[:self.caretx] + chr + ln[self.caretx:]
                
            self.caretx += 1
                
            ln = ln.replace("\n", "")
            self.text = ln
        
        fire_if_possible(self.on_text_changed, self, ln)       
        self.text = ln
        
        self.__update_cx()
    
    def __update_cx(self):        
        self.cx = 0
        for i in range(self.caretx):
            self.cx += self.fw + self.charSpacing
    
    def onMouseClick(self, d):
        self.__click_char(self.worldPos[0], self.worldPos[1], d["button"])
        self.__update_cx()
        self.blink = True
    
    def __click_char(self, x, y, btn):
        if btn != events.LEFTMOUSE: return
    
        offsetx = 0
        newOffset = False
        
        for i in range(self.__renderable_right()-1):
            if not newOffset:
                if self.masked:
                    thisW, thisH = blf.dimensions(self.fid, "*")
                    nextW, nextH = blf.dimensions(self.fid, "*")
                else:
                    thisW, thisH = blf.dimensions(self.fid, self.text[i])
                    nextW, nextH = blf.dimensions(self.fid, self.text[i + 1])
                
                fx = self.bounds[0] + (offsetx + (nextW+1) / 2)
                if x <= fx+self.margin:
                    self.caretx = i
                    newOffset = True
                
                offsetx += thisW + self.charSpacing
            else: break
                
        if not newOffset:
            self.caretx = len(self.text)
    
    def __renderable_right(self):
        totalLen = 0
        totalCnt = 0        
        for i in range(len(self.text)):
            charw, charh = blf.dimensions(self.fid, self.text[i])
            totalLen += charw
            
            if totalLen > self.bounds[2]:
                return totalCnt
            else:
                totalCnt += 1
        return totalCnt
    
    @property
    def cursorPosition(self):
        return self.caretx
    
    @cursorPosition.setter
    def cursorPosition(self, pos):
        if pos < 0:
            self.caretx = 0
        elif pos > len(self.text):
            self.caretx = len(self.text)
        else:
            self.caretx = pos
    
    def draw(self):        
        if not self.visible: return

        PControl.new.draw(self)
        
        if self.theme == None:
            h_draw_quad_b(self.bounds, self.backColor, 2)
            h_clip_begin(self.bounds, padding=[1, 1, 1, 1])
        else:
            t = self.theme["panel_down"]
            h_draw_9patch_skin(t, self.bounds)
            h_clip_begin(self.bounds, padding=t["padding"])
        
        offx = 0
        
        for i in range(len(self.text)):
            charw, charh = blf.dimensions(self.fid, self.text[i])
            
            if offx+charw > self.bounds[2]: break
        
            ## Uncomment these lines to show each char collision box
            #
            #bnds = [self.bounds[0]+(offx + (charw+1) / 2), self.bounds[1], charw, self.bounds[3]]
            #bgl.glColor4f(*(0.0, 0.0, 1.0, 1.0))
            #h_draw_quad_wire(bnds)
            
            if not self.masked:
                h_draw_text(self.fid, self.text[i], [self.bounds[0]+offx, self.bounds[1], charw, self.bounds[3]], self.foreColor, margin=self.margin, font_size=self.fontSize, text_align=0, vertical_align=2, shadow=self.shadow, clip=False)
            else:
                charw, charh = blf.dimensions(self.fid, "*")
                h_draw_text(self.fid, "*", [self.bounds[0]+offx, self.bounds[1], charw, self.bounds[3]], self.foreColor, margin=self.margin, font_size=self.fontSize, text_align=0, vertical_align=2, shadow=self.shadow, clip=False)
            offx += charw + self.charSpacing
            
#        h_draw_text(self.fid, "cx: %d, ln: %d, lt: %d" % (self.caretx, len(self.text), (self.caretx < len(self.text))), [10, 200, 100, 22], self.foreColor, margin=0, font_size=14, text_align=0, vertical_align=2)
        if self.focused and self.blink and not self.readOnly:
            offx = 0
            txt = self.text+" "
            for i in range(len(txt)):
                charw, charh = blf.dimensions(self.fid, txt[i])
                if self.masked:
                    charw, charh = blf.dimensions(self.fid, "*")
                if i == self.caretx:
                    cx = self.bounds[0]+offx-3
                    if cx < self.bounds[0]+self.bounds[2]:
                        h_draw_text(self.fid, "|", [cx, self.bounds[1]-2, 1, self.bounds[3]], self.foreColor, margin=self.margin, font_size=self.fontSize, text_align=0, vertical_align=2, shadow=False, clip=False)
                    #break
                offx += charw + self.charSpacing
                
        h_clip_end()
import pgui.src.PRadio as PRadio

class PRadioGroup:
    def __init__(self):
        self.radios = []
        self.previous = None
    
    def addToGroup(self, rad):
        if not isinstance(rad, PRadio.new): return
        rad.group = self
        self.radios.append(rad)
        if self.nothingChecked() and len(self.radios):
            self.radios[0].checked = True
            self.previous = self.radios[0]
    
    def nothingChecked(self):
        notn = True
        for r in self.radios:
            if r.checked:
                notn = False
                break
        return notn
    
    def uncheckAll(self):
        for r in self.radios:
            r.checked = False

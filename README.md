# PGUI
Blender Game Engine GUI System

# Installing / Using

You need to make a folder named "pgui" and place all the contents of this repo and make sure this folder is in the same place as your game .exe.
You can permanently place the folder inside Blender's Lib folder, so whenever you save a game as .exe, the Lib folder will be automatically copied.
Then in your game make a script and just import the module:

```python
  from pgui import *
```

And start making awesome GUIs :)

# Basic GUI example
Rotate and change the color of a Cube
```python
from pgui import *
from bge import logic as g

# Events
def rotate_cube_left(sender, x, y, b):
    sender.cube.applyRotation([0.0, 0.0, 0.1], True)
    
def rotate_cube_right(sender, x, y, b):
    sender.cube.applyRotation([0.0, 0.0, -0.1], True)

def slide_col(sender, val):
    if "R" in sender.name:
        sender.cube.color[0] = val / 100
    elif "G" in sender.name:
        sender.cube.color[1] = val / 100
    elif "B" in sender.name:
        sender.cube.color[2] = val / 100

def draw(sender):
    pass

def main(cont):
    o = cont.owner
    cube = g.getCurrentScene().objects["Cube"]
    if "init" not in o:
        o["mgr"] = PManager.new()
        
        # Controls for the container
        C = {
            "rotate1": PButton.new(bounds=[10, 10, 90, 25], text="Rotate Left", text_align=1),
            "rotate2": PButton.new(bounds=[10, 40, 90, 25], text="Rotate Right", text_align=1),
            "sldR": PSlider.new(bounds=[10, 75, 90, 18]),
            "sldG": PSlider.new(bounds=[10, 105, 90, 18]),
            "sldB": PSlider.new(bounds=[10, 135, 90, 18]),
            "dd": PDropDown.new(bounds=[110, 10, 90, 18], text="Select")
        }
        
        # Controls for the manager
        MC = {
            "cont": PContainer.new(bounds=[10, 10, 210, 200])
        }
        
        # Add the controls to the container
        MC["cont"].controls = C
        
        # And the container to the manager...
        # You can also add the controls directly to the manager.
        o["mgr"].controls = MC
        
        # Add events to some controls...
        # Note that if you want to modify an object, 
        # You need to pass it to the control and
        # then access it in the function by doing
        # sender.object
        C["rotate1"].cube = cube
        C["rotate2"].cube = cube
        C["rotate1"].on_mouse_hold = rotate_cube_left
        C["rotate2"].on_mouse_hold = rotate_cube_right
                
        C["sldR"].cube = cube
        C["sldG"].cube = cube
        C["sldB"].cube = cube
        
        C["sldR"].on_value_change = slide_col
        C["sldG"].on_value_change = slide_col
        C["sldB"].on_value_change = slide_col
        
        o["init"] = 1
    else:
        # Update the manager and events.
        o["mgr"].update()
```

... Also please give credit to the original author ...

import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText 
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.gui.DirectGui import DirectFrame
 
myFrame = DirectFrame(frameColor=(0, 1, 0, 1),
                      frameSize=(-2, 2, -1, 1),
                      pos=(0, -1, -1.8))
                      
yourframe = DirectFrame(frameColor=(0, 1, 0, 1),
                        frameSize=(-2, 2, -1, 1),
                        pos=(0, -1, 1.8)) 
                 
 
# Callback function to set  text
def setText():
        bk_text = "Button"
       
 
# Add button
b = DirectButton(text = ("Button", "click!", "Button", "Button"), scale=.05, pos = (0,0,0.9), command=setText)
d = DirectButton(text = ("thing", "click!", "stuff", "other"), scale=.05, pos = (-0.9,0,-0.9), command=setText)                     
                     
                     
# Run the tutorial
run()
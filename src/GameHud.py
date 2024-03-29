import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from panda3d.core import WindowProperties
from panda3d.core import Filename,Shader
from panda3d.core import AmbientLight,PointLight
from panda3d.core import TextNode
from panda3d.core import Point3,Vec3,Vec4
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.filter.CommonFilters import *
from direct.task import Task #for update functions
import math, sys, random, time, os
from ActionCommand import *
from GrabBag import *
from PipeGeneric import *

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.gui.DirectGui import DirectFrame

class GameHUD:
     def __init__(self):
        #Creates the HUD elements.


        self.stabilityBar = OnscreenImage(image = "../images/100.png", pos = (1.2, 0, .1))
        self.stabilityBar.setScale(.05,1,.65)
        self.stabilityBar.setTransparency(TransparencyAttrib.MAlpha)

        self.actionCommand = OnscreenImage(image = '../images/open.png', pos = (.95, 0, -.75), scale = (0.33, 1, 0.2))
        self.actionCommand.setTransparency(TransparencyAttrib.MAlpha)

        self.score = OnscreenText(text = 'Score: 0', align = TextNode.ALeft, pos = (-1.3, -.9), scale = 0.10, fg = (1,1,1,1), mayChange = True)
        self.score.align = TextNode.ALeft
        self.score.setText('Depth: 0')
        #self.score.setScale(.2,.2,.2)

     def updateHud(self, NewStability, NewScore, NewActionCommand):
        #Updates the HUD using the inputted values.
        self.score.setText('Depth: ' + str(NewScore))

        if NewStability >= 100:
            self.stabilityBar.setImage('../images/100.png')
        elif NewStability >= 90:
            self.stabilityBar.setImage('../images/90.png')
        elif NewStability >= 80:
            self.stabilityBar.setImage('../images/80.png')
        elif NewStability >= 70:
            self.stabilityBar.setImage('../images/70.png')
        elif NewStability >= 60:
            self.stabilityBar.setImage('../images/60.png')
        elif NewStability >= 50:
            self.stabilityBar.setImage('../images/50.png')
        elif NewStability >= 40:
            self.stabilityBar.setImage('../images/40.png')
        elif NewStability >= 30:
            self.stabilityBar.setImage('../images/30.png')
        elif NewStability >= 20:
            self.stabilityBar.setImage('../images/20.png')
        elif NewStability >= 10:
            self.stabilityBar.setImage('../images/10.png')
        elif NewStability >= 0:
            self.stabilityBar.setImage('../images/0.png')

        if NewActionCommand == []:
            self.actionCommand.setImage('../images/open.png')
        elif NewActionCommand == ['l','d']:
            self.actionCommand.setImage('../images/left_down.png')
        elif NewActionCommand == ['r','d']:
            self.actionCommand.setImage('../images/right_down.png')
        elif NewActionCommand == ['l','u']:
            self.actionCommand.setImage('../images/left_up.png')
        elif NewActionCommand == ['r','u']:
            self.actionCommand.setImage('../images/right_up.png')
        elif NewActionCommand == ['u','d']:
            self.actionCommand.setImage('../images/up_down.png')
        elif NewActionCommand == ['l','r']:
            self.actionCommand.setImage('../images/left_right.png')

        self.actionCommand.setTransparency(TransparencyAttrib.MAlpha)



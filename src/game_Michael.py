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
from GameHud import *
from PipeGeneric import PipeGeneric
from PipeFire import PipeFire
from PipeGears import PipeGears
from PipeWires import PipeWires
from PipeSteam import PipeSteam

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.gui.DirectGui import DirectFrame


class World(DirectObject): #necessary to accept events
    def __init__(self):
        print "START THE GAAAAAME!"
        self.accept("space", self.StartGame)
        self.titleScreen = OnscreenImage(image = '../images/Title.png', scale = (1.3333333,1,1))
        self.titleScreen.setTransparency(TransparencyAttrib.MAlpha)

        #sound Effect
        self.fixSound1 = loader.loadSfx("../audio/repair1.wav")
        self.fixSound2 = loader.loadSfx("../audio/repair2.wav")
        self.fixSound3 = loader.loadSfx("../audio/repair3.wav")
        self.fixSound4 = loader.loadSfx("../audio/repair4.wav")


    def StartGame(self):

        self.titleScreen.destroy()
        #turn off default mouse control
        base.disableMouse()
        #add update tasks to taskManager
        taskMgr.add(self.keyEvents, "keyEventTask")
        taskMgr.add(self.loopMusic, "loopMusicTask")
        taskMgr.add(self.checkPipes2, "checkPipesTask")
        taskMgr.add(self.updateTimer, "timeTask")

        #Enables particle effects
        base.enableParticles()

        camera.setPosHpr(0, -18, 3, 0, 0, 0)
        self.keyMap = {"moveLeft":0, "moveRight":0, "moveUp":0, "moveDown":0, "drop":0, \
        "actionLeft":0, "actionRight":0, "actionDown":0, "actionUp":0}
        self.prevTime = 0

        #Sets initial collision state, will change name later
        self.numCollisions = 0
        self.currentPipe = False

        self.loadModels()
        self.setupLights()
        self.loadSound()
        self.setupCollisions()

        self.accept("escape", sys.exit) #message name, function to call, (optional) list of arguments to that function
        #useful interval methods:
        # loop, pause, resume, finish
        # start can optionally take arguments: starttime, endtime, playrate


        #for "continuous" control
        self.accept("space", self.setKey, ["drop", 1])
        self.accept("space-up", self.setKey, ["drop", 0])

        self.accept("arrow_up", self.setKey, ["actionUp", 1])
        self.accept("arrow_down", self.setKey, ["actionDown", 1])
        self.accept("arrow_left", self.setKey, ["actionLeft", 1])
        self.accept("arrow_right", self.setKey, ["actionRight", 1])
        self.accept("arrow_up-up", self.setKey, ["actionUp", 0])
        self.accept("arrow_down-up", self.setKey, ["actionDown", 0])
        self.accept("arrow_left-up", self.setKey, ["actionLeft", 0])
        self.accept("arrow_right-up", self.setKey, ["actionRight", 0])

        self.accept("w", self.setKey, ["moveUp", 1])
        self.accept("s", self.setKey, ["moveDown", 1])
        self.accept("a", self.setKey, ["moveLeft", 1])
        self.accept("d", self.setKey, ["moveRight", 1])
        self.accept("w-up", self.setKey, ["moveUp", 0])
        self.accept("s-up", self.setKey, ["moveDown", 0])
        self.accept("a-up", self.setKey, ["moveLeft", 0])
        self.accept("d-up", self.setKey, ["moveRight", 0])

        self.accept("spider-and-tube_collision", self.pipeCollide)

        self.DefaultTime = 1.4
        self.TimeLeft = self.DefaultTime
        self.TimerGoing = False

        #Set game over thing
        self.GameOver = False

        #Set gameplay variables to keep track of
        self.gameScore = 0
        self.playerStability = 100
        self.currentActionCommand = ActionCommand(0,"")
        self.currentActionCommand.isEmpty()

        #Create HUD and add it to task thing
        self.Hud = GameHUD()
        taskMgr.add(self.update_game_Hud, "updateHudTask")

        #Fog and changing background
        myFog = Fog("Fog Name")
        f = 0.05
        myFog.setColor(f,f,f)
        myFog.setExpDensity(.01)
        render.setFog(myFog)
        base.setBackgroundColor(f,f,f)

    def updateTimer(self,task):
        if self.TimerGoing == True:
            self.TimeLeft = self.TimeLeft - globalClock.getDt()
            if self.TimeLeft <= 0:
                print"-----------TIME UP!!!!!!!!!---------"
                print self.currentActionCommand.getCommand()
                if self.currentActionCommand.isEmpty() == False:
                    self.playerStability = self.playerStability - 10
                    if self.playerStability <= 0:
                        if self.GameOver == False:
                            #REPLACE TITLE.PNG WITH THE GAME OVER IMAGE!!!!!!
                            self.gameOverScreen = OnscreenImage(image = '../images/GameOver.png', scale = (1.3333333,1,1))
                            self.gameOverScreen.setTransparency(TransparencyAttrib.MAlpha)
                            self.GameOver = True
                            self.Hud.hide = True
                print "***Blanked Action Command***"
                self.currentActionCommand = ActionCommand(0,"")
                self.TimeLeft = self.DefaultTime
                self.TimerGoing = False
        return Task.cont

    def setKey(self, key, value):
        self.keyMap[key] = value

    def loadModels(self):
        """loads initial models into the world"""
        #load pipes
        self.numPipes = 6 #number appearing on the stage at any given time
        self.numGenericTypes = 5 #number of normal pipe models
        self.numSpecialTypes = 4 #number of 'broken' pipe models
        self.pipeGenericBag = GrabBag(self.numGenericTypes)
        self.pipeSpecialBag = GrabBag(self.numSpecialTypes)
        self.pipeList = []
        self.pipeInterval = 20.25*3.05#*.98 #length*timesLonger*overlapConstant
        self.pipeDepth = 0
        self.pipeCycle = 1

        #create initial pipes
        for i in range(self.numPipes):
            self.createPipe2(i)
            #print self.pipeList[i].model.getY()

        #Enable initial shaders
        self.pipeList[0].addShader()
        self.pipeList[1].addShader()

        #load spider
        #self.spider = loader.loadModel("../models/spider.egg")
        self.spider = Actor("../models/spider.egg", {"spider mechanicWITHRIG2013animuted_temp":"../models/animation_fall cycle.egg"})
        self.spider.loop("spider mechanicWITHRIG2013animuted_temp")
        self.spider.reparentTo(render)
        self.spider.setShaderAuto()
        self.spider.setScale(.045)
        self.spider.setZ(4.25)
        self.spider.setH(180)
        self.spider.setP(-65)

        #load back panal
        self.backPanal = loader.loadModel("../models/infinity.egg")
        self.backPanal.reparentTo(render)
        self.backPanal.setZ(4.25)
        self.backPanal.setY(self.pipeInterval*5*.90)


    def loadSound(self):
        self.openingMusic = loader.loadSfx("../audio/opening.wav")
        self.mainLoopMusic = loader.loadSfx("../audio/mainLoop.wav")
        SoundInterval(self.openingMusic).start()


    def setupLights(self):
        """loads initial lighting"""
        self.ambientLight = AmbientLight("ambientLight")
        #for setting colors, alpha is largely irrelevant
        self.ambientLight.setColor((.25, .25, .35, 1.0))
        #self.ambientLight.setColor((.25, .25, .25, 1.0))
        #create a NodePath, and attach it directly into the scene
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the node that calls setLight is what's illuminated by the given light
        #you can use clearLight() to turn it off
        render.setLight(self.ambientLightNP)

        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.7, .5, .5, 1))
        #self.dirLight.setColor((.7, .7, 1, 1))
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0, -25, 0)
        render.setLight(self.dirLightNP)

    def setupCollisions(self):
        #make a collision traverser, set it to default
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        #set the pattern for the event sent on collision
        # "%in" is substituted with the name of the into object
        self.cHandler.setInPattern("%fn-and-%in")

        cSphere = CollisionSphere((0,-5,0), 30)
        cNode = CollisionNode("spider")
        cNode.addSolid(cSphere)
        #spider is *only* a from object
        cNode.setIntoCollideMask(BitMask32.allOff())
        self.spiderCollisionNode = self.spider.attachNewNode(cNode)

        #self.spiderCollisionNode.show()
        base.cTrav.addCollider(self.spiderCollisionNode, self.cHandler)


    def pipeCollide(self, cEntry):
        self.numCollisions += 1
        print self.numCollisions
        #print cEntry.getIntoNodePath().getParent().getParent().getName()
        #print "\n\n\n"
        modelKey = cEntry.getIntoNodePath().getParent().getParent().getKey()
        self.currentPipe = self.getPipe(modelKey)
        if self.currentPipe.actionCommand.isEmpty() == False:
            print "Pipe Action Command = " + str(self.currentPipe.actionCommand.getCommand())
            self.currentActionCommand = ActionCommand(2,"",self.currentPipe.actionCommand.getCommand())
            print "Player Action Command = " + str(self.currentActionCommand.getCommand())
            self.currentPipe.actionCommand.blankCommand()
            print "Player Action Command = " + str(self.currentActionCommand.getCommand())

            print "------!!!!!!!!!!!!!------"

            if self.TimerGoing == False:
                self.TimeLeft = self.DefaultTime
                self.TimerGoing = True


    # def getPipe(self, modelPath, model):
        # modelPath += model
        # print modelPath
        # for i in range(self.pipeList.__len__()):
            # print self.pipeList[i].fileName
            # if self.pipeList[i].fileName == modelPath: return(self.pipeList[i])

    def getPipe(self, model):
        modelPath = model
        print modelPath
        print "CollideKey: " + str(modelPath)
        #KeyTestDebug
        for i in range(self.pipeList.__len__()):
            print "Key "+ str(i) +":" + str(self.pipeList[i].key)
        for i in range(self.pipeList.__len__()):
            print "Testing Key: " + str(self.pipeList[i].key)
            if self.pipeList[i].key == modelPath: return(self.pipeList[i])

    def update_game_Hud(self,task):
        self.gameScore = self.gameScore + globalClock.getDt()
        tempScore = int(self.gameScore * 100)
        self.Hud.updateHud(self.playerStability,tempScore,self.currentActionCommand.getOriginal())
        return Task.cont

import updateWorld_Michael as updateWorld
World.keyEvents = updateWorld.keyEvents
World.adjustCamera = updateWorld.adjustCamera
World.loopMusic = updateWorld.loopMusic
# World.checkPipes = updateWorld.checkPipes
# World.createPipe = updateWorld.createPipe
World.checkPipes2 = updateWorld.checkPipes2
World.createPipe2 = updateWorld.createPipe2

world = World()
run()
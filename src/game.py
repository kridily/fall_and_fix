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


class World(DirectObject): #necessary to accept events
    def __init__(self):
        #turn off default mouse control
        base.disableMouse()
        #add update tasks to taskManager
        taskMgr.add(self.keyEvents, "keyEventTask")
        taskMgr.add(self.loopMusic, "loopMusicTask")
        taskMgr.add(self.checkPipes, "checkPipesTask")
        
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
        
       
    
    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def loadModels(self):
        """loads initial models into the world"""
        #load pipes
        self.numPipes = 6
        self.numGenericTypes = 5
        self.numSpecialPipes = 4
        
        self.pipeGenericBag = GrabBag(self.numTypes)        
        self.pipeList = []
        self.pipeInterval = 20.25*3.05*.98 #length*timesLonger*overlapConstant
        self.pipeDepth = 0
        
        
        #create initial pipes
        for i in range(self.numPipes):            
            self.createPipe(i)
            #print self.pipeList[i].model.getY()
        
        #Enable initial shaders
        self.pipeList[0].addShader()
        self.pipeList[1].addShader()
        
        #load spider
        self.spider = loader.loadModel("../models/spider.egg")
        self.spider.reparentTo(render)
        self.spider.setScale(.045)
        self.spider.setZ(4.25)
        self.spider.setH(180)
        self.spider.setP(-65)

        
            
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
        model = cEntry.getIntoNodePath().getTop().find("**/*.egg").getName()
        self.currentPipe = self.getPipe("../models/", model)
        print self.currentPipe.actionCommand.getCommand()
        print "------!!!!!!!!!!!!!------"
        
    
    def getPipe(self, modelPath, model):
        modelPath += model
        print modelPath
        for i in range(self.pipeList.__len__()):
            print self.pipeList[i].fileName
            if self.pipeList[i].fileName == modelPath: return(self.pipeList[i])
        
        
        
import updateWorld
World.keyEvents = updateWorld.keyEvents
World.adjustCamera = updateWorld.adjustCamera
World.loopMusic = updateWorld.loopMusic
World.checkPipes = updateWorld.checkPipes
World.createPipe = updateWorld.createPipe

world = World()
run()
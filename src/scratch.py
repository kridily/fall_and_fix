import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
import math, sys, random, time
from GrabBag import *


class World(DirectObject): #necessary to accept events
    def __init__(self):
        #turn off default mouse control
        base.disableMouse()
        #add update tasks to taskManager
        taskMgr.add(self.keyEvents, "keyEventTask")
        taskMgr.add(self.loopMusic, "loopMusicTask")
        taskMgr.add(self.checkPipes, "checkPipesTask")
        
        
        camera.setPosHpr(0, -18, 3, 0, 0, 0)
        self.keyMap = {"moveLeft":0, "moveRight":0, "moveUp":0, "moveDown":0, "drop":0}
        self.prevTime = 0
                
        self.loadModels()
        #camera.lookAt(self.spider)
            
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
        # self.accept("arrow_up", self.setKey, ["moveUp", 1])
        # self.accept("arrow_down", self.setKey, ["moveDown", 1])
        # self.accept("arrow_left", self.setKey, ["moveLeft", 1])
        # self.accept("arrow_right", self.setKey, ["moveRight", 1])
        # self.accept("arrow_up-up", self.setKey, ["moveUp", 0])
        # self.accept("arrow_down-up", self.setKey, ["moveDown", 0])
        # self.accept("arrow_left-up", self.setKey, ["moveLeft", 0])
        # self.accept("arrow_right-up", self.setKey, ["moveRight", 0])
        
        self.accept("w", self.setKey, ["moveUp", 1])
        self.accept("s", self.setKey, ["moveDown", 1])
        self.accept("a", self.setKey, ["moveLeft", 1])
        self.accept("d", self.setKey, ["moveRight", 1])
        self.accept("w-up", self.setKey, ["moveUp", 0])
        self.accept("s-up", self.setKey, ["moveDown", 0])
        self.accept("a-up", self.setKey, ["moveLeft", 0])
        self.accept("d-up", self.setKey, ["moveRight", 0])
        
        self.accept("ate-smiley", self.eat)
        
        #self.env.setShaderAuto()
        self.shaderenable = 1
    
    
    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def loadModels(self):
        """loads initial models into the world"""
        #load pipes
        self.numPipes = 6
        self.numTypes = 6
        self.pipeBag = GrabBag(self.numTypes)
        self.pipeList = []
        self.pipeInterval = 20.25*3.05#*.90 #length*timesLonger*overlapConstant
        self.pipeDepth = 0
        
        self.redHelperList = []
        self.redLightList = []
        for i in range(self.numPipes):
            self.createPipe(i)   
                
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
        self.ambientLight.setColor((.25, .25, .25, 1.0))
        #create a NodePath, and attach it directly into the scene
        self.ambientLightNP = render.attachNewNode(self.ambientLight)
        #the node that calls setLight is what's illuminated by the given light
        #you can use clearLight() to turn it off
        render.setLight(self.ambientLightNP)
        
        self.dirLight = DirectionalLight("dirLight")
        self.dirLight.setColor((.7, .7, 1, 1))
        self.dirLightNP = render.attachNewNode(self.dirLight)
        self.dirLightNP.setHpr(0, -25, 0)
        render.setLight(self.dirLightNP)
        
    
        
    def addPointLight(self, pipe):    
        """create a point light for pipe"""      
        
        #The redpoint light and helper
        gb = random.uniform(0, 300) / 1000
        r = random.uniform(700, 900) / 1000        
        helper = loader.loadModel("../models/sphere.egg.pz")
        
        helper.setColor( Vec4( r, gb, gb, 1 ) )      
        helper.setPos(pipe.getPos())
        print helper.getColor()
        helper.setScale(.25*0)
        #optionally set location of light within pipe
        helper.setY(helper.getY()-50*35 ) #moves to inbetween segments
        #helper.setZ(helper.getZ()-50*6 ) #makes 3 sided lights
        
        light = helper.attachNewNode( PointLight( "light" ) )
        light.node().setAttenuation( Vec3( .1, 0.04, 0.0 )/2 )                   
        light.node().setColor( Vec4( r, gb, gb, 1 ) )
        light.node().setSpecularColor( Vec4( 1 ) )
        helper.reparentTo( pipe )
        render.setLight( light )
        
        self.redHelperList.append(helper)
        self.redLightList.append(light)
   
    
    def setupCollisions(self):
        #make a collision traverser, set it to default
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        #set the pattern for the event sent on collision
        # "%in" is substituted with the name of the into object
        self.cHandler.setInPattern("ate-%in")
        
        cSphere = CollisionSphere((0,-5,0), 40)
        cNode = CollisionNode("spider")
        cNode.addSolid(cSphere)
        #spider is *only* a from object
        cNode.setIntoCollideMask(BitMask32.allOff())
        cNodePath = self.spider.attachNewNode(cNode)
        #cNodePath.show()
        base.cTrav.addCollider(cNodePath, self.cHandler)
        
        # for pipe in self.pipeList:
            # cSphere = CollisionSphere((0,0,0), 100)
            # cNode = CollisionNode("smiley")
            # cNode.addSolid(cSphere)
            # cNodePath = pipe.attachNewNode(cNode)
            # cNodePath.show()
        
    def eat(self, cEntry):
        self.targets.remove(cEntry.getIntoNodePath().getParent())
        cEntry.getIntoNodePath().getParent().remove()
        n = random.uniform(0,1)
        if n < .5:
            sound = loader.loadSfx("assets/bubbles1.wav")
        else:
            sound = loader.loadSfx("assets/bubbles2.wav")
        SoundInterval(sound).start()
        
import updateWorld
World.keyEvents = updateWorld.keyEvents
World.adjustCamera = updateWorld.adjustCamera
World.loopMusic = updateWorld.loopMusic
World.checkPipes = updateWorld.checkPipes
World.createPipe = updateWorld.createPipe

w = World()
run()
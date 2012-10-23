import direct.directbase.DirectStart #starts Panda
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions
import math, sys, random
from GrabBag import *


class World(DirectObject): #necessary to accept events
    def __init__(self):
        #turn off default mouse control
        base.disableMouse()
        
        camera.setPosHpr(0, -18, 3, 0, 0, 0)
        self.keyMap = {"moveLeft":0, "moveRight":0, "moveUp":0, "moveDown":0, "drop":0}
        self.prevTime = 0
        taskMgr.add(self.move, "moveTask")
        
        self.loadModels()
            
        self.setupLights()
        #self.setupLights2()
        
        self.loadSound()
                
        #self.setupCollisions()
      
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
        self.pipeInterval = 20.25*3.05
        
        for i in range(self.numPipes):
            filename = ["../models/tunnelWallTemp"]
            filename.append(str(self.pipeBag.pick()-1))
            filename.append(".egg")
            filename = ''.join(filename)
            
            pipe = loader.loadModel(filename)
            pipe.setScale(.0175)
            pipe.setPos(0, i*self.pipeInterval, 0)
            pipe.reparentTo(render)
            self.pipeList.append(pipe)
        
        self.pipeDepth = 0
        
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
        
        #The blue point light and helper
        helper = loader.loadModel("assets/maya/sphere.egg.pz")
        helper.setColor( Vec4( 1, 0, 0, 1 ) )        
        helper.setPos(pipe.getPos())
        print helper.getPos()
        helper.setScale(.25)
        light = helper.attachNewNode( PointLight( "light" ) )
        light.node().setAttenuation( Vec3( .1, 0.04, 0.0 ) )
        gb = random.uniform(0, 600) / 1000
        r = random.uniform(700, 900) / 1000            
        light.node().setColor( Vec4( r, gb, gb, 1 ) )
        light.node().setSpecularColor( Vec4( 1 ) )
        helper.reparentTo( pipe )
        render.setLight( light )       
   
    

    def move(self, task):
        """compound interval for walking"""
        dt = task.time - self.prevTime
        #stuff and things
        
        #comment this line to debug camera
        self.adjustCamera()
        
        if self.openingMusic.status() != self.openingMusic.PLAYING:
            if self.mainLoopMusic.status() != self.mainLoopMusic.PLAYING:
                SoundInterval(self.mainLoopMusic).loop()
      
        self.pipeDepth = self.pipeList[0].getY()
        #print self.pipeDepth
        if self.pipeDepth < -1*self.pipeInterval:
            self.pipeList[0].removeNode()
            self.pipeList.pop(0)
            
            #pick file
            filename = ["../models/tunnelWallTemp"]
            filename.append(str(self.pipeBag.pick()-1))
            filename.append(".egg")
            filename = ''.join(filename)
            
            #load file
            pipe = loader.loadModel(filename)
            pipe.setScale(.0175)
            # pipe.setR(random.randint(0,3)*90)
            # print pipe.getR()
            pipe.setPos(0, self.pipeList[self.pipeList.__len__()-1].getY() + self.pipeInterval, 0)
            
            if filename == "tunnelWallTemp5.egg":
                addPointLight(pipe)
            pipe.reparentTo(render)
            self.pipeList.append(pipe)            
           
        
        if self.keyMap["drop"] == 0:
            for i in range(self.pipeList.__len__()):
                self.pipeList[i].setY(self.pipeList[i].getY() - dt*100)            
        
        dist = .1
        if self.keyMap["moveLeft"] == 1:          
            self.spider.setHpr(-115, 0, 90)
            if self.spider.getX() > -2.0:
                self.spider.setX(self.spider.getX()-1*dist)
        if self.keyMap["moveRight"] == 1: 
            self.spider.setHpr(115, -0, -90)
            if self.spider.getX() < 2.0:
                self.spider.setX(self.spider.getX()+1*dist)            
        if self.keyMap["moveUp"] == 1:
            self.spider.setHpr(180, -65, 0)
            if self.spider.getZ() < 6.45:
                self.spider.setZ(self.spider.getZ()+1*dist)            
        if self.keyMap["moveDown"] == 1:
            self.spider.setHpr(180, 65, 180)
            if self.spider.getZ() > 2.6:            
                self.spider.setZ(self.spider.getZ()-1*dist)
        #print self.spider.getPos()
               
        
        self.prevTime = task.time
        return Task.cont
        
    def adjustCamera (self):
        camvec = self.spider.getPos() - camera.getPos()
        #camH = camera.getH() - self.spider.getH()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()

        if (camdist > -10.0):
            camera.setPos(camera.getPos() + camvec * (camdist - 20))
        elif (camdist < -15.0):
            camera.setPos(camera.getPos() - camvec * (15 - camdist))

        dirVec = self.spider.getPos(render) - camera.getPos()
        dirVec.setZ(0)
        turnRate = 0.1
        camera.setPos(camera.getPos() + (dirVec * turnRate))
        camera.setZ(4.5)
        camera.lookAt(self.spider)

        
    def setupCollisions(self):
        #make a collision traverser, set it to default
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        #set the pattern for the event sent on collision
        # "%in" is substituted with the name of the into object
        self.cHandler.setInPattern("ate-%in")
        
        cSphere = CollisionSphere((0,-.25,-1.1), 7.3)
        cNode = CollisionNode("spider")
        cNode.addSolid(cSphere)
        #spider is *only* a from object
        cNode.setIntoCollideMask(BitMask32.allOff())
        cNodePath = self.spider.attachNewNode(cNode)
        #cNodePath.show()
        base.cTrav.addCollider(cNodePath, self.cHandler)
        
        for target in self.targets:
            cSphere = CollisionSphere((0,0,4), 6)
            cNode = CollisionNode("smiley")
            cNode.addSolid(cSphere)
            cNodePath = target.attachNewNode(cNode)
            #cNodePath.show()
        
    def eat(self, cEntry):
        self.targets.remove(cEntry.getIntoNodePath().getParent())
        cEntry.getIntoNodePath().getParent().remove()
        n = random.uniform(0,1)
        if n < .5:
            sound = loader.loadSfx("assets/bubbles1.wav")
        else:
            sound = loader.loadSfx("assets/bubbles2.wav")
        SoundInterval(sound).start()
        
        
w = World()
run()
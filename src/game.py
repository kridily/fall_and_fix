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
        #otherwise we can't position the camera
        base.disableMouse()
        camera.setPosHpr(0, -18, 3, 0, 0, 0)
        self.keyMap = {"left":0, "right":0, "forward":0, "back":0, "drop":0}
        self.prevTime = 0
        taskMgr.add(self.move, "moveTask")
        
        self.loadModels()
        #camera.lookAt(self.panda)
    
        self.setupLights()
        #self.setupLights2()
        
        self.loadSound()
        #self.intervalFish()
        
        #self.setupCollisions()
      
        self.accept("escape", sys.exit) #message name, function to call, (optional) list of arguments to that function
        #self.accept("arrow_up", self.walk)
        #other useful interval methods:
        # loop, pause, resume, finish
        # start can optionally take arguments: starttime, endtime, playrate
        
        #for fixed interval movement
        #self.accept("arrow_left", self.turn, [-1]) #yes, you have to use a list, event if the function only takes one argument
        #self.accept("arrow_right", self.turn, [1])
        
        #for "continuous" control
        self.accept("space", self.setKey, ["drop", 1])
        self.accept("space-up", self.setKey, ["drop", 0])
        # self.accept("arrow_up", self.setKey, ["forward", 1])
        # self.accept("arrow_down", self.setKey, ["back", 1])
        # self.accept("arrow_left", self.setKey, ["left", 1])
        # self.accept("arrow_right", self.setKey, ["right", 1])
        # self.accept("arrow_up-up", self.setKey, ["forward", 0])
        # self.accept("arrow_down-up", self.setKey, ["back", 0])
        # self.accept("arrow_left-up", self.setKey, ["left", 0])
        # self.accept("arrow_right-up", self.setKey, ["right", 0])
        
        self.accept("w", self.setKey, ["forward", 1])
        self.accept("s", self.setKey, ["back", 1])
        self.accept("a", self.setKey, ["left", 1])
        self.accept("d", self.setKey, ["right", 1])
        self.accept("w-up", self.setKey, ["forward", 0])
        self.accept("s-up", self.setKey, ["back", 0])
        self.accept("a-up", self.setKey, ["left", 0])
        self.accept("d-up", self.setKey, ["right", 0])
        
        self.accept("ate-smiley", self.eat)
        
        #self.env.setShaderAuto()
        self.shaderenable = 1
    
    def setKey(self, key, value):
        self.keyMap[key] = value
        
    def loadModels(self):
        """loads initial models into the world"""
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
        
        self.panda = loader.loadModel("../models/spider.egg")
        self.panda.reparentTo(render)
        self.panda.setScale(.045)
        self.panda.setZ(3.5)
        self.panda.setH(180)
        self.panda.setP(-65)

        
            
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
        
        
        # # Now we create a spotlight. Spotlights light objects in a given cone
        # # They are good for simulating things like flashlights
        # self.spotlight = render.attachNewNode( Spotlight( "spotlight" ) )
        # self.spotlight.node().setColor( Vec4( .7, .7, 1, 1 ) )
        # self.spotlight.setPos(self.panda.getX(), self.panda.getY()+10, self.panda.getZ()+2)
        # self.spotlight.setHpr(180,-7,0)
        # #The cone of a spotlight is controlled by it's lens. This creates the lens
        # self.spotlight.node().setLens( PerspectiveLens() )
        # #This sets the Field of View (fov) of the lens, in degrees for width and
        # #height. The lower the numbers, the tighter the spotlight.
        # self.spotlight.node().getLens().setFov( 6, 6 )
        # # Attenuation controls how the light fades with distance. The numbers are
        # # The three values represent the three constants (constant, linear, and
        # # quadratic) in the internal lighting equation. The higher the numbers the
        # # shorter the light goes.
        # self.spotlight.node().setAttenuation( Vec3( 1, 0, 0 ) ) 
        # # This exponent value sets how soft the edge of the spotlight is. 0 means a
        # # hard edge. 128 means a very soft edge.
        # self.spotlight.node().setExponent( 60.0 )
        # self.spotlight.reparentTo( self.panda )
        # render.setLight( self.spotlight )
        
        
        """
        self.headLight = loader.loadModel("assets/maya/sphere.egg.pz")
        self.headLight.setColor( Vec4( .9, 0, 0, 1 ) )
        self.headLight.setPos(self.panda.getX(), self.panda.getY()+20, self.panda.getZ()+2)
        self.headLight.setScale(.2)
        self.headPointLight = self.headLight.attachNewNode( PointLight( "headPointLight" ) )
        self.headPointLight.node().setAttenuation( Vec3( .1, 0.04, 0.0 ) ) 
        self.headPointLight.node().setColor( Vec4( .9, 0, 0, 1 ) )
        #self.headPointLight.node().setSpecularColor( Vec4( 1 ) )
        render.setLight(self.headPointLight)
        """
                
        #The blue point light and helper
        # self.blueLightsStatic = []
        # for i in range(8):
            # self.blueHelper = loader.loadModel("assets/maya/sphere.egg.pz")
            # rg = random.uniform(0, 600) / 1000
            # b = random.uniform(700, 900) / 1000
            # self.blueHelper.setColor( Vec4( rg, rg, b, 1 ) )
            # radius = 250
            # self.blueHelper.setPos(random.uniform(-250, 250), random.uniform(-250, 250), 12)
            # self.blueHelper.setScale(40)
            # self.bluePointLight = self.blueHelper.attachNewNode( PointLight( "bluePointLight" ) )
            # self.bluePointLight.node().setAttenuation( Vec3( .7, 0.04, 0.0 ) ) 
            # self.bluePointLight.node().setColor( Vec4( rg, rg, b, 1 ) )
            # self.bluePointLight.node().setSpecularColor( Vec4( 1 ) )
            # render.setLight(self.bluePointLight)
            # self.blueLightsStatic.append(self.bluePointLight)
                        
        # for i in range(8):
            # print self.blueLightsStatic[i].node().getColor()
            
        
    def setupLights2(self):    
        """Now we create moving Point lights."""
                
        #Create a dummy node so the lights can be spun with one command
        self.pointLightHelper = render.attachNewNode( "pointLightHelper" )
        self.pointLightHelper.setPos(0, 50, 8)
        
        self.blueLights = []
        for i in range(7):
            #The blue point light and helper
            self.blueHelper = loader.loadModel("assets/maya/sphere.egg.pz")
            #self.blueHelper.setColor( Vec4( 0, 0, 1, 1 ) )
            self.blueHelper.setTransparency(0)
            self.blueHelper.setPos(random.uniform(-150, 150), random.uniform(-150, 150), 8 )
            self.blueHelper.setScale(.25)
            self.bluePointLight = self.blueHelper.attachNewNode( PointLight( "bluePointLight" ) )
            self.bluePointLight.node().setAttenuation( Vec3( .1, 0.04, 0.0 ) )
            rg = random.uniform(0, 600) / 1000
            b = random.uniform(700, 900) / 1000            
            self.bluePointLight.node().setColor( Vec4( rg, rg, b, 1 ) )
            self.bluePointLight.node().setSpecularColor( Vec4( 1 ) )
            self.blueHelper.reparentTo( self.pointLightHelper )
            self.blueLights.append(self.blueHelper)
            render.setLight( self.bluePointLight )       

        # Create and start interval to spin the lights, and a variable to
        # manage them.
        self.pointLightsSpin = self.pointLightHelper.hprInterval(15, Vec3(360, 0, 0))
        self.pointLightsSpin.loop()
    
    def intervalFish(self):
        for i in range(self.targets.__len__()):
            len = random.uniform(.4,2)
            self.pitch1 = self.targets[i].hprInterval(len, Vec3(0, 30, 0))
            self.pitch2 = self.targets[i].hprInterval(len*2, Vec3(0, -30, 0))
            self.pitch3 = self.targets[i].hprInterval(len, Vec3(0, 0, 0))
            self.spin1 = self.targets[i].hprInterval(len*3, Vec3(360, 0, 0))
            
            Parallel(
                Sequence(
                    self.pitch1,                    
                    self.pitch2,
                    self.pitch3
                ),
                self.spin1
            ).loop()            
            

    def moveFish(self, dt):
        x = self.targets.__len__()
        for i in range(x):
            #self.targets[i].setH(self.targets[i].getH() + dt*100)
            dist = random.uniform(.1, .4)
            angle = deg2Rad(self.targets[i].getH())
            dx = dist * math.sin(angle)
            dy = dist * -math.cos(angle)
            self.targets[i].setX(self.targets[i].getX() + dx) 
            self.targets[i].setY(self.targets[i].getY() + dy)
    
    def move(self, task):
        """compound interval for walking"""
        dt = task.time - self.prevTime
        #stuff and things
        
        #comment this line to debug camera
        self.adjustCamera()
        #self.moveFish(dt)
        if self.openingMusic.status() != self.openingMusic.PLAYING:
            if self.mainLoopMusic.status() != self.mainLoopMusic.PLAYING:
                SoundInterval(self.mainLoopMusic).loop()
        #self.spotlight.setPos(self.panda.getX(), self.panda.getY()+10, self.panda.getZ()+2)
        
        
        self.pipeDepth = self.pipeList[0].getY()
        #print self.pipeDepth
        if self.pipeDepth < -1*self.pipeInterval:
            self.pipeList[0].removeNode()
            self.pipeList.pop(0)
        
            filename = ["../models/tunnelWallTemp"]
            filename.append(str(self.pipeBag.pick()-1))
            filename.append(".egg")
            filename = ''.join(filename)
            
            pipe = loader.loadModel(filename)
            pipe.setScale(.0175)
            pipe.setPos(0, self.pipeList[self.pipeList.__len__()-1].getY() + self.pipeInterval, 0)
            pipe.reparentTo(render)
            self.pipeList.append(pipe)
           
        
        if self.keyMap["drop"] == 0:
            for i in range(self.pipeList.__len__()):
                self.pipeList[i].setY(self.pipeList[i].getY() - dt*100)            
        
        dist = .1
        if self.keyMap["left"] == 1:            
            self.panda.setHpr(-115, 0, 90)
            self.panda.setX(self.panda.getX()-1*dist)
        if self.keyMap["right"] == 1:
            self.panda.setHpr(115, -0, -90)
            self.panda.setX(self.panda.getX()+1*dist)            
        if self.keyMap["forward"] == 1:
            dist = .1
            #self.panda.setHpr(self.panda.getHpr()+1)
            self.panda.setHpr(180, -65, 0)
            #self.panda.setHpr(542,295,360)            
            self.panda.setZ(self.panda.getZ()+1*dist)            
        if self.keyMap["back"] == 1:
            dist = .1
            #self.panda.setHpr(self.panda.getHpr()+1)
            #self.panda.setH(self.panda.getH()+180)
            self.panda.setHpr(180, 65, 180)
            print self.panda.getHpr()
            self.panda.setZ(self.panda.getZ()-1*dist)
          
        
        self.prevTime = task.time
        return Task.cont
        
    def adjustCamera (self):
        camvec = self.panda.getPos() - camera.getPos()
        #camH = camera.getH() - self.panda.getH()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()

        if (camdist > -10.0):
            camera.setPos(camera.getPos() + camvec * (camdist - 20))
        elif (camdist < -15.0):
            camera.setPos(camera.getPos() - camvec * (15 - camdist))

        dirVec = self.panda.getPos(render) - camera.getPos()
        dirVec.setZ(0)
        turnRate = 0.1
        camera.setPos(camera.getPos() + (dirVec * turnRate))
        camera.setZ(4.5)
        #camera.lookAt(self.panda)

        
    def setupCollisions(self):
        #make a collision traverser, set it to default
        base.cTrav = CollisionTraverser()
        self.cHandler = CollisionHandlerEvent()
        #set the pattern for the event sent on collision
        # "%in" is substituted with the name of the into object
        self.cHandler.setInPattern("ate-%in")
        
        cSphere = CollisionSphere((0,-.25,-1.1), 7.3) #panda is scaled way down!
        cNode = CollisionNode("panda")
        cNode.addSolid(cSphere)
        #panda is *only* a from object
        cNode.setIntoCollideMask(BitMask32.allOff())
        cNodePath = self.panda.attachNewNode(cNode)
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
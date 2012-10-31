"""
This File is to define all update tasks that take place
every frame, and in game.py will be refered to
as though they are world methods (ie. self.x).
"""
from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.actor.Actor import Actor #for animated models
from direct.interval.IntervalGlobal import * #for compound intervals
from direct.task import Task #for update functions

from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from panda3d.core import TextNode
from panda3d.core import AmbientLight,DirectionalLight,PointLight
from panda3d.core import Point3,Vec3,Vec4
from panda3d.core import Filename, Shader
from panda3d.core import WindowProperties

from direct.filter.CommonFilters import *
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText

from ActionCommand import *
from GrabBag import *
from GameHud import *
from PipeGeneric import PipeGeneric
from PipeFire import PipeFire
from PipeGears import PipeGears
from PipeWires import PipeWires
from PipeSteam import PipeSteam


import math, sys, random, time
from GrabBag import *

def keyEvents(self, task):
    """defines all keypress events"""
    dt = task.time - self.prevTime


    if self.keyMap["drop"] == 0:
        for i in range(self.pipeList.__len__()):
            self.pipeList[i].model.setY(self.pipeList[i].model.getY() - dt*100*1.0)
    if self.keyMap["drop"] == 1:
        for i in range(self.pipeList.__len__()):
            pass
            #self.pipeList[i].model.setR(self.pipeList[i].model.getR() + dt*20*i)

    dist = .135
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
        if self.spider.getZ() < 6.1:
            self.spider.setZ(self.spider.getZ()+1*dist)
    if self.keyMap["moveDown"] == 1:
        self.spider.setHpr(180, 65, 180)
        if self.spider.getZ() > 2.6:
            self.spider.setZ(self.spider.getZ()-1*dist)
    #print self.spider.getPos()

    self.adjustCamera()

    if self.keyMap["actionLeft"] == 1:
        print "actionLeft"
        self.keyMap["actionLeft"] = 0
    if self.keyMap["actionRight"] == 1:
        print "actionRight"
        self.keyMap["actionRight"] = 0
    if self.keyMap["actionUp"] == 1:
        print "actionUp"
        self.keyMap["actionUp"] = 0
    if self.keyMap["actionDown"] == 1:
        print "actionDown"
        self.keyMap["actionDown"] = 0


    self.prevTime = task.time
    return Task.cont


def adjustCamera(self):
    camvec = self.spider.getPos() - camera.getPos()
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


def loopMusic(self, task):
    if self.openingMusic.status() != self.openingMusic.PLAYING:
            if self.mainLoopMusic.status() != self.mainLoopMusic.PLAYING:
                SoundInterval(self.mainLoopMusic).loop()

    return Task.cont

def checkPipes(self, task):
    self.pipeDepth = self.pipeList[0].model.getY()
    #print self.pipeDepth
    if self.pipeDepth < -1*self.pipeInterval:
        
        self.pipeCycle += 1
        print self.pipeCycle
        print self.pipeCycle % 7
        print "\n"        
        
        #check pipe cycle state
        if self.pipeCycle % 7 >= 2:
        #recycle pipe
            self.createPipe(-5, self.pipeList[0])
            self.pipeList.pop(0)
        elif self.pipeCycle % 7 == 0:
        #spawn broken pipe            
            type = self.pipeSpecialBag.pick() *-1
            print "type" + str(type)
            self.createPipe(type)
            self.pipeList.pop(0)
        elif self.pipeCycle % 7 == 1:
        #spawn generic pipe            
            self.createPipe(-6)
            self.pipeList.pop(0)
            
        #Enable shaders for the first two pipe segments
        if not self.pipeList[0].shaderEnabled: self.pipeList[0].addShader()
        if not self.pipeList[1].shaderEnabled: self.pipeList[1].addShader()


    return Task.cont

def createPipe(self, i, pipe = False):
    print "i = " + str(i) + "!!!!!!"
    if i >= 0: #only in initial world.loadModels()
    #create new generic pipe
       pipe = PipeFire()#Generic(self.pipeGenericBag)
    #set position in queue
       pipe.model.setPos(0, i*self.pipeInterval, 4.25)
    elif i == -5:
    #recycle pipe
        pipe.recycle()
        pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
        + self.pipeInterval, 4.25)
    elif i == -6:
    #create new generic pipe
        pipe = PipeFire()#Generic(self.pipeGenericBag)
    #set position in queue
        pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
        + self.pipeInterval, 4.25)
    elif i == -1:
    #create Steam pipe
        pipe = PipeFire()
        #self.loadParticleConfig(pipe, '../models/','steam.ptf')
    #set position in queue
        pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
        + self.pipeInterval, 4.25)    
    elif i == -2:
    #create Steam pipe
        pipe = PipeFire()
        #self.loadParticleConfig(pipe, '../models/','spark.ptf')
    #set position in queue
        pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
        + self.pipeInterval, 4.25)    
    elif i == -3:
    #create Steam pipe
        pipe = PipeFire()
        #self.loadParticleConfig(pipe, '../models/','spark.ptf')
    #set position in queue
        pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
        + self.pipeInterval, 4.25)    
    elif i == -4:
    #create Steam pipe
        pipe = PipeFire()
        #self.loadParticleConfig(pipe, '../models/','fireish.ptf')
    #set position in queue
        pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
        + self.pipeInterval, 4.25)
        

    self.pipeList.append(pipe)
    #self.pipeGenericKeep.append(pipe)
    
def loadParticleConfig(self, pipe, path, file):
    #Start of the code from steam.ptf
    pipe.particle.cleanup()
    pipe.particle = ParticleEffect()
    pipe.particle.loadConfig(Filename(path,file))
    #Sets particles to birth relative to the teapot, but to render at toplevel
    pipe.particle.start(pipe.model)
    pipe.particle.setScale(20)
    pipe.particle.setPos(0.00, -200.000, -200.00)


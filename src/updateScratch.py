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
from panda3d.core import AmbientLight,DirectionalLight
from panda3d.core import Point3,Vec3,Vec4
from panda3d.core import Filename
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
from direct.gui.OnscreenText import OnscreenText

from GrabBag import *
from Pipe import *


import math, sys, random, time
from GrabBag import *

def keyEvents(self, task):
    """defines all keypress events"""
    dt = task.time - self.prevTime


    if self.keyMap["drop"] == 0:
        for i in range(self.pipeList.__len__()):
            self.pipeList[i].model.setY(self.pipeList[i].model.getY() - dt*100*1.6)
    if self.keyMap["drop"] == 1:
        for i in range(self.pipeList.__len__()):
            self.pipeList[i].model.setR(self.pipeList[i].model.getR() + dt*20*i)

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
        if self.spider.getZ() < 6.1:
            self.spider.setZ(self.spider.getZ()+1*dist)
    if self.keyMap["moveDown"] == 1:
        self.spider.setHpr(180, 65, 180)
        if self.spider.getZ() > 2.6:
            self.spider.setZ(self.spider.getZ()-1*dist)
    #print self.spider.getPos()

    self.adjustCamera()

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

        self.pipeList[0].destroy()
        self.pipeList.pop(0)

        #create new pipe segment
        self.createPipe(-1)



    return Task.cont

def createPipe(self, i):
        pipe = PipeGeneric()
        
        #set position in queue
        if i >= 0:
            pipe.model.setPos(0, i*self.pipeInterval, 4.25)
        else:
            pipe.model.setPos(0, self.pipeList[self.pipeList.__len__()-1].model.getY() \
            + self.pipeInterval, 4.25)
            
        self.pipeList.append(pipe)    
        
        # #pick file
        # filename = ["../models/tunnelWallTemp"]
        # filename.append(str(self.pipeBag.pick()-1))
        # filename.append(".egg")
        # filename = ''.join(filename)
        # filename = "../models/COMPARE1tunnelwall ALL.egg"

        # #load file
        # pipe = loader.loadModel(filename)
        # pipe.setScale(.0175)
        # self.addPointLight(pipe)

        # #set position in queue
        # if i >= 0:
            # pipe.setPos(0, i*self.pipeInterval, 4.25)
        # else:
            # pipe.setPos(0, self.pipeList[self.pipeList.__len__()-1].getY() \
            # + self.pipeInterval, 4.25)

        # #rotate by 0, 90, 180, or 270 degrees
        # pipe.setR(random.randint(0,3)*90)
        # print pipe.getR()

        # pipe.reparentTo(render)
        # self.pipeList.append(pipe)

        # #Adding a collision sphere to the pipe
        # cSphere = CollisionSphere((200,0,0), 100)
        # cNode = CollisionNode("pipe")
        # cNode.addSolid(cSphere)
        # cNodePath = pipe.attachNewNode(cNode)
        # #cNodePath.show()

        #Particle Effect: VERY SLOW
##        p = ParticleEffect()
##        p.loadConfig("../models/steam.ptf")
##        p.start(pipe)
##        p.setPos(100.00, 0.000, 0)
##        p.setScale(100.00, 80.000, 80)
##
##        self.particleList.append(p)

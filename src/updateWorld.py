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
import math, sys, random, time
from GrabBag import *
    
def keyEvents(self, task):
    """defines all keypress events"""
    dt = task.time - self.prevTime        
    
    
    if self.keyMap["drop"] == 0:
        for i in range(self.pipeList.__len__()):
            self.pipeList[i].setY(self.pipeList[i].getY() - dt*100)
    else:
        for i in range(self.pipeList.__len__()):
            self.pipeList[i].setR(self.pipeList[i].getR() + dt*10*i)
    
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
    self.pipeDepth = self.pipeList[0].getY()
    #print self.pipeDepth
    if self.pipeDepth < -1*self.pipeInterval:
        self.pipeList[0].removeNode()
        self.pipeList.pop(0)
        
        self.createPipe(-1)
        
    return Task.cont
    
def createPipe(self, i):                
        #pick file
        filename = ["../models/tunnelWallTemp"]
        filename.append(str(self.pipeBag.pick()-1))
        filename.append(".egg")
        filename = ''.join(filename)
        filename = "../models/NO TRY MEEE- tunnelwall template5.egg"
        
        #load file
        pipe = loader.loadModel(filename)
        pipe.setScale(.0175)
        
        #set position in queue
        if i >= 0:
            pipe.setPos(0, i*self.pipeInterval, 4.25)
        else:
            pipe.setPos(0, self.pipeList[self.pipeList.__len__()-1].getY() \
            + self.pipeInterval, 4.25)
            
        #rotate by 0, 90, 180, or 270 degrees
        pipe.setR(random.randint(0,3)*90)
        print pipe.getR()
        
        # if filename == "tunnelWallTemp5.egg":
            # self.addPointLight(pipe)
        pipe.reparentTo(render)
        self.pipeList.append(pipe)
        
        
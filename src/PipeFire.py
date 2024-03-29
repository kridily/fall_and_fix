from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.interval.IntervalGlobal import * #for compound intervals

from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from panda3d.core import TextNode
from panda3d.core import AmbientLight,DirectionalLight, PointLight
from panda3d.core import Point3,Vec3,Vec4
from panda3d.core import Filename
from panda3d.core import Shader
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
import math, sys, random, time

from ActionCommand import *
from GrabBag import *

class PipeFire:
    """
    Creates self contained pipe objects with methods that create,
    reference, and destroy models, collision tubes, lights,
    particles, and ActionCommand sequences.
    """



    def __init__(self):

        #SoundIntervals
        #base = ShowBase()
        self.sound = loader.loadSfx("../audio/fire.wav")
        self.sound.setLoop(True)
        self.sound.play()

        #pick file
        self.fileName = "../models/tunnelfire"
        
        #load model
        self.model = loader.loadModel(self.fileName)
        self.model.setScale(.0175)
        #print self.model.ls()

        self.nodePath = NodePath(self.model)
        self.model.reparentTo(render)
        self.key = self.model.getKey()


        ##self.addModel(bag)
        self.addPointLight(self.model)
        self.shaderEnabled = 0
        #self.addShader()        
        #self.addCollision()
        ##self.addParticle(self.model)

        base.enableParticles()

        self.particle = ParticleEffect()
        self.loadParticleConfig('../models/', 'fireish.ptf')
        #self.loadParticleConfig("fireish.ptf")
        
        i = random.randint(0,2)
        if not i: self.addActionCommand("ud")
        else: self.addActionCommand("lr")
        self.type = "fire"

        
        
        #rotate by 0, 90, 180, or 270 degrees
        self.model.setR(random.randint(0,3)*90)
        #print self.model.getR()

    def addPointLight(self, pipe):
        """create a point light for pipe"""

        #The redpoint light and helper
        #RED
        # r = random.uniform(700, 900) / 1000
        # g = random.uniform(0, 300) / 1000
        # b = g

        #ORANGE
        r = 1
        b = random.randint(0,91)
        g = (b / 2) + 102
        b = b / 255.0
        g = g / 255.0
        self.helper = loader.loadModel("../models/sphere.egg.pz")

        self.helper.setColor( Vec4( r, g, b, 1 ) )
        self.helper.setPos(pipe.getPos())
        #print self.helper.getColor()

        #This is value is irrelevent at the moment unless I move the lights
        self.helper.setScale(.25*1) #must be greater than 0.001


        #optionally set location of light within pipe
        self.helper.setY(self.helper.getY()-50*35 ) #moves to inbetween segments
        self.helper.setZ(self.helper.getZ()-50*6 ) #makes 3 sided lights

        self.light = self.helper.attachNewNode( PointLight( "self.light" ) )
        self.light.node().setAttenuation( Vec3( .1, 0.04, 0.1 )/2.5 )
        self.light.node().setColor( Vec4( r, g, b, 1 ) )
        self.light.node().setSpecularColor( Vec4( 1 ) )
     
        render.setLight( self.light )

        self.helper.reparentTo( pipe )
        
        ###
        self.h = loader.loadModel("../models/sphere.egg.pz")
        self.h.setColor( Vec4( 1, 1, 1, 1 ) )
        self.h.setPos(140, 0, -100)
        self.h.setScale(.25*1)
        
        self.plight = self.h.attachNewNode( PointLight( "self.plight" ) )
        self.plight.node().setColor(VBase4(4, 2, 0, 1))
        self.plight.node().setAttenuation(Point3(1, 1, 1))
        
        render.setLight(self.plight)
        self.h.reparentTo( pipe )
        
        
        
        
    ###def addModel(self, bag):
        """Adds the model to the pipe object"""
        ####moved to init for some reason



    def addShader(self):
        self.model.setShaderAuto()
        self.shaderEnabled = 1


    def addCollision(self):
        #Finding and adding collision tube to the pipe
        #cSphere = CollisionSphere((200,0,0), 100)
        cNode = self.nodePath.find("**/tube_collision").node()
        #cNode = CollisionNode("pipeCollision")
        #cNode.addSolid(solid)
        self.collision = self.model.attachNewNode(cNode)
        self.collision.show()


    def loadParticleConfig(self, path, file):
        #Start of the code from steam.ptf
        self.particle.cleanup()
        self.particle = ParticleEffect()
        self.particle.loadConfig(Filename(path, file))
        #Sets particles to birth relative to the teapot, but to render at toplevel
        self.particle.start(self.model)
        self.particle.setScale(40)
        self.particle.setPos(140.00, 0.00, -200.00)
        
        
        
        

        
        
    def addActionCommand(self, command):
        self.actionCommand = ActionCommand(command.__len__(), command, command)


    def destroy(self):
        #Remove particles from particle list
        #Idea: Instead of deleting particle effects, try moving them
        #to new pipe segment?
        # self.particle.cleanup()
        # self.particle.removeNode()

        #stop sound
        self.sound.setLoop(False)
        self.sound.stop()

        #remove pointLight from segment
        render.clearLight(self.light)
        render.clearLight(self.plight)
        self.helper.removeNode()

        #remove pipe segment
        self.model.removeNode()


    def reactivate(self, pipe):
        print pipe.nodePath.ls()
        print "\n\n\n\n"
        self.model = pipe.model
        self.helper = pipe.helper
        self.light = pipe.light.node()
        self.shaderEnabled = 0
        self.collision = pipe.collision.node()
        #self.particle = pipe.particle
        
        #rotate by 0, 90, 180, or 270 degrees
        self.model.setR(random.randint(0,3)*90)

    def recycle(self):
        #rotate by 0, 90, 180, or 270 degrees
        self.model.setR(random.randint(0,3)*90)

        #ORANGE
        r = 1
        b = random.randint(0,91)
        g = (b / 2) + 102
        b = b / 255.0
        g = g / 255.0
        self.helper.setColor( Vec4( r, g, b, 1 ) )
        self.light.node().setColor( Vec4( r, g, b, 1 ) )
        self.actionCommand.resetCommand()

    def isCommandEmpty(self):
        print "LETS FIND OUT"
        return self.actionCommand.isEmpty()


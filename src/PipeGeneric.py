from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.interval.IntervalGlobal import * #for compound intervals

from panda3d.physics import BaseParticleEmitter,BaseParticleRenderer
from panda3d.physics import PointParticleFactory,SpriteParticleRenderer
from panda3d.physics import LinearNoiseForce,DiscEmitter
from panda3d.core import TextNode
from panda3d.core import AmbientLight,DirectionalLight, PointLight
from panda3d.core import Point3,Vec3,Vec4
from panda3d.core import Filename, Shader
from direct.particles.Particles import Particles
from direct.particles.ParticleEffect import ParticleEffect
from direct.particles.ForceGroup import ForceGroup
import math, sys, random, time

from ActionCommand import *
from GrabBag import *

class PipeGeneric:
    """
    Creates self contained pipe objects with methods that create,
    reference, and destroy models, collision tubes, lights,
    particles, and ActionCommand sequences.
    """
    def __init__(self, bag, template=False):

        if template is not False: self.reactivate(template)
        else:
            self.addModel(bag)
            self.addPointLight(self.model)
            self.shaderEnabled = 0
            #self.addCollision()
            #self.addParticle()
            self.addActionCommand("")

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
        self.helper.reparentTo( pipe )
        render.setLight( self.light )


    def addModel(self, bag):
        """Adds the model to the pipe object"""

        #pick file
        filename = ["../models/tunnel"]
        filename.append(str(bag.pick()))
        filename.append(".egg")
        self.fileName = ''.join(filename)

        #self.fileName = "../models/tunnelclear.egg"

        #load model
        self.model = loader.loadModel(self.fileName)
        self.model.setScale(.0175)
        #print self.model.ls()

        #rotate by 0, 90, 180, or 270 degrees
        self.model.setR(random.randint(0,3)*90)
        #print self.model.getR()

        self.nodePath = NodePath(self.model)
        self.model.reparentTo(render)
        self.key = self.model.getKey()

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


    def addParticle(self, pipe):
        #Particle Effect: VERY SLOW
        self.particle = ParticleEffect()
        self.particle.loadConfig("../models/steam.ptf")
        self.particle.start(pipe)
        self.particle.setPos(100.00, 0.000, 0)
        self.particle.setScale(100.00, 80.00, 80.00)

    def addActionCommand(self, command):
        self.actionCommand = ActionCommand(command.__len__(), command, command)


    def destroy(self):
        #Remove particles from particle list
        #Idea: Instead of deleting particle effects, try moving them
        #to new pipe segment?
        # self.particle.cleanup()
        # self.particle.removeNode()

        #remove pointLight from segment
        render.clearLight(self.light)
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

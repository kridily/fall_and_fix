from pandac.PandaModules import * #basic Panda modules
from direct.showbase.DirectObject import DirectObject #for event handling
from direct.interval.IntervalGlobal import * #for compound intervals

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
import math, sys, random, time

from ActionCommand import *
from GrabBag import *

class PipeGeneric:
    """
    Creates self contained pipe objects with methods that create,
    reference, and destroy models, collision tubes, lights,
    particles, and ActionCommand sequences.
    """
    def __init__(self):
        
        #self.nodePath = NodePath(self)
        self.addModel()
        self.addPointLight(self.model)
        self.addCollision()
        #self.addParticle()
        self.addActionCommand("")

        #return (self)
        
    def addPointLight(self, pipe):    
        """create a point light for pipe"""      
        
        #The redpoint light and helper
        gb = random.uniform(0, 300) / 1000
        r = random.uniform(700, 900) / 1000        
        self.helper = loader.loadModel("../models/sphere.egg.pz")
        
        self.helper.setColor( Vec4( r, gb, gb, 1 ) )      
        self.helper.setPos(pipe.getPos())
        #print self.helper.getColor()
        self.helper.setScale(.25*0)
        #optionally set location of light within pipe
        self.helper.setY(self.helper.getY()-50*35 ) #moves to inbetween segments
        self.helper.setZ(self.helper.getZ()-50*6 ) #makes 3 sided lights
        
        self.light = self.helper.attachNewNode( PointLight( "self.light" ) )
        self.light.node().setAttenuation( Vec3( .1, 0.04, 0.0 )/2 )                   
        self.light.node().setColor( Vec4( r, gb, gb, 1 ) )
        self.light.node().setSpecularColor( Vec4( 1 ) )
        self.helper.reparentTo( pipe )
        render.setLight( self.light )

        
    def addModel(self):
        """Adds the model to the pipe object"""
    
        #pick file
        self.fileName = "../models/broken pipe tunnel (with collision tube).egg"

        #load model
        self.model = loader.loadModel(self.fileName)
        self.model.setScale(.0175)
        #print self.model.ls()
        
        #rotate by 0, 90, 180, or 270 degrees
        self.model.setR(random.randint(0,3)*90)
        #print self.model.getR()

        self.nodePath = NodePath(self.model)
        self.model.reparentTo(render)
    
    def addCollision(self):
        #Finding and adding collision tube to the pipe
        #cSphere = CollisionSphere((200,0,0), 100)
        cNode = self.nodePath.find("**/pipe_collision").node()
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
        self.particle.setScale(100.00, 80.000, 80)
          
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
    


    
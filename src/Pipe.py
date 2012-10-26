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

class PipeGeneric:
    """
    Creates self contained pipe objects with methods that create,
    reference, and destroy models, collision tubes, lights,
    particles, and ActionCommand sequences.
    """
    def __init__(self, world):
        
        self.addModel()
        self.addPointLight(self.model)
        

        #Adding a collision sphere to the pipe
        #cSphere = CollisionSphere((200,0,0), 100)
        self.collision = nodepath.find("**/pipe_collision")        
        cNode = CollisionNode("pipeCollision")
        cNode.addSolid(self.collision)
        cNodePath = self.model.attachNewNode(cNode)        
        cNodePath.show()

        #Particle Effect: VERY SLOW
        # p = ParticleEffect()
        # p.loadConfig("../models/steam.ptf")
        # p.start(pipe)
        # p.setPos(100.00, 0.000, 0)
        # p.setScale(100.00, 80.000, 80)

        # self.particleList.append(p)
        
        world.pipeList.append(self)
        
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
        helper.setZ(helper.getZ()-50*6 ) #makes 3 sided lights
        
        light = helper.attachNewNode( PointLight( "light" ) )
        light.node().setAttenuation( Vec3( .1, 0.04, 0.0 )/2 )                   
        light.node().setColor( Vec4( r, gb, gb, 1 ) )
        light.node().setSpecularColor( Vec4( 1 ) )
        helper.reparentTo( pipe )
        render.setLight( light )
        
        self.redHelperList.append(helper)
        self.redLightList.append(light)
        
    def addModel(self):
        #pick file
        self.filename = "../models/COMPARE1tunnelwall ALL.egg"

        #load model
        self.model = loader.loadModel(self.filename)
        self.model.setScale(.0175)
        
        #set position in queue
        if i >= 0:
            self.model.setPos(0, i*world.pipeInterval, 4.25)
        else:
            self.model.setPos(0, world.pipeList[world.pipeList.__len__()-1].getY() \
            + world.pipeInterval, 4.25)

        #rotate by 0, 90, 180, or 270 degrees
        self.model.setR(random.randint(0,3)*90)
        print self.model.getR()

        self.model.reparentTo(render)
    
    def collision(self):
    
    # def helper(self):
    
    # def light(self):
    
    def particle(self):
    
    def actionCommand(self):
    
    def destroy(self):
    
    


    


from Entity import Entity
import Category

from StateFactory import StateFactory

from DrawingSystem import DrawingSystem
from CollisionSystem import CollisionSystem
from MovingSystem import MovingSystem
from SpriteSystem import SpriteSystem
from InputSystem import InputSystem

import StateKey

BACKGROUND  = 0
ACTIVELAYER = 1
FORGROUND   = 2
LAYERCOUNT  = 3





class World():
    """ Contains all objects relevant to the game world """

    def __init__(self, dt):
        viewSize = (300,300)
        self.spawnLocation = [100,100]
        self.entities = []
        self.newEntities = []
        self.sf = StateFactory()
        self.buildScene()
        #self.commandQueue = []
        
        self.drawingSystem   = DrawingSystem()
        self.collisionSystem = CollisionSystem(viewSize, dt)
        self.movingSystem    = MovingSystem(dt)
        self.spriteSystem    = SpriteSystem()
        self.inputSystem     = InputSystem()


    def update(self, commandQueue, dt):
        """Applies the command Queue to the entities, finds how the orld should respond (collisions ect.) and then updates the entities """

        #Add a command asking for the player entity to look for input
        #note that we use an optional paramiter to pass the lambda access to the command queue

        #Process all commands (dt = timePerFrame)
        #while self.commandQueue != []:
        #    command = self.commandQueue.pop(0)
        #    for entity in entities:
        #        entity.performCommand(command, dt)


        self.inputSystem.handleInput(self.entities)
        self.collisionSystem.resolveCollisions(self.entities)
        self.movingSystem.move(self.entities)

    def render(self, surface):
        self.drawingSystem.draw(self.entities, surface)   
                          
    def buildScene(self):
        
        eTemp = Entity(Category.PLAYER, self.sf.getState(StateKey.PlayerStanding))
        eTemp.state.geometryComponent.location = [50,100]
        self.entities.append(eTemp)

        #####

        eTemp = Entity(Category.ENEMY, self.sf.getState(StateKey.EnemyStanding))
        eTemp.state.geometryComponent.location = [120,150]
        self.entities.append(eTemp)
        
        eTemp = Entity(Category.ENEMY, self.sf.getState(StateKey.EnemyStanding))
        eTemp.state.geometryComponent.location = [100,100]
        self.entities.append(eTemp)
        
        eTemp = Entity(Category.ENEMY, self.sf.getState(StateKey.EnemyStanding))
        eTemp.state.geometryComponent.location = [200,130]
        self.entities.append(eTemp)
        
        eTemp = Entity(Category.ENEMY, self.sf.getState(StateKey.EnemyStanding))
        eTemp.state.geometryComponent.location = [160,30]
        self.entities.append(eTemp)
        
    def createEntities(self)
        pastNoEntities = len(self.entities)
        self.entities.extend(self.newEntities)
        self.drawingSystem.registerEntities(pastNoEntities, self.entities)
        self.collisionSystem.registerEntities(pastNoEntities, self.entities)
        self.movingSystem.registerEntities(pastNoEntities, self.entities)
        self.spriteSystem.registerEntities(pastNoEntities, self.entities)
        self.inputSystem.registerEntities(pastNoEntities, self.entities)



























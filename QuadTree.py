
import pygame
from pygame.locals import Color
from itertools import combinations
import FindingLambda as fl

_maxDepth = 5
_capacity = 4

class QuadTree():

    def __init__(self, boundary, depth = 0):
        self.boundary   = boundary
        self.contents   = []
        self.subtree    = []
        self.depth      = depth
    
    def addEntities(self, lambdaFinder):
        """ Pass a list or tupple of entities which will then be added to the quadtree."""

        #does the entitiy lie in the quadtree's bondary
        esInBounds = lambdaFinder.inBoundary(self.boundary)

        #are we adding to this level or do we need to pass down the tree
        if len(self.contents) < _capacity or self.depth > _maxDepth:
            self.contents.extend(esInBounds)
            return
        
        #Make the subtree if the current node is full
        if len(self.subtree) == 0:
            self.makeSubTrees(lambdaFinder, esInBounds)

    def makeSubTrees(self, lambdaFinder, esInBounds):
        """ The domain is spit into 4 quads and all contents are passed to the relevant quad """

        self.subtree.append(QuadTree(self._NWBoundary(), self.depth + 1))
        self.subtree.append(QuadTree(self._NEBoundary(), self.depth + 1))
        self.subtree.append(QuadTree(self._SWBoundary(), self.depth + 1))
        self.subtree.append(QuadTree(self._SEBoundary(), self.depth + 1))

        #Try to add contents to any tree that wants it
        for quad in self.subtree:
            quad.addEntities(lambdaFinder, self.contents)
            quad.addEntities(lambdaFinder, esInBounds)


    def empty(self):
        self.contents   = []
        self.subtree    = []


    def findCollisions(self, lambdaFinder, collisions = []):
        if self.subtree == []:
            collisions.append(lambdaFinder.findCollisions(self.contents))
        else:
            for tree in self.subtree:
                tree.findCollisions(lambdaFinder, collisions)
        return collisions


    def drawTree(self, surface):
        """ Draws the boundaries of the quadtree """
        pygame.draw.rect(surface, Color("green"), self.boundary, 1)
        for quad in self.subtree:
            quad.drawTree(surface)



    """A collection of functions for finding the quarters of the current boudary"""
    def _NWBoundary(self):
        return pygame.Rect(self.boundary.left, self.boundary.top, self.boundary.width / 2, self.boundary.height / 2)

    def _NEBoundary(self):
        return pygame.Rect(self.boundary.left + self.boundary.width / 2, self.boundary.top, self.boundary.width / 2, self.boundary.height / 2)

    def _SWBoundary(self):
        return pygame.Rect(self.boundary.left, self.boundary.top + self.boundary.height / 2, self.boundary.width / 2, self.boundary.height / 2)

    def _SEBoundary(self):
        return pygame.Rect(self.boundary.left + self.boundary.width / 2, self.boundary.top + self.boundary.height / 2, self.boundary.width / 2, self.boundary.height / 2)
    """end of helper functions"""

    #-------------------------------------------


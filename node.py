import math
from constants import *
import pygame

class Node:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def pos(self):
        return self.row, self.col
    
    def is_considered(self):
        return self.color == RED
    
    def is_found(self):
        return self.color == GREEN
    
    def is_wall(self):
        return self.color == BLACK
    
    def is_start_pos(self):
        return self.color == ORANGE
    
    def is_end_pos(self):
        return self.color == BLUE
    
    def reset(self):
        self.color = WHITE

    def consider(self):
        self.color = RED

    def find(self):
        self.color = GREEN

    def block(self):
        self.color = BLACK
    
    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE
    
    def make_start(self):
        self.color = ORANGE
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def make_neighbors(self,grid):
        self.neighbors = []
        NW = (self.row-1,self.col-1)
        N = (self.row-1,self.col)
        NE = (self.row-1,self.col+1)
        W = (self.row,self.col-1)
        E = (self.row,self.col+1)
        SW = (self.row+1,self.col-1)
        S = (self.row+1,self.col)
        SE = (self.row+1,self.col+1)

        dirs = [NW,
                N,
                NE,
                W,
                E,
                SW,
                S,
                SE]
        dirs = list(filter(lambda coords: (0<=coords[0]<=self.total_rows-1 and 0<=coords[1]<=self.total_rows-1),dirs))

        for dir in dirs:
            if (not grid[dir[0]][dir[1]].is_wall()):
                self.neighbors.append(grid[dir[0]][dir[1]])

        if (N in dirs and E in dirs and grid[N[0]][N[1]].is_wall() and grid[E[0]][E[1]].is_wall() and NE in dirs and grid[NE[0]][NE[1]] in self.neighbors):
            self.neighbors.remove(grid[NE[0]][NE[1]])
        if (N in dirs and W in dirs and grid[N[0]][N[1]].is_wall() and grid[W[0]][W[1]].is_wall() and NW in dirs and grid[NW[0]][NW[1]] in self.neighbors):
            self.neighbors.remove(grid[NW[0]][NW[1]])
        if (S in dirs and E in dirs and grid[S[0]][S[1]].is_wall() and grid[E[0]][E[1]].is_wall() and SE in dirs and grid[SE[0]][SE[1]] in self.neighbors):
            self.neighbors.remove(grid[SE[0]][SE[1]])
        if (S in dirs and W in dirs and grid[S[0]][S[1]].is_wall() and grid[W[0]][W[1]].is_wall() and SW in dirs and grid[SW[0]][SW[1]] in self.neighbors):
            self.neighbors.remove(grid[SW[0]][SW[1]])

            
        

        
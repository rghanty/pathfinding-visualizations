import pygame
from queue import PriorityQueue
import math
from node import Node
from constants import *


window = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption("Pathfinding Visualizations")

def heuristic(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    #abs(x2-x1) + abs(y2-y1)
    #math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)


def make_grid(rows,width):
    grid = []
    side = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            grid[i].append(Node(i,j,side,rows))
    return grid

def draw_grid(win,rows,width):
    side = width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*side),(width,i*side))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*side,0),(j*side,width))

def draw(win,grid,rows,width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()

def mouse_pos(pos, rows, width):
    side = width//rows
    y,x = pos
    row = y//side
    col = x//side

    return row,col

def path(parent,current,draw):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()

def is_all_nodes_inf(nodes, scores):
    for node in nodes:
        if scores[node] != float("inf"):
            return False
    return True


def a_star(draw,grid,start,end):
    rank = 0
    open_set = PriorityQueue()
    open_set.put((0,rank,start))
    parent = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.pos(), end.pos())

    open_set_dict = {start}         #contains same elements as open_set, because cannot check if something exists in open_set
    while not open_set.empty() and not is_all_nodes_inf(open_set_dict,f_score):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = open_set.get()[2]
        open_set_dict.remove(current)

        if current == end:
            path(parent, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors: 
            temp_g_score = g_score[current]+1
            if temp_g_score < g_score[neighbor]:
                parent[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor.pos(),end.pos())

                if neighbor not in open_set_dict:
                    rank += 1
                    open_set.put((f_score[neighbor],rank,neighbor))
                    open_set_dict.add(neighbor)
                    neighbor.find()
        
        draw()
        if current != start:
            current.consider()
    return False

def dijkstra(draw,grid,start,end):
    rank = 0
    unvisited = PriorityQueue()
    unvisited.put((0,rank,start))
    parent = {}
    distances = {node: float("inf") for row in grid for node in row}
    distances[start] = 0
    

    unvisited_dict = {start}         #contains same elements as open_set, because cannot check if something exists in open_set
    while not unvisited.empty() and not is_all_nodes_inf(unvisited_dict,distances):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = unvisited.get()[2]
        unvisited_dict.remove(current)

        if current == end:
            path(parent, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for neighbor in current.neighbors: 
            temp_g_score = distances[current]+1
            if temp_g_score < distances[neighbor]:
                parent[neighbor] = current
                distances[neighbor] = temp_g_score
               

                if neighbor not in unvisited_dict:
                    rank += 1
                    unvisited.put((distances[neighbor],rank,neighbor))
                    unvisited_dict.add(neighbor)
                    neighbor.find()
        
        draw()
        if current != start:
            current.consider()
    return False

def dfs(draw, grid, start, end):
    stack = [start]
    parent = {}
    visited = set()

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = stack.pop()
        visited.add(current)

        if current == end:
            path(parent, end, draw)
            end.make_end()
            start.make_start()
            return True

        for neighbor in current.neighbors:
            if neighbor not in visited and neighbor not in stack:
                parent[neighbor] = current
                stack.append(neighbor)
                neighbor.find()

        draw()
        if current != start:
            current.consider()

    return False
        





def clear(grid):
    for row in grid:
        for node in row:
            node.reset()

def main(win,width):
    ROWS = 80
    grid = make_grid(ROWS,width)
    start = None
    end = None
    clock = pygame.time.Clock()
    run = True
    
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
            if pygame.mouse.get_pressed()[0]: #left mouse
                pos = pygame.mouse.get_pos()
                row,col = mouse_pos(pos,ROWS,width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_end()
                elif node != start and node != end:
                    node.block()

            elif pygame.mouse.get_pressed()[2]: #right mouse
                pos = pygame.mouse.get_pos()
                row,col = mouse_pos(pos,ROWS,width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                if node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.make_neighbors(grid)
                            
                    
                    result = a_star(lambda: draw(win,grid,ROWS,width),grid,start,end)
                    if result:
                        print("Found!")
                    else:
                        print("Not found")

                if event.key == pygame.K_c:
                    clear(grid)
                    start = None
                    end = None
        clock.tick(120)

                

                    
                
    

    pygame.quit()


main(window,SIZE)






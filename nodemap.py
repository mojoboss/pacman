__author__ = 'starlord'

import pygame
from pygame.locals import *
import numpy
from nodegroup import NodeGroup
from pacman import Pacman
from tilegroup import Tilegroup
from ghostgroup import Ghostgroup
from coingroup import Coingroup
from maze_env import Environment
from time import sleep

def getRowCol(filename):
        layout = numpy.loadtxt(filename, dtype=str)
        c, r = layout.shape
        return r, c

pygame.init()
width, height = (16, 16)
maze_filename = 'mazes/t1.txt'
coin_and_ghosts_filename = 'mazes/t2.txt'
r, c = getRowCol(maze_filename)
screen = pygame.display.set_mode((r*width, c*height), 0, 32)
background = pygame.surface.Surface((r*width, c*height)).convert()
background.fill((0,0,0))

#GLOBAL VARIABLES
tilegrp = None
tiles = None
nodegrp = None
nodes = None
coingrp = None
coins = None
ghostgrp = None
score = None
ghosts = None
pacman = None
count = None
#-----------------
def game_start():
    global tilegrp
    global tiles
    global nodegrp
    global nodes
    global coingrp
    global coins
    global ghostgrp
    global ghosts
    global pacman
    global count
    global score

    score = 0
    #code to add tiles in the screen
    tilegrp = Tilegroup(width, height)
    tiles = tilegrp.createTileList(maze_filename)

    #nodes added, not displayed on the screen, only for navigation purpose
    nodegrp = NodeGroup(width, height)
    nodes = nodegrp.createNodeList(maze_filename)

    #adding coins to our maze
    coingrp = Coingroup(width)
    coins = coingrp.createCoinList(coin_and_ghosts_filename)

    #ghosts added
    ghostgrp = Ghostgroup(width, height)
    ghosts = ghostgrp.create_ghostlist(maze_filename, coin_and_ghosts_filename, nodes)

    #pacman added
    from random import randint
    ind = randint(0, len(nodes)-1)
    pacman = Pacman(nodes[ind], (width,height), [nodes[ind].position.x, nodes[ind].position.y])
    count=0
#-------------------------------------------------------------------------------------------
episodes = 0
training = True
game_start()
env = Environment(pacman, ghosts, nodes, coins)
learning_rate = 0.3
discount = 0.8
while True:
    if episodes > 150:
        pacman.speed = 0.2
        ghosts[0].speed = 0.1
        learning_rate = 0
        discount = 0
        training = False
    #++++
    count+=1
    from random import randint
    if count == 20:
        i  = randint(0, len(ghosts)-1)
        ghosts[i].scatter_ghost()
        count = 0
    #++++
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0,0))

    pacman.draw(screen)

    ####moment before pacman update position
    env.set_params(pacman, ghosts, nodes, coins)
    k1 = env.make_key()
    if k1 not in env.qdictionary:
        env.add_key(k1)
    ##########################################
    for t in tiles:
        t.draw(screen)
    for c in coins:
        c.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)
        ghost.ghost_movement(pacman.currentnode, nodes, 'bfs')

    #print k1, env.qdictionary[k1]
    action = pacman.update(nodes, env.qdictionary, k1, training)

    reward = -0.005
    for c in coins:
        if (pacman.coin_collide(c)):
            score += 10
            coins.remove(c)
            reward += 3.5
            if (len(coins)==0):
                print str(episodes)+'  winnnnnnnn  '+ str(score)
                episodes += 1
                game_start()

    for g in ghosts:
        if (pacman.ghost_collide(g)):
            pygame.mixer.music.load('sounds/sound.wav')
            #pygame.mixer.music.play(0)
            reward -= 4.5
            episodes += 1
            print str(episodes)+'  lost  '+ str(score)
            game_start()
    if action:
        ####moment after pacman update position
        env.set_params(pacman, ghosts, nodes, coins)
        k2 = env.make_key()
        if k2 not in env.qdictionary:
            env.add_key(k2)
        best_action_in_k2 = pacman.best_action(env.qdictionary, k2)
        maxx = env.qdictionary[k2][best_action_in_k2]
        expected = reward + (discount * maxx)
        action_tuple = (int(action.x), int(action.y))
        change = learning_rate * (expected - env.qdictionary[k1][action_tuple])
        env.qdictionary[k1][action_tuple] += change
        #############################################

    pygame.display.update()


'''
#code to draw the node graph
    for node in nodes:
        pygame.draw.circle(screen,(255,0,0),node.position.toTuple(), 10)
    for node in nodes:
        for nextnode in node.neighbors:
            pygame.draw.line(screen,(255,255,255),node.position.toTuple(), nextnode.position.toTuple(), 2)
'''
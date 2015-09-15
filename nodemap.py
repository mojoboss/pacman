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

#method to get rows and cols from layout text file as a matrix
def getRowCol(filename):
        layout = numpy.loadtxt(filename, dtype=str)
        c, r = layout.shape
        return r, c
#SOUNDS
def play_tick():
    pygame.mixer.music.load('sounds/tick.mp3')
    pygame.mixer.music.play(0)
def play_ghost():
    pygame.mixer.music.load('sounds/sound.wav')
    pygame.mixer.music.play(0)

pygame.init()
width, height = (32, 32)
maze_filename = 'mazes/trickyClassic.txt'
coin_and_ghosts_filename = 'mazes/trickyClassicCoins.txt'
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
pacman1 = None
pacman2 = None
pacman3 = None
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
    global pacman1
    global pacman2
    global pacman3
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
    ind1 = randint(0, len(nodes)-1)
    ind2 = randint(0, len(nodes)-1)
    ind3 = randint(0, len(nodes)-1)
    pacman =  Pacman(nodes[ind], (width,height), [nodes[ind].position.x, nodes[ind].position.y])
    pacman1 = Pacman(nodes[ind1], (width,height), [nodes[ind].position.x, nodes[ind].position.y])
    pacman2 = Pacman(nodes[ind2], (width,height), [nodes[ind].position.x, nodes[ind].position.y])
    pacman3 = Pacman(nodes[ind3], (width,height), [nodes[ind].position.x, nodes[ind].position.y])
#-------------------------------------------------------------------------------------------
# following are the training parameters, boolean 'training' causes pacman speed to be very fast during
# training phase and then visible speed after training when learning rate and DISCOUNT factor are set
# to 0. Episodes are the number of episodes for which training occurs.
episodes = 0
training = True
game_start()
env = Environment(pacman, ghosts, nodes, coins)
LEARNING_RATE = 0.5
DISCOUNT = 0.9
TRAIN_EPISODES = 200
avg_scores_list = []
while True:
    #check whether training is finished or not
    if episodes >= TRAIN_EPISODES:
        pacman.speed = 0.8
        for g in ghosts:
            g.speed = 0.4
        LEARNING_RATE = 0
        DISCOUNT = 0
        training = False

    #this animates pacman
    pacman.animate_pacman()
    if training:
        pacman1.animate_pacman()
        pacman2.animate_pacman()
        pacman3.animate_pacman()
    #this part creates randomness in ghost's movement
    for g in ghosts:
        g.random_ghost_movement()

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
    screen.blit(background, (0, 0))
    pacman.draw(screen)
    if training:
        pacman1.draw(screen)
        pacman2.draw(screen)
        pacman3.draw(screen)
    for t in tiles:
        t.draw(screen)
    for c in coins:
        c.draw(screen)
    for ghost in ghosts:
        ghost.draw(screen)
        ghost.ghost_movement(pacman.currentnode, nodes, 'bfs')

    ####moment before pacman update position
    env.set_params(pacman, ghosts, nodes, coins)
    k1 = env.make_key()
    if k1 not in env.qdictionary:
        env.add_key(k1)
    ##########################################
    #print k1, env.qdictionary[k1]

    #training is boolean passed into update method. It keeps fast speed for pacman for for faster training.
    action = pacman.update(nodes, env.qdictionary, k1, training)
    reward = -0.05
    for c in coins:
        if (pacman.coin_collide(c)):
            #play_tick()
            score += 10
            coins.remove(c)
            reward += 3.5
            if (len(coins)==0):
                print str(episodes)+'   **won**  '+ str(score)
                episodes += 1
                if training:
                    LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                avg_scores_list.append(score)
                game_start()

    for g in ghosts:
        if (pacman.ghost_collide(g)):
            #play_ghost()
            reward -= 4.5
            episodes += 1
            if training:
                LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
            print str(episodes)+'    lost    '+ str(score)
            avg_scores_list.append(score)
            game_start()
    if action:
        ####moment after pacman update position
        env.set_params(pacman, ghosts, nodes, coins)
        k2 = env.make_key()
        if k2 not in env.qdictionary:
            env.add_key(k2)
        best_action_in_k2 = pacman.best_action(env.qdictionary, k2)
        maxx = env.qdictionary[k2][best_action_in_k2]
        expected = reward + (DISCOUNT * maxx)
        action_tuple = (int(action.x), int(action.y))
        change = LEARNING_RATE * (expected - env.qdictionary[k1][action_tuple])
        env.qdictionary[k1][action_tuple] += change
        #############################################

    if training:
        ####moment before pacman update position
        env.set_params(pacman1, ghosts, nodes, coins)
        k1 = env.make_key()
        if k1 not in env.qdictionary:
            env.add_key(k1)
        ##########################################
        #print k1, env.qdictionary[k1]

        #training is boolean passed into update method. It keeps fast speed for pacman for for faster training.
        action = pacman1.update(nodes, env.qdictionary, k1, training)
        reward = -0.05
        for c in coins:
            if (pacman1.coin_collide(c)):
                #play_tick()
                score += 10
                coins.remove(c)
                reward += 3.5
                if (len(coins)==0):
                    print str(episodes)+'   **won**  '+ str(score)
                    episodes += 1
                    if training:
                        LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                    avg_scores_list.append(score)
                    game_start()

        for g in ghosts:
            if (pacman1.ghost_collide(g)):
                #play_ghost()
                reward -= 4.5
                episodes += 1
                if training:
                    LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                print str(episodes)+'    lost    '+ str(score)
                avg_scores_list.append(score)
                game_start()
        if action:
            ####moment after pacman update position
            env.set_params(pacman1, ghosts, nodes, coins)
            k2 = env.make_key()
            if k2 not in env.qdictionary:
                env.add_key(k2)
            best_action_in_k2 = pacman1.best_action(env.qdictionary, k2)
            maxx = env.qdictionary[k2][best_action_in_k2]
            expected = reward + (DISCOUNT * maxx)
            action_tuple = (int(action.x), int(action.y))
            change = LEARNING_RATE * (expected - env.qdictionary[k1][action_tuple])
            env.qdictionary[k1][action_tuple] += change
        #------------------------------------------------------------------------------------------
        ####moment before pacman update position
        env.set_params(pacman2, ghosts, nodes, coins)
        k1 = env.make_key()
        if k1 not in env.qdictionary:
            env.add_key(k1)
        ##########################################
        #print k1, env.qdictionary[k1]

        #training is boolean passed into update method. It keeps fast speed for pacman for for faster training.
        action = pacman2.update(nodes, env.qdictionary, k1, training)
        reward = -0.05
        for c in coins:
            if (pacman2.coin_collide(c)):
                #play_tick()
                score += 10
                coins.remove(c)
                reward += 3.5
                if (len(coins)==0):
                    print str(episodes)+'   **won**  '+ str(score)
                    episodes += 1
                    if training:
                        LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                    avg_scores_list.append(score)
                    game_start()

        for g in ghosts:
            if (pacman2.ghost_collide(g)):
                #play_ghost()
                reward -= 4.5
                episodes += 1
                if training:
                    LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                print str(episodes)+'    lost    '+ str(score)
                avg_scores_list.append(score)
                game_start()
        if action:
            ####moment after pacman update position
            env.set_params(pacman2, ghosts, nodes, coins)
            k2 = env.make_key()
            if k2 not in env.qdictionary:
                env.add_key(k2)
            best_action_in_k2 = pacman2.best_action(env.qdictionary, k2)
            maxx = env.qdictionary[k2][best_action_in_k2]
            expected = reward + (DISCOUNT * maxx)
            action_tuple = (int(action.x), int(action.y))
            change = LEARNING_RATE * (expected - env.qdictionary[k1][action_tuple])
            env.qdictionary[k1][action_tuple] += change
        #-----------------------------------------------------------------------------------
        ####moment before pacman update position
        env.set_params(pacman3, ghosts, nodes, coins)
        k1 = env.make_key()
        if k1 not in env.qdictionary:
            env.add_key(k1)
        ##########################################
        #print k1, env.qdictionary[k1]

        #training is boolean passed into update method. It keeps fast speed for pacman for for faster training.
        action = pacman3.update(nodes, env.qdictionary, k1, training)
        reward = -0.05
        for c in coins:
            if (pacman3.coin_collide(c)):
                #play_tick()
                score += 10
                coins.remove(c)
                reward += 3.5
                if (len(coins)==0):
                    print str(episodes)+'   **won**  '+ str(score)
                    episodes += 1
                    if training:
                        LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                    avg_scores_list.append(score)
                    game_start()

        for g in ghosts:
            if (pacman3.ghost_collide(g)):
                #play_ghost()
                reward -= 4.5
                episodes += 1
                if training:
                    LEARNING_RATE = 0.5 - (0.45*episodes)/TRAIN_EPISODES
                print str(episodes)+'    lost    '+ str(score)
                avg_scores_list.append(score)
                game_start()
        if action:
            ####moment after pacman update position
            env.set_params(pacman3, ghosts, nodes, coins)
            k2 = env.make_key()
            if k2 not in env.qdictionary:
                env.add_key(k2)
            best_action_in_k2 = pacman3.best_action(env.qdictionary, k2)
            maxx = env.qdictionary[k2][best_action_in_k2]
            expected = reward + (DISCOUNT * maxx)
            action_tuple = (int(action.x), int(action.y))
            change = LEARNING_RATE * (expected - env.qdictionary[k1][action_tuple])
            env.qdictionary[k1][action_tuple] += change
    if len(avg_scores_list) >= 10:
        print 'average score for last ten games = '+str(sum(avg_scores_list)/len(avg_scores_list))
        print 'learning rate = '+ str(LEARNING_RATE)
        del avg_scores_list[:]
    pygame.display.update()



'''
#code to draw the node graph
    for node in nodes:
        pygame.draw.circle(screen,(255,0,0),node.position.toTuple(), 10)
    for node in nodes:
        for nextnode in node.neighbors:
            pygame.draw.line(screen,(255,255,255),node.position.toTuple(), nextnode.position.toTuple(), 2)
'''
from nodemap import score
from nodemap import episodes
from nodemap import training
from nodemap import TRAIN_EPISODES
from nodemap import avg_scores_list
from nodemap import game_start
from nodemap import DISCOUNT
from nodemap import ghosts
from nodemap import nodes
from nodemap import coins
__author__ = 'starlord'
def setEnvironment(env, pacman):
    ####moment before pacman update position
    env.set_params(pacman, ghosts, nodes, coins)
    k1 = env.make_key()
    if k1 not in env.qdictionary:
        env.add_key(k1)
    ##########################################
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

    return env, pacman
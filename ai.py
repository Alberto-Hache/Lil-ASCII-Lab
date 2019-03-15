###############################################################
# AI 
# for "Lil' ASCII Lab" and its entities...

###############################################################
# IMPORT

# libraries
import numpy as np
import random

# Modules
# (none)

###############################################################
#   SETTINGS

# Actions definition:
# An action consists of a verb and some arguments, expressed between brackets here.

Actions_def = {
    "None":             # PASSIVE action.
    (
        [],             # Arguments: Not required.
        0               # Energy ratio: 0x -> No energy consumption.
    ),

    "MOVE":             # MOVING to adjacent relative coordinates.
    (                   # 2 arguments with 8 possible values (excluding (0,0)).
        np.array(       # [x, y] deltas for a given [x0, y0]
            [[-1, -1],[-1, 0],[-1, 1],[0, -1],[0, 1],[1, -1],[1, 0],[1, 1]]
        ),
        1               # Energy ratio: 1x -> Unmodified ratio for 1-tile moves.
    ),

    "FEED":             # FEEDING from adjacent relative coordinates.
    (                   # 2 arguments with 8 possible values (excluding (0,0)).
        np.array(       # [x, y] deltas for a given [x0, y0]
            [[-1, -1],[-1, 0],[-1, 1],[0, -1],[0, 1],[1, -1],[1, 0],[1, 1]]
        ),
        0               # Energy ratio: 0x -> No energy consumption.
    ),
}

###############################################################
# Minds: Auxiliary functions
#   Used by Senses and Policies.

def obtain_possible_moves(world, position, moves_delta_list):
    # Return a list with the deltas from 'moves_delta_list' which,
    # if applied to given 'position', would land on an emptly tile in 'world'.
    possible_moves = [delta for delta in moves_delta_list if world.tile_is_empty(position + delta)]
    return possible_moves

def obtain_possible_bites(world, position, moves_delta_list):
    # Return a list with the deltas from 'moves_delta_list' which,
    # if applied to given 'position', would land on an emptly tile in 'world'.
    possible_moves = [delta for delta in moves_delta_list if world.tile_with_agent(position + delta)]
    return possible_moves

###############################################################
# Minds: Senses
#   TODO

###############################################################
# Minds: Policies
# 
# A policy selects an action at each step for the agent.
#
# - Inputs:
#       - agent.
#       - world [used to query about empty tiles, etc.].
#       - state, the current state of the agent.
#
# - Outputs: the action chosen, as a list:
#       - action_type, e.g. "MOVE", "FEED", "None".
#       - action_arguments, e.g. [-1, 1], [].
#       - action_energy_ratio, the cost invested in the action,
#       as a multiplier of agent.move_cost.

No_action = ["None", Actions_def["None"][0], Actions_def["None"][1]]

def mindless(agent, world, state = None):
    # Void AI, always retuning 'No_action'.
    return(No_action)

def wanderer(agent, world, state = None):
    # It chooses random moves, stopping from time to time.
    # Some parametrizable inertia gives continuity to successful moves.
    # NOTE: 'world' is only passed in order to call auxiliary methods.

    inertia_prob = 0.66 # Probability of repeating latest action.
    stopping_prob = 0.1 # Probability of stopping vs. doing something.
    biting_prob = 0.5   # Probability of biting an adjacent agent vs. moving.

    if random.uniform(0,1) <= inertia_prob and agent.chosen_action_success:
        # Repeat latest action.
        action = agent.chosen_action
    else:
        if random.uniform(0,1) <= stopping_prob:
            # Stop for a while.
            action = No_action
        else:
            # Check for close agents.
            possible_bites = obtain_possible_bites(world, agent.position, Actions_def["FEED"][0])
            if random.uniform(0,1) <= biting_prob and len(possible_bites) > 0:
                # Choose a rondom bite.
                xy_delta = possible_bites[random.randint(0, len(possible_bites) - 1)]
                action = ["FEED", xy_delta, Actions_def["FEED"][1]]
            else:            
                # Choose a random legal move.
                possible_moves = obtain_possible_moves(world, agent.position, Actions_def["MOVE"][0])
                if len(possible_moves) == 0:
                    action = No_action
                else:
                    xy_delta = possible_moves[random.randint(0, len(possible_moves) - 1)]
                    action = ["MOVE", xy_delta, Actions_def["MOVE"][1]]
    
    return(action)
            

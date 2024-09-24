from src.environments.mario_env import MarioJoypadSpace, StepResult
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import numpy as np
import time
from typing import Tuple
from src.utils.utils import save_state_as_png
from src.genetics.genome import Genome
from src.genetics.traverse import Traverse
import numpy as np


def env_init() -> Tuple[MarioJoypadSpace, np.ndarray]:
    "Initialize the super-mario environment."

    ENV_NAME = "SuperMarioBros-v3"
    env = gym_super_mario_bros.make(ENV_NAME)
    env = MarioJoypadSpace(env, SIMPLE_MOVEMENT) # Select available actions for AI
    env.metadata['render_modes'] = "human"
    env.metadata['render_fps'] = 144
    env.unwrapped._lives = 1
 
    state = env.reset() # Good practice to reset the env before using it.
    return env, state

def insert_input(genome:Genome, state: list) -> None:
    start_idx_input_node = 7
    num_input_nodes = 200
    for node in genome.nodes:
        node.value = 0
    
    for i, node in enumerate(genome.nodes[start_idx_input_node:start_idx_input_node+num_input_nodes]): # get all input nodes
        node.value = state[i//20][i % 20] # (Not sure if this is correct)
            

def run_game(env: MarioJoypadSpace, genome: Genome):
    forward = Traverse(genome)
    life2 = 0
    for i in range(1000): # Simulate 200 frames.
        
        action = forward.traverse() 
        if action == -1:
            quit()
        print([node.value for node in genome.output_nodes])
        # print(f"Chosen action: {action}. This is {SIMPLE_MOVEMENT[action]} in SIMPLE_MOVEMENT")
        # move = SIMPLE_MOVEMENT[simple_movement_dict[action]] # Choose to go in the direction NN chooses. BE CAREFUL WITH THE ID OF OUTPUT NODES
        sr = env.step(action) # State, Reward, Done, Info
        save_state_as_png(i + 1, sr.state)
        insert_input(genome, sr.state)
        # print(sr.state) 
        # time.sleep(0.02)
        # if sr.info["life"] == 2 and life2==0:
        #     print(f"Lost a life at frame {i}.")
        #     life2 = 1
        
        # if sr.info["life"] == 0:
        #     print(f"Zero lives at fram: {i}.")
            
        if sr.done:
            print(f"Game over at frame {i}.")
            reward = sr.reward
            env.reset() # Discard the new initial state if done.
            print(reward)
            return reward
            
        env.render()
    print(sr.reward)
    env.close()
    
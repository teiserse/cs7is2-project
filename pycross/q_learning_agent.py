import pycross
import random
import numpy as np
import copy

class q_learning_agent():
    def __init__(self, picross):
        self.picross = picross
        self.q_table = {}

        self.epsilon = 1
        self.exploration_decay_rate = 0.98
        self.learning_rate = 0.1
        self.discount = 0.99
        
        self.initialise_qtable()

    def initialise_qtable(self):
        """
        Function initialises the q_table given the initial state
        """
        actions = self.picross.get_actions()
        for action in actions:
            for line in action[2]:
                self.q_table[tuple(map(tuple, self.picross.puzzle)), (action[0], action[1], tuple(line))] = 0
        
    def is_explore(self):
        """
        Function returns a bool to signify if the agent should explore or exploit.
        This is done by generating a random number and comparing it with the current epsilon parameter.
        Expect the epsilon rate to decrease as the model is refined
        """
        rand = random.uniform(0,1)
        if rand > self.epsilon:
            return False
        return True
    
    def get_action(self):
        """
        Function gets values from the current Q-values
        """
        actions = self.picross.get_actions()
        state = tuple(map(tuple, self.picross.puzzle))
        qvalue_max = float('-inf')
        for action in actions:
            for line in action[2]:
                move = (action[0], action[1], tuple(line))
                if (state, move) not in self.q_table:
                    self.q_table[state, move] = 0
                if self.q_table[state, move] > qvalue_max:
                    max_action = move
                    qvalue_max = self.q_table[state, move]

        try:
            return max_action
        except:
            return move

    def get_value(self, new_state):
        """
        Function gets the best q value for a possible action in the current
        Q-table
        """
        possible_actions = []
        actions = new_state.get_actions()
        q_value = float("-inf")
        for action in actions:
            for line in action[2]:
                state = tuple(map(tuple, new_state.puzzle))
                current_action = (action[0], action[1], tuple(line))
                if (state, current_action) not in self.q_table:
                    self.q_table[state, current_action] = 0
                if self.q_table[state, current_action] > q_value:
                    q_value = self.q_table[state, current_action]
        
        return q_value


    def get_random_action(self):
        """
        Function gets a random action
        """
        actions = self.picross.get_actions()
        line = random.choice(actions)
        action = random.choice(line[2])
        return (line[0], line[1], tuple(action))

    def get_reward(self, new_state):
        """
        Function returns reward of a given an action and using the current state.
        The better the outcoome, the higher the reward.
        """
        done = True
        correct = True
        for i in range(new_state.get_height()):
            if not new_state._check_complete(False, i):
                done = False
                break
        if done:
            for i in range(new_state.get_width()):
                if not new_state._check_complete(True, i):
                    correct = False
                    break
            if correct:
                return 1000, done
            else:
                return -10, done
        else:
            return 1, done

    def step(self, action):
        """
        Function takes an actions and determines the new reward and state
        """
        index = action[0]
        row = action[1]
        line = action[2]

        new_state = copy.deepcopy(self.picross)
        if row:
            for i in range(new_state.get_width()):
                new_state[index][i] = line[i]
        else:
            for i in range(new_state.get_height()):
                new_state[i][index] = line[i]

        reward, done = self.get_reward(new_state)
        return new_state, reward, done

    def update_qtable(self, action, new_state, reward):
        state = tuple(map(tuple, self.picross.puzzle))
        if (state, action) not in self.q_table:
            q_table[state, action] = 0

        v1 = self.get_value(new_state)
        self.q_table[state, action] = self.q_table[state, action]*(1-self.learning_rate) + self.learning_rate*(reward + self.discount*v1)

    def test(self, index, row=True):
        result = self.picross.get_possible_actions(index, row)
        return result

if __name__ == '__main__':
    num_episodes = 10000
    max_step_per_episode = 100
    rewards_all_episodes = []
    original_picross = pycross.from_json(open("pycross/examples/1.json").read())
    agent = q_learning_agent(copy.deepcopy(original_picross))

    #Q-Learning Algo
    for episode in range(num_episodes):
        done = False
        rewards_current_episode = 0
        agent.picross.puzzle = original_picross.puzzle.copy()
        agent.epsilon *= agent.exploration_decay_rate
        for step in range(max_step_per_episode):
            if agent.is_explore():
                action = agent.get_random_action()
            else:
                action = agent.get_action()
            
            new_state, reward, done = agent.step(action)
            agent.update_qtable(action, new_state, reward)
            agent.picross.puzzle = new_state.puzzle.copy()
            rewards_current_episode += reward

            if done:
                break
        rewards_all_episodes.append(reward)

    print(rewards_all_episodes)
import numpy as np
import random

class QLearningAgent:
    def __init__(self, grid_size=(4, 4), learning_rate=0.1, discount_factor=0.9, epsilon=0.1, episodes=500):
        self.grid_size = grid_size
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.episodes = episodes

        self.n_states = grid_size[0] * grid_size[1]
        self.n_actions = 4  # up, down, left, right
        self.q_table = np.zeros((self.n_states, self.n_actions))

        # environment setup
        self.start = (0, 0)
        self.goal = (0, 3)
        self.traps = [(1, 1), (3, 0)]
        self.rewards = {
            "goal": 10,
            "trap": -10,
            "step": -1
        }

    def state_to_index(self, state):
        """Convert (row, col) to index"""
        return state[0] * self.grid_size[1] + state[1]

    def index_to_state(self, index):
        """Convert index back to (row, col)"""
        return divmod(index, self.grid_size[1])

    def get_next_state(self, state, action):
        """Returns next state and reward"""
        r, c = state
        if action == 0 and r > 0: r -= 1        
        elif action == 1 and r < self.grid_size[0] - 1: r += 1  
        elif action == 2 and c > 0: c -= 1     
        elif action == 3 and c < self.grid_size[1] - 1: c += 1  

        next_state = (r, c)
        reward = self.rewards["step"]

        if next_state in self.traps:
            reward = self.rewards["trap"]
        elif next_state == self.goal:
            reward = self.rewards["goal"]

        done = next_state in self.traps or next_state == self.goal
        return next_state, reward, done

    def choose_action(self, state_index):
        """Epsilon-greedy policy"""
        if random.uniform(0, 1) < self.epsilon:
            return random.randint(0, self.n_actions - 1)
        else:
            return np.argmax(self.q_table[state_index])

    def train(self):
        rewards_per_episode = []

        for ep in range(self.episodes):
            state = self.start
            total_reward = 0

            for _ in range(100):  # max 100 steps
                s_idx = self.state_to_index(state)
                action = self.choose_action(s_idx)

                next_state, reward, done = self.get_next_state(state, action)
                next_idx = self.state_to_index(next_state)

                # Bellman update
                self.q_table[s_idx, action] += self.lr * (
                    reward + self.gamma * np.max(self.q_table[next_idx]) - self.q_table[s_idx, action]
                )

                total_reward += reward
                state = next_state

                if done:
                    break

            rewards_per_episode.append(total_reward)

        return {
            "q_table": self.q_table.tolist(),
            "rewards": rewards_per_episode,
            "average_reward": np.mean(rewards_per_episode)
        }

if __name__ == "__main__":
    agent = QLearningAgent()
    result = agent.train()
    print("Average Reward:", result["average_reward"])
    print("Q-Table:")
    print(np.round(agent.q_table, 2))
    np.save("data/qtable.npy", agent.q_table)

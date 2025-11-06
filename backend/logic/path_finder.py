import numpy as np

class PathFinder:
    def __init__(self, grid_size=(4, 4)):
        self.grid_size = grid_size
        self.start = (0, 0)
        self.goal = (0, 3)
        self.traps = [(1, 1), (3, 0)]
        self.actions = ["up", "down", "left", "right"]

    def state_to_index(self, state):
        return state[0] * self.grid_size[1] + state[1]

    def index_to_state(self, index):
        return divmod(index, self.grid_size[1])

    def get_next_state(self, state, action):
        r, c = state
        if action == 0 and r > 0: r -= 1
        elif action == 1 and r < self.grid_size[0] - 1: r += 1
        elif action == 2 and c > 0: c -= 1
        elif action == 3 and c < self.grid_size[1] - 1: c += 1
        return (r, c)

    def find_path(self, q_table_path="data/qtable.npy", max_steps=30):
        q_table = np.load(q_table_path)
        path = []
        state = self.start

        for _ in range(max_steps):
            state_idx = self.state_to_index(state)
            action = np.argmax(q_table[state_idx])
            next_state = self.get_next_state(state, action)
            path.append(self.actions[action])

            if next_state == self.goal:
                path.append("goal")
                break
            if next_state in self.traps:
                path.append("trap")
                break
            state = next_state

        return path

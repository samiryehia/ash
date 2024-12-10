from gymnasium import Env, spaces
import numpy as np

class SmartHomeEnv(Env):
    def __init__(self):
        super(SmartHomeEnv, self).__init__()
        self.action_space = spaces.Discrete(20)  # Updated for 20 actions
        self.observation_space = spaces.Box(low=0, high=1, shape=(16,), dtype=np.float32)
        self.state = self._get_initial_state()
        self.step_count = 0
        self.max_steps = 100

    def _get_initial_state(self):
        device_states = np.random.randint(0, 2, 5)
        energy_metrics = np.random.rand(5)
        user_preferences = np.random.randint(0, 2, 2)
        environmental_data = np.random.rand(3)
        occupancy_status = np.random.randint(0, 2, 1)
        return np.concatenate([device_states, energy_metrics, user_preferences, environmental_data, occupancy_status])

    def step(self, action):
        self.step_count += 1
        energy_saved = np.random.uniform(0.1, 1.0)
        comfort_level = np.random.uniform(0.5, 1.0)
        reward = (energy_saved * 0.6) + (comfort_level * 0.4)
        self.state = self._get_initial_state()
        done = self.step_count >= self.max_steps
        return self.state, reward, done, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = self._get_initial_state()
        self.step_count = 0
        return self.state, {}

    def render(self, mode="human"):
        pass

    def close(self):
        pass

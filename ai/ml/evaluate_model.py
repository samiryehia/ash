from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from smart_home_env import SmartHomeEnv


def evaluate_model():
    """
    Evaluate the trained reinforcement learning model.
    """
    # Load the trained model
    model = PPO.load("models/trained_model")

    # Wrap the environment in a DummyVecEnv
    env = DummyVecEnv([lambda: SmartHomeEnv()])

    # Reset the environment
    obs = env.reset()  # DummyVecEnv only returns observation

    total_reward = 0
    for _ in range(100):  # Evaluate for 100 steps
        # Predict the action
        action, _ = model.predict(obs, deterministic=True)

        # Step the environment
        obs, reward, done, _ = env.step(action)
        total_reward += reward

        # Reset the environment if done
        if done.any():  # VecEnv uses arrays for `done`
            obs = env.reset()

    print(f"Total reward over 100 steps: {total_reward.sum()}")


if __name__ == "__main__":
    evaluate_model()

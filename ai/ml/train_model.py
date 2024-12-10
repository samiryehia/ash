from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from smart_home_env import SmartHomeEnv


def train_rl_model():
    """
    Train the reinforcement learning model using PPO.
    """
    # Create the environment
    env = DummyVecEnv([lambda: SmartHomeEnv()])

    # Define the policy network architecture
    policy_kwargs = dict(net_arch=[64, 64])

    # Initialize the PPO model
    model = PPO("MlpPolicy", env, policy_kwargs=policy_kwargs, verbose=1)

    # Train the model
    TIMESTEPS = 100000
    model.learn(total_timesteps=TIMESTEPS)

    # Save the trained model
    model.save("models/trained_model")
    print("Model training complete and saved as 'models/trained_model.zip'.")


if __name__ == "__main__":
    train_rl_model()

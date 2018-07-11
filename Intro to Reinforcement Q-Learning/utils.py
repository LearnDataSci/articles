import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import clear_output
from time import sleep

def print_frames(frames):
    for frame in frames:
        clear_output(wait=True)
        print(frame['frame'].getvalue())
        print(f"State: {frame['state']}")
        print(f"Reward: {frame['reward']}")
        sleep(.1)


def plot_q_table(q_table):
    fig, ax = plt.subplots(figsize=(16,16))
    ax = sns.heatmap(q_table, cmap="Blues")     
    plt.show()


def display_training_info(episode, epochs):
	pass



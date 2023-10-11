import gym
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import IPython

def show(states):
    fig = plt.Figure()
    ax = fig.subplots()
    ax.matshow(np.zeros([4,4]), cmap='bwr',alpha=0.0)
    sc = ax.scatter(0, 0, color='red', s=500)  
    ax.text(0, 0, 'start', ha='center', va='center')
    ax.text(3, 3, 'end', ha='center', va='center')
    # Adding grid lines to the plot
    ax.set_xticks(np.arange(-.5, 4, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 4, 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=2)
    def update(t):
        sc.set_offsets(states[t])
    ani = FuncAnimation(fig,update,frames=len(states))
    IPython.display(IPython.display.HTML(ani.to_jshtml()))

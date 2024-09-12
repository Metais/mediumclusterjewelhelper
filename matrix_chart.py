import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

class Price_type(Enum):
    AVERAGE = 1
    LOWEST = 2

# Adjust as needed (min and max of avg chaos price on the color scale)
VMIN = 0
VMAX = 200
INPUT_FILE = 'outputs/projectile_output.txt'
PRICE_TYPE = Price_type.AVERAGE

def sort_dict(d):
    """Recursively sorts a dictionary and any nested dictionaries by key."""
    if isinstance(d, dict):
        # Sort the outer dictionary and recursively sort each inner dictionary
        return {k: sort_dict(v) for k, v in sorted(d.items())}
    else:
        # If it's not a dictionary, return as is
        return d
    
def make_plot(matrix, notables):
    # Plot the heatmap
    fig, ax = plt.subplots()
    cax = ax.matshow(matrix, cmap="viridis", vmin=VMIN, vmax=VMAX)  # You can change the colormap if you prefer

    # Set axis labels
    ax.set_xticks(range(len(notables)))
    ax.set_xticklabels(notables)
    ax.set_yticks(range(len(notables)))
    ax.set_yticklabels(notables)

    # Rotate x-axis labels
    plt.xticks(rotation=90)

    # Add color bar
    plt.colorbar(cax)

    # Add text annotations
    for i in range(len(notables)):
        for j in range(len(notables)):
            value = matrix[i, j]
            if not np.isnan(value):
                ax.text(j, i, int(value), va='center', ha='center', color='white')

    plt.show()

# Read terminal output
with open(INPUT_FILE, 'r') as f:
    notables = {}
    
    while True:
        name_line = f.readline()
        if name_line is None or name_line == '':
            break

        name_line = name_line.strip().split(', ')
        price_line = f.readline().strip()
        f.readline()
        f.readline()

        notable_1 = name_line[0][1:]
        notable_2 = name_line[1][:-2]
        
        # Average price
        if PRICE_TYPE == Price_type.AVERAGE:
            price = float(price_line.split('=')[1].split(' ')[0])
        # Lowest price
        elif PRICE_TYPE == Price_type.LOWEST:
            price = float(price_line.split('=')[2].strip())

        if notable_1 not in notables.keys():
            notables[notable_1] = {}
        if notable_2 not in notables.keys():
            notables[notable_2] = {}

        notables[notable_1][notable_2] = price
        notables[notable_2][notable_1] = price

    sorted_notables = sort_dict(notables)



matrix = np.full((len(sorted_notables.keys()), len(sorted_notables.keys())), np.nan)

for i, outer_key in enumerate(sorted_notables.keys()):
    for j, inner_key in enumerate(sorted_notables.keys()):
        if outer_key != inner_key:
            matrix[i, j] = sorted_notables[outer_key][inner_key]

make_plot(matrix, sorted_notables.keys())
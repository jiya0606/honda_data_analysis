import os
import pandas as pd
import matplotlib.pyplot as plt
import re

# Define the action unit columns
action_units = [
    ' AU01_c', ' AU02_c', ' AU04_c', ' AU05_c', ' AU06_c', ' AU07_c', 
    ' AU09_c', ' AU10_c', ' AU12_c', ' AU14_c', ' AU15_c', ' AU17_c', 
    ' AU20_c', ' AU23_c', ' AU25_c', ' AU26_c', ' AU28_c', ' AU45_c'
]

def count_ones(data, columns):
    counts = {}
    for column in columns:
        if column in data.columns:
            counts[column] = (data[column] == 1).sum()
        else:
            counts[column] = 0
    return counts

def create_bar_chart(counts, csv_name, ax):
    labels, values = zip(*counts.items())
    bars = ax.bar(labels, values)
    ax.set_title(f'Occurrences of 1 in Action Units - {csv_name}')
    ax.set_xlabel('Action Units')
    ax.set_ylabel('Count of 1')
    ax.tick_params(axis='x', rotation=45)
    
    # Annotate bars with counts
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom')

def extract_index(filename):
    match = re.search(r'_(\d+)_', filename)
    return int(match.group(1)) if match else -1

def process_csv_files(folder_path):
    before_files = sorted([f for f in os.listdir(folder_path) if f.endswith('_before.csv')], key=extract_index)
    after_files = sorted([f for f in os.listdir(folder_path) if f.endswith('_after.csv')], key=extract_index)
    
    num_files = max(len(before_files), len(after_files))
    
    fig, axes = plt.subplots(num_files, 2, figsize=(24, num_files * 4))

    for idx, filename in enumerate(before_files):
        csv_path = os.path.join(folder_path, filename)
        data = pd.read_csv(csv_path)
        csv_name = os.path.splitext(filename)[0]
        counts = count_ones(data, action_units)
        create_bar_chart(counts, csv_name, axes[idx, 0])

    for idx, filename in enumerate(after_files):
        csv_path = os.path.join(folder_path, filename)
        data = pd.read_csv(csv_path)
        csv_name = os.path.splitext(filename)[0]
        counts = count_ones(data, action_units)
        create_bar_chart(counts, csv_name, axes[idx, 1])

    plt.tight_layout()
    output_filename = 'combined_action_unit_counts.png'
    plt.savefig(output_filename)
    print(f"Output saved to {output_filename}")
    plt.close()

#Replace with path of folder that contains CSV files 
folder_path = 'D103/D103_S1'
process_csv_files(folder_path)





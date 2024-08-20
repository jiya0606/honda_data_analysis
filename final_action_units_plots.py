import os
import pandas as pd
import matplotlib.pyplot as plt
import re
from pathlib import Path
from scipy.stats import pearsonr, spearmanr

# Define the action unit columns
action_units = [
    ' AU01_c', ' AU02_c', ' AU04_c', ' AU05_c', ' AU06_c', ' AU07_c', 
    ' AU09_c', ' AU10_c', ' AU12_c', ' AU14_c', ' AU15_c', ' AU17_c', 
    ' AU20_c', ' AU23_c', ' AU25_c', ' AU26_c', ' AU28_c', ' AU45_c'
]

# Good Signal array
#good_signal = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']  # Add indexes here as needed
good_signal = ['8', '10']

# Variables for customization
subject_prefix = "D124"  # Example: "D106"
session_id = "S4"        # Example: "S4"

def count_ones(data, columns):
    counts = {}
    for column in columns:
        if column in data.columns:
            counts[column] = (data[column] == 1).sum()
        else:
            counts[column] = 0
    return counts

def compute_correlations(data):
    pearson_corr = {}
    spearman_corr = {}
    for au in action_units:
        if data[au].var() > 0:  # Ensure that there is variation in the data
            pearson_corr[au] = pearsonr(data[au], range(len(data)))[0]
            spearman_corr[au] = spearmanr(data[au], range(len(data)))[0]
        else:
            pearson_corr[au] = float('nan')
            spearman_corr[au] = float('nan')
    return pearson_corr, spearman_corr

def compute_percent_abundance(data):
    total_counts = data.sum(axis=0)
    percent_abundance = (total_counts / total_counts.sum()) * 100
    return percent_abundance

def create_bar_chart(counts, csv_name, ax):
    labels, values = zip(*counts.items())
    bars = ax.bar(labels, values)
    ax.set_title(f'{csv_name}')
    ax.set_xlabel('Action Units')
    ax.set_ylabel('Count of 1')
    ax.tick_params(axis='x', rotation=45)
    
    # Calculate total to compute percentages
    total = sum(values)
    
    # Annotate bars with percentages
    for bar in bars:
        yval = bar.get_height()
        percentage = (yval / total) * 100 if total > 0 else 0
        ax.text(bar.get_x() + bar.get_width()/2, yval, f'{percentage:.1f}%', va='bottom')

def extract_index(filename):
    match = re.search(rf'{session_id}_(\d+)_', filename)  # Refine the regex to extract the index correctly
    return match.group(1) if match else '-1'

def categorize_files(filenames):
    good_files = []
    bad_files = []
    for filename in filenames:
        index = extract_index(filename)
        if index in good_signal:
            good_files.append(filename)
        else:
            bad_files.append(filename)
    return good_files, bad_files

def analyze_category(files, folder_path):
    all_data = pd.DataFrame(columns=action_units)
    pearson_corrs = {au: [] for au in action_units}
    spearman_corrs = {au: [] for au in action_units}
    percent_abundances = {au: [] for au in action_units}

    for file in files:
        data = pd.read_csv(os.path.join(folder_path, file))
        counts = count_ones(data, action_units)
        all_data = pd.concat([all_data, pd.DataFrame([counts])], ignore_index=True)

        # Compute correlations
        pearson_corr, spearman_corr = compute_correlations(data)
        for au in action_units:
            if not pd.isna(pearson_corr[au]):
                pearson_corrs[au].append(pearson_corr[au])
            if not pd.isna(spearman_corr[au]):
                spearman_corrs[au].append(spearman_corr[au])

        # Compute percent abundance
        percent_abundance = compute_percent_abundance(data)
        for au in action_units:
            percent_abundances[au].append(percent_abundance[au])

    # Average correlations and percent abundances
    avg_pearson = {au: (sum(pearson_corrs[au]) / len(pearson_corrs[au]) if pearson_corrs[au] else float('nan')) for au in action_units}
    avg_spearman = {au: (sum(spearman_corrs[au]) / len(spearman_corrs[au]) if spearman_corrs[au] else float('nan')) for au in action_units}
    avg_percent_abundance = {au: (sum(percent_abundances[au]) / len(percent_abundances[au]) if percent_abundances[au] else float('nan')) for au in action_units}
    
    return avg_pearson, avg_spearman, avg_percent_abundance

def save_statistics_to_csv(good_before_stats, good_after_stats, bad_before_stats, bad_after_stats, output_path):
    # Create a DataFrame to hold all statistics
    stats_data = {
        'Action Unit': action_units,
        'Good Before Pearson': [good_before_stats[0][au] for au in action_units],
        'Good Before Spearman': [good_before_stats[1][au] for au in action_units],
        'Good Before Abundance (%)': [good_before_stats[2][au] for au in action_units],
        'Good After Pearson': [good_after_stats[0][au] for au in action_units],
        'Good After Spearman': [good_after_stats[1][au] for au in action_units],
        'Good After Abundance (%)': [good_after_stats[2][au] for au in action_units],
        'Bad Before Pearson': [bad_before_stats[0][au] for au in action_units],
        'Bad Before Spearman': [bad_before_stats[1][au] for au in action_units],
        'Bad Before Abundance (%)': [bad_before_stats[2][au] for au in action_units],
        'Bad After Pearson': [bad_after_stats[0][au] for au in action_units],
        'Bad After Spearman': [bad_after_stats[1][au] for au in action_units],
        'Bad After Abundance (%)': [bad_after_stats[2][au] for au in action_units],
    }
    
    stats_df = pd.DataFrame(stats_data)
    
    # Save the DataFrame to a CSV file in the specified folder
    csv_filename = f"{subject_prefix}_{session_id}_au_csv.csv"
    stats_df.to_csv(os.path.join(output_path, csv_filename), index=False)

def process_csv_files(folder_path):
    before_files = sorted([f for f in os.listdir(folder_path) if f.startswith(subject_prefix) and f.endswith('_before.csv')])
    after_files = sorted([f for f in os.listdir(folder_path) if f.startswith(subject_prefix) and f.endswith('_after.csv')])
    
    good_before, bad_before = categorize_files(before_files)
    good_after, bad_after = categorize_files(after_files)

    total_rows = max(len(good_before), len(bad_before))
    
    fig, axes = plt.subplots(total_rows + 1, 4, figsize=(24, (total_rows + 1) * 4))
    
    # Add headers for the columns
    fig.suptitle('Good Signal' + ' ' * 100 + 'Bad Signal', fontsize=16, fontweight='bold')
    axes[0, 0].set_title('Good Signal Before')
    axes[0, 1].set_title('Good Signal After')
    axes[0, 2].set_title('Bad Signal Before')
    axes[0, 3].set_title('Bad Signal After')
    
    row = 0
    for before_file, after_file in zip(good_before, good_after):
        csv_before = pd.read_csv(os.path.join(folder_path, before_file))
        counts_before = count_ones(csv_before, action_units)
        create_bar_chart(counts_before, before_file.replace(".csv", ""), axes[row, 0])
        
        csv_after = pd.read_csv(os.path.join(folder_path, after_file))
        counts_after = count_ones(csv_after, action_units)
        create_bar_chart(counts_after, after_file.replace(".csv", ""), axes[row, 1])
        row += 1
    
    row = 0  # Reset for the bad signal column
    for before_file, after_file in zip(bad_before, bad_after):
        csv_before = pd.read_csv(os.path.join(folder_path, before_file))
        counts_before = count_ones(csv_before, action_units)
        create_bar_chart(counts_before, before_file.replace(".csv", ""), axes[row, 2])
        
        csv_after = pd.read_csv(os.path.join(folder_path, after_file))
        counts_after = count_ones(csv_after, action_units)
        create_bar_chart(counts_after, after_file.replace(".csv", ""), axes[row, 3])
        row += 1

    # Perform statistical analysis
    good_before_stats = analyze_category(good_before, folder_path)
    good_after_stats = analyze_category(good_after, folder_path)
    bad_before_stats = analyze_category(bad_before, folder_path)
    bad_after_stats = analyze_category(bad_after, folder_path)

    # Save statistics to CSV in the same folder as the CSV files
    save_statistics_to_csv(good_before_stats, good_after_stats, bad_before_stats, bad_after_stats, folder_path)

    plt.tight_layout(rect=[0, 0.08, 1, 0.95])  # Adjust layout to accommodate the title
    
    # Save the plot to the same folder as the CSV files
    image_filename = f"{subject_prefix}_{session_id}_au_graphs.png"
    plt.savefig(os.path.join(folder_path, image_filename))


# Call the main function with the path to the folder containing the CSV files
if __name__ == "__main__":
    folder_path = 'openface_results/D124/D124_S4'  # Replace with your actual path
    process_csv_files(folder_path)
